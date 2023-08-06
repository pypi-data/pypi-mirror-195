from dingsdk.core import DingSDKCore


class TaskTodo(DingSDKCore):
    
    def get_tasks_byuser(self, unionid:str, isdone=True) -> list:
        """获取用户待办列表
        
        最多可以获取到180天内已完成状态的待办任务；未完成状态的待办任务无此限制
        
        params:
            - unionid
            - isdone
        
        https://open.dingtalk.com/document/orgapp/query-the-to-do-list-of-enterprise-users
        """
        kws = {
            'url': f'/v1.0/todo/users/{unionid}/org/tasks/query',
            'method': 'POST', 'json': {'nextToken': 0, 'isDone': isdone}
        }
        response = self.api(**kws)
        results = response.get('todoCards', [])
        next_token = response.get('nextToken', 0)

        while next_token >= 1:
            kws['json']['nextToken'] = next_token
            response = self.api(**kws)
            next_token = response.get('nextToken', 0)
            results.extend(response.get('todoCards', []))
        return results
