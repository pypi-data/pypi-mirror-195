from datetime import datetime
from dingsdk.core import DingSDKCore

_timestrf = '%Y-%m-%d %H:%M:%S'


class Attendance(DingSDKCore):

    def get_clock_details(self, usersid:str, stime:datetime, etime:datetime) -> list:
        """获取打卡详情
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多7天;
            - usersid 考勤员工的 UserId, 使用英文逗号分隔多个;
        
        https://open.dingtalk.com/document/orgapp/attendance-clock-in-record-is-open
        """
        size, results, usersid = 50, [], usersid.split(',')
        func = lambda uid: self._get_clock_details(uid, stime, etime)
        
        for i in range(0, len(usersid), size):
            results.extend(func(usersid[i: i+size]))
        return results

    def get_leave_rulers(self, opuserid:str) -> list:
        """查询假期规则列表
        
        params:
            - opuserid 操作人的 UserId
        
        https://open.dingtalk.com/document/orgapp/holiday-type-query
        """
        kws = {
            'method': 'POST',
            'url': 'topapi/attendance/vacation/type/list',
            'json': {'op_userid': opuserid, 'vacation_source':'all'}
        }
        return self.oapi(**kws).get('result', [])

    def get_leave_repars(self, userid:str, names:str, stime:datetime, etime:datetime) -> list:
        """获取报表假期数据
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多7天;
            - names 假期名称, 使用英文逗号分隔多个;
            - userid 考勤员工的 UserId;
        
        注意: 对返回的结果进行了优化, 将columnvo并入到columnvals中, 组成列表包含二者的所有字段
        
        https://open.dingtalk.com/document/orgapp/obtains-the-holiday-data-from-the-smart-attendance-report
        """
        size, results, names = 20, [], names.split(',')
        func = lambda name: self._get_leave_repars(userid, name, stime, etime)
        
        for i in range(0, len(names), size):
            results.extend(func(names[i: i+size]))
        return results

    def get_leave_status(self, usersid:str, stime:datetime, etime:datetime) -> list:
        """查询请假状态
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多180天;
            - usersid 请假员工的 UserId, 使用英文逗号分隔多个;
        
        https://open.dingtalk.com/document/orgapp/query-status
        """
        size, results, usersid = 100, [], usersid.split(',')
        func = lambda uid: self._get_leave_status(uid, stime, etime)
        
        for i in range(0, len(usersid), size):
            results.extend(func(usersid[i: i+size]))
        return results

    def get_leave_quotas(self, usersid:str, opuserid:str, codes:str) -> list:
        """查询假期余额
        
        params:
            - codes 假期类型编号, 使用英文逗号分隔多个, 可通过查询假期规则定义接口获取;
            - usersid 查询的员工 UserId, 使用英文逗号分隔多个;
            - opuserid 管理员的 UserId;
        
        https://open.dingtalk.com/document/orgapp/query-holiday-balance
        """
        kws = {
            'method': 'POST',
            'url': 'topapi/attendance/vacation/quota/list',
            'json': {
                'userids': usersid, 'leave_code': codes,
                'op_userid': opuserid, 'offset': 0, 'size': 50
            }
        }
        response = self.oapi(**kws).get('result', {})
        results = response.get('leave_quotas', [])
        
        while response.get('has_more', False):
            kws['json']['offset'] += kws['json']['size']
            response = self.oapi(**kws).get('result', {})
            results.extend(response.get('leave_quotas', []))
        return results

    def get_attendance_repars(self, userid:str, codes:str, stime:datetime, etime:datetime) -> list:
        """获取考勤报表列值
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多31天;
            - userid 考勤员工的 UserId;
            - codes 报表列编号, 使用英文逗号分隔多个;
        
        注意: 对返回的结果进行了优化, 将columnvo并入到columnvals中, 组成列表包含二者的所有字段
        
        https://open.dingtalk.com/document/orgapp/queries-the-column-value-of-the-attendance-report
        """
        size, results, codes = 20, [], codes.split(',')
        func = lambda code: self._get_attendance_repars(
            userid, code, stime, etime)
        
        for i in range(0, len(codes), size):
            results.extend(func(codes[i: i+size]))
        return results

    def get_attendance_columns(self) -> list:
        """获取考勤报表列定义
        
        https://open.dingtalk.com/document/orgapp/queries-the-enterprise-attendance-report-column
        """
        kws = {
            'method': 'POST',
            'url': 'topapi/attendance/getattcolumns',
        }
        return self.oapi(**kws).get('result',{}).get('columns', [])

    def _get_clock_details(self, usersid:list, stime:datetime, etime:datetime) -> list:
        """获取打卡详情
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多7天;
            - usersid 考勤员工的 UserId, 每次最多50个;
        
        https://open.dingtalk.com/document/orgapp/attendance-clock-in-record-is-open
        """
        kws = {
            'method': 'POST',
            'url': 'attendance/listRecord',
            'json': {
                'userIds': usersid, 'isI18n': False,
                'checkDateTo': etime.strftime(_timestrf), 
                'checkDateFrom': stime.strftime(_timestrf), 
            }
        }
        return self.oapi(**kws).get('recordresult', [])

    def _get_leave_repars(self, userid:str, names:list, stime:datetime, etime:datetime) -> list:
        """获取报表假期数据
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多7天;
            - names 假期名称, 每次最多20个;
            - userid 考勤员工的 UserId;
        
        注意: 对返回的结果进行了优化, 将columnvo并入到columnvals中, 组成列表包含二者的所有字段
        
        https://open.dingtalk.com/document/orgapp/obtains-the-holiday-data-from-the-smart-attendance-report
        """
        kws = {
            'method': 'POST',
            'url': 'topapi/attendance/getleavetimebynames',
            'json': {
                'userid': userid,
                'leave_names':','.join(names),
                'to_date': etime.strftime(_timestrf),
                'from_date': stime.strftime(_timestrf),
            }
        }
        results = self.oapi(**kws).get(
            'result', {}).get('columns', [])
        
        return [{**column['columnvo'], **col}\
            for column in results for col in column['columnvals']]

    def _get_leave_status(self, usersid:list, stime:datetime, etime:datetime) -> list:
        """查询请假状态
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多180天;
            - usersid 请假员工的 UserId, 每次最多100个;
        
        https://open.dingtalk.com/document/orgapp/query-status
        """
        kws = {
            'method': 'POST',
            'url': 'topapi/attendance/getleavestatus',
            'json': {
                'offset': 0, 'size': 20,
                'userid_list': ','.join(usersid),
                'end_time': round(etime.timestamp() * 1000),
                'start_time': round(stime.timestamp() * 1000),
            }
        }
        response = self.oapi(**kws).get('result', {})
        results = response.get('leave_status', [])
        
        while response.get('has_more', False):
            kws['json']['offset'] += kws['json']['size']
            response = self.oapi(**kws).get('result', {})
            results.extend(response.get('leave_status', []))
        return results

    def _get_attendance_repars(self, userid:str, codes:list, stime:datetime, etime:datetime) -> list:
        """获取考勤报表列值
        
        params:
            - stime 打开记录开始时间;
            - etime 打开记录结束时间, 距开始时间最多31天;
            - codes 报表列编号, 每次最多20个;
            - userid 考勤员工的 UserId, 使用英文逗号分隔多个;
        
        注意: 对返回的结果进行了优化, 将columnvo并入到columnvals中, 组成列表包含二者的所有字段
        
        https://open.dingtalk.com/document/orgapp/queries-the-column-value-of-the-attendance-report
        """
        kws = {
            'method': 'POST',
            'url': '/topapi/attendance/getcolumnval',
            'json': {
                'to_date': etime.strftime(_timestrf),
                'from_date': stime.strftime(_timestrf),
                'userid': userid, 'column_id_list': ','.join(codes),
            }
        }
        results = self.oapi(**kws).get(
            'result', {}).get('column_vals', [])

        return [{**column['column_vo'], **col}\
            for column in results for col in column['column_vals']]
