from dingsdk.core import DingSDKCore


class Contacts(DingSDKCore):
    
    def get_user_detail(self, userid:str) -> dict:
        """获取用户详情
        
        https://open.dingtalk.com/document/orgapp/query-user-details
        """
        kws = {
            'method': 'POST', 'url': 'topapi/v2/user/get',
            'json': {'userid': userid, 'language': 'zh_CN'}
        }
        return self.oapi(**kws).get('result', {})
    
    def get_userid_bymobile(self, mobile:str) -> str:
        """根据手机号查询用户 UserId
        
        https://open.dingtalk.com/document/orgapp/query-users-by-phone-number
        """
        kws = {
            'method': 'POST',
            'json': {'mobile': mobile},
            'url': 'topapi/v2/user/getbymobile',
        }
        return self.oapi(**kws).get('result', '')
    
    def get_users_bydeptid(self, deptid:str=1) -> list:
        """获取部门用户详情
        
        params:
            - deptid 部门编号
        
        https://open.dingtalk.com/document/orgapp/queries-the-complete-information-of-a-department-user
        """
        pms = {
            'dept_id': deptid,
            'language': 'zh_CN',
            'cursor': 0, 'size': 100,
            'order_field': 'entry_desc',
            'contain_access_limit': True
        }
        kws = {
            'json': pms, 'method': 'POST',
            'url': 'topapi/v2/user/list',
        }
        response = self.oapi(**kws).get('result', {})
        cursor = response.get('next_cursor', 0)
        results = response.get('list', [])
        
        while cursor >= 1:
            kws['json']['cursor'] = cursor
            response = self.oapi(**kws).get('result', {})
            results.extend(response.get('list', []))
            cursor = response.get('next_cursor', 0)

        return results
    
    def get_dept_detail(self, deptid:str=1) -> dict:
        """获取部门详情
        
        https://open.dingtalk.com/document/orgapp/query-department-details0-v2
        """
        kws = {
            'json': {'dept_id': deptid, 'language': 'zh_CN'},
            'method': 'POST', 'url': 'topapi/v2/department/get',
        }
        return self.oapi(**kws).get('result', {})

    def get_subs_deptid(self, deptid:str=1) -> list:
        """获取子部门 ID 列表
        
        https://open.dingtalk.com/document/orgapp/obtain-a-sub-department-id-list-v2
        """
        kws = {
            'method': 'POST',
            'json': {'dept_id': deptid},
            'url': 'topapi/v2/department/listsubid',
        }
        return self.oapi(**kws).get(
            'result', {}).get('dept_id_list', [])
    
    def get_subs_dept(self, deptid:str=1) -> list:
        """获取子部门列表
        
        https://open.dingtalk.com/document/orgapp/obtain-the-department-list-v2
        """
        kws = {
            'json': {'dept_id': deptid, 'language': 'zh_CN'},
            'method': 'POST', 'url': 'topapi/v2/department/listsub',
        }
        return self.oapi(**kws).get('result', [])
