from dingsdk.core import DingSDKCore

import json


class Chatbot(DingSDKCore):
    
    def send_singles_msg(self, usersid:str, msgkey:str, msgpms:dict) -> dict:
        """批量发送单聊消息
        
        params:
            - msgkey 消息模板
            - msgpms 消息参数
            - usersid 用户的 UserId, 使用英文逗号分隔多个;
            
        https://open.dingtalk.com/document/orgapp/chatbots-send-one-on-one-chat-messages-in-batches
        """
        results = {
            'processQueryKey': [],
            'invalidStaffIdList': [],
            'flowControlledStaffIdList': [],
        }
        size, usersid = 20, usersid.split(',')
        func = lambda uid: self._send_singles_msg(uid, msgkey, msgpms)
        
        for i in range(0, len(usersid), size):
            res = func(usersid[i: i+size])
            results['processQueryKey'].append(
                res.get('processQueryKey', ''))
            results['invalidStaffIdList'].extend(
                res.get('invalidStaffIdList', ''))
            results['flowControlledStaffIdList'].extend(
                res.get('flowControlledStaffIdList', ''))
        return results

    def _send_singles_msg(self, usersid:list, msgkey:str, msgpms:dict) -> dict:
        """批量发送单聊消息
        
        params:
            - msgkey 消息模板
            - msgpms 消息参数
            - usersid 用户的 UserId, 每次最多20个
        https://open.dingtalk.com/document/orgapp/chatbots-send-one-on-one-chat-messages-in-batches
        """
        kwargs = {
            'method': 'POST',
            'url': 'v1.0/robot/oToMessages/batchSend',
            'json': {
                "robotCode": self.appkey, "userIds": usersid,
                "msgKey": msgkey, "msgParam": json.dumps(msgpms),
            }
        }
        return self.api(**kwargs)
    
    def back_singles_msg(self, tasksid:str) -> dict:
        """批量撤回单聊消息, 只能撤回24小时内的消息。
        
        params:
            - tasksid 消息唯一标识, 使用英文逗号分割多个;
        
        https://open.dingtalk.com/document/orgapp/batch-message-recall-chat
        """
        func = self._back_signles_msg
        size, tasksid = 20, tasksid.split(',')
        result = {'successResult': [],'failedResult': []}
        
        for i in range(0, len(tasksid), size):
            res = func(tasksid[i: i+size])
            result['failedResult'].append(
                res.get('failedResult', {}))
            result['successResult'].extend(
                res.get('successResult', []))
        return result

    def _back_singles_msg(self, tasksid:list) -> dict:
        """批量撤回单聊消息, 只能撤回24小时内的消息。
        
        params:
            - tasksid 消息唯一标识, 每次最多20个
        
        https://open.dingtalk.com/document/orgapp/batch-message-recall-chat
        """
        kwargs = {
            'method': 'POST', 'url': 'v1.0/robot/otoMessages/batchRecall',
            'json': {'robotCode': self.appkey, 'processQueryKeys': tasksid}
        }
        return self.api(**kwargs)
