from dingsdk.core import DingSDKCore


class Personnel(DingSDKCore):
    
    def get_onjob_usersid(self, status:str='2,3,5,-1') -> list:
        """获取在职员工 UserId 列表
        
        params:
            - status 在职员工状态筛选，可以查询多个状态, 不同状态之间使用英文逗号分隔。
            支持状态 2:试用期, 3:正式, 5:待离职, -1:无状态, 默认值为 2,3,5,-1。
            
        https://open.dingtalk.com/document/orgapp/intelligent-personnel-query-the-list-of-on-the-job-employees-of-the
        """
        kws = {
            'method': 'POST',
            'url': 'topapi/smartwork/hrm/employee/queryonjob',
            'json': {'status_list': status, 'offset': 0, 'size': 50}
        }
        response = self.oapi(**kws).get('result', {})
        results = response.get('data_list', [])
        cursor = response.get('next_cursor', 0)
        
        while cursor >= 1:
            kws['json']['offset'] = cursor
            response = self.oapi(**kws).get('result', {})
            results.extend(response.get('data_list', []))
            cursor = response.get('next_cursor', 0)
        
        return results
    
    def get_dismiss_usersid(self) -> list:
        """获取离职员工 UserId 列表
        
        https://open.dingtalk.com/document/orgapp/obtain-the-list-of-employees-who-have-left
        """
        kws = {
            'method': 'GET', 
            'url': '/v1.0/hrm/employees/dismissions',
            'json': {'nextToken': 0, 'maxResults': 50}
        }
        response = self.api(**kws)
        results = response.get('userIdList', [])
        next_token = response.get('nextToken', 0)
        
        while next_token >= 1:
            kws['json']['nextToken'] = next_token
            response = self.api(**kws)
            next_token = response.get('nextToken', 0)
            results.extend(response.get('userIdList', []))
        return results

    def get_dismiss_users(self, usersid:str) -> list:
        """获取离职员工信息

        https://open.dingtalk.com/document/orgapp/obtain-resignation-information-of-employees-new-version
        """
        kws = {
            'method': 'GET',
            'json': {'userIdList', usersid.split(',')},
            'url': '/v1.0/hrm/employees/dimissionInfos',
        }
        
        return self.api(**kws).get('result', [])
