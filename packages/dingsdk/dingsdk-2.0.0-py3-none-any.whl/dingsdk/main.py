from dingsdk.libs import *


class DingSDK(
    Chatbot,
    Contacts,
    TaskTodo,
    Approval,
    Personnel,
    Attendance,
    AccessToken
    ):
    """
    - 获取访问凭证 https://open.dingtalk.com/document/orgapp/authorization-overview
        - 获取企业内部应用的 AccessToken `get_token`

    - 通讯录管理 https://open.dingtalk.com/document/orgapp/contacts-overview
        - 查询用户详情 `get_user_detail`
        - 查询 UserId `get_userid_bymobile`
        - 获取部门用户详情 `get_users_bydeptid`
        - 获取部门详细信息 `get_dept_detail`
        - 获取子部门列表 `get_subs_dept`
        - 获取子部门 ID 列表 `get_subs_deptid`

    - 智能人事 https://open.dingtalk.com/document/orgapp/intelligent-personnel-call-description
        - 获取在职员工列表 `get_onjob_usersid`
        - 获取离职员工列表 `get_dismiss_usersid`
        - 获取离职员工信息 `get_dismiss_users`
    
    - 机器人 https://open.dingtalk.com/document/orgapp/robot-overview
        - 批量发送机器人单聊消息 `send_singles_msg`
        - 批量撤回机器人单聊消息 `back_singles_msg`

    - OA审批 https://open.dingtalk.com/document/orgapp/workflow-overview
        - 获取审批模板编号 `get_procid_byname`
        - 获取审批实例详情 `get_instance_detail`
        - 获取审批实例编号 `get_instancesid`
        - 获取审批实例附件 `get_instance_file`
        - 同意或拒绝审批实例 `execute_instance`

    - 待办任务 https://open.dingtalk.com/document/orgapp/dingtalk-todo-task-overview
        - 查询企业下用户待办列表 `get_tasks_byuser`

    - 考勤 https://open.dingtalk.com/document/orgapp/attendance-overview
        - 获取打卡详情记录 `get_clock_details`
        - 获取假期规则定义 `get_leave_rulers`
        - 获取假期报表数据 `get_leave_repars`
        - 获取员工请假状态 `get_leave_status`
        - 获取员工假期剩余 `get_leave_quotas`
        - 获取考勤报表数据 `get_attendance_repars`
        - 获取考勤报表字段 `get_attendance_columns`
    """
