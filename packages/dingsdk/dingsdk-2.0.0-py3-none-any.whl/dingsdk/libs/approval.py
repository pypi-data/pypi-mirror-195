from datetime import datetime
from dingsdk.core import DingSDKCore


class Approval(DingSDKCore):
    
    def get_procid_byname(self, name:str) -> str:
        """获取模板编号
        
        https://open.dingtalk.com/document/orgapp/obtain-the-template-code
        """
        kws = {
            'method': 'GET', 'json': {'name': name},
            'url': '/v1.0/workflow/processCentres/schemaNames/processCodes'
        }
        return self.api(**kws).get('result', {}).get('processCode', '')

    def get_instance_detail(self, instid:str) -> dict:
        """获取单个审批实例详情
        
        https://open.dingtalk.com/document/orgapp/obtains-the-details-of-a-single-approval-instance-pop
        """
        kws = {
            'method': 'GET',
            'json': {'processInstanceId': instid},
            'url': '/v1.0/workflow/processInstances',
        }
        return self.api(**kws).get('result', {})
    
    def get_instancesid(self, procid:str, st:datetime, et:datetime, usersid:str=None, status:str=None) -> list:
        """获取审批实例ID列表
        
        params:
            - procid 审批模板编号, 可通过获取模板编号接口获取;
            - usersid 可选发起人
            - status 可选实例状态
        
        https://open.dingtalk.com/document/orgapp/obtain-an-approval-list-of-instance-ids
        """
        status = status.split(',') if \
            isinstance(status, str) else None
        usersid = usersid.split(',') if \
            isinstance(usersid, str) else None

        pms = {
            'processCode': procid,
            'nextToken': 0, 'maxResults': 20,
            'userIds': usersid, 'statuses': status,
            'endTime': round(et.timestamp() * 1000),
            'startTime': round(st.timestamp() * 1000),
        }
        kws = {
            'method': 'POST', 'json': pms,
            'url': '/v1.0/workflow/processes/instanceIds/query',
        }
        
        response = self.api(**kws).get('result', {})
        next_token = response.get('nextToken', 0)
        results = response.get('list', [])
        
        while next_token >= 1:
            kws['json']['nextToken'] = next_token
            response = self.api(**kws).get('result', {})
            next_token = response.get('nextToken', 0)
            results.extend(response.get('list', []))
        return results
    
    def get_instance_file(self, instid:str, fileid:str) -> str:
        """获取审批实例附件下载链接
        
        https://open.dingtalk.com/document/orgapp/download-an-approval-attachment
        """
        kws = {
            'url': '/v1.0/workflow/processInstances/spaces/files/urls/download',
            'method': 'POST', 'json': {'processInstanceId': instid, 'fileId': fileid},
        }
        return self.api(**kws).get('result', {}).get('downloadUri', '')

    def execute_instance(
        self,
        procid:str,
        taskid:int,
        opuserid:str,
        result:bool=True,
        remark:str=None,
        file:object=None
        ) -> bool:
        """同意或拒绝审批任务
        
        params:
            - procid
            - taskid
            - opuserid
            - result
            - remark
            - file
        
        https://open.dingtalk.com/document/orgapp/approve-or-reject-the-approval-task
        """
        pms = {
            'taskId': taskid, 'remark': remark, 'file': file,
            'result': {True: 'agree', False: 'refuse'}.get(result),
            'processInstanceId': procid, 'actionerUserId': opuserid, 
        }
        kws = {
            'method': 'POST', 'json': pms,
            'url': '/v1.0/workflow/processInstances/execute'
        }
        return self.api(**kws).get('success', False)
