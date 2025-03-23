"""delay为发送消息的延迟"""


class Plugin:
    def __init__(self, **kwargs):
        self.pid: int = kwargs.get('pid')
        self.name: str = kwargs.get('name')
        self.author: str = kwargs.get('author')
        self.ver: str = kwargs.get('version')
        self.setting = kwargs.get('setting')
        self.if_privateMsg = kwargs.get('if_privateMsg')
        self.if_groupMsg = kwargs.get('if_groupMsg')
        self.if_notice = kwargs.get('if_notice')
        self.complain = kwargs.get('complain')
        self.enable = kwargs.get('enable', True)
        self.respond_group_msg = kwargs.get('respond_group_msg')
        self.respond_private_msg = kwargs.get('respond_private_msg')
        self.respond_notice = kwargs.get('respond_notice')
        self.respond_request = kwargs.get('respond_request')
        self.enable_func = kwargs.get('enable_func')
        self.on_request = None


class Bot:
    def __init__(self, Api, p_id, name, **kwargs):
        self.api = Api  # 插件被传入的api类，用来调用各种功能
        self.p_id = p_id  # 插件的hash,用来标记唯一插件
        self.quanxian = kwargs
        self.name = name

    def init(self, plu_data: dict):
        self.api = plu_data['Api']  # 插件被传入的api类，用来调用各种功能
        self.p_id = plu_data['p_id']  # 插件的hash,用来标记唯一插件

    def delete_msg(self, msg_id):
        self.api.delete_msg(msg_id)

    def send_group_msg(self, group: int, msg: str, delay=0):
        if self.quanxian.get('can_group'):
            self.api.send_group_msg(delay=delay, group=group, msg=msg, plugin_name=self.name)
        return 0

    def send_msg(self, dic, delay=0):
        self.api.send_msg(delay, dic, plugin_name=self.name)
        return 0

    def send_private_msg(self, user_id, msg, delay=0):
        self.api.send_private_msg(user_id=user_id, msg=msg, delay=delay, plugin_name=self.name)

    def info(self, s: dict):
        self.api.info(s)
        return 0

    def get_skey(self):
        res = self.api.get_skey()
        return res

    def get_gtk(self):
        res = self.api.get_gtk()
        return res

    def delete_friend(self, id: int, delay=0):
        self.api.delete_friend(delay, id=id, plugin_name=self.name)

    def group_request(self, flag, type_, approve, reason, delay=0):
        self.api.group_request(delay, flag=flag, type=type_, approve=approve, reason=reason, plugin_name=self.name)
        return 0

    def friend_request(self, flag, approve, remark, delay=0):  # 加好友请求的 flag（需从上报的数据中获得）|是否同意请求|添加后的好友备注（仅在同意时有效）
        self.api.friend_request(delay, flag=flag, approve=approve, remark=remark, plugin_name=self.name)
        return 0

    def kick(self, group_id: int, user_id, reject_add_request, delay=0):
        self.api.kick(delay, group_id=group_id, user_id=user_id, reject_add_request=reject_add_request,
                      plugin_name=self.name,
                      )
        return 0

    def ban(self, group_id, user_id, time, delay=0):  # 群中单人禁言
        self.api.ban(delay, group_id=group_id, user_id=user_id, time=time, plugin_name=self.name)
        return 0

    def set_title(self, group_id, user_id, special_title, delay=0):
        self.api.set_title(delay, group_id=group_id, user_id=user_id, special_title=special_title,
                           plugin_name=self.name,
                           )
        return 0

    def group_ban(self, group_id, enable, delay=0):
        self.api.group_ban(delay, group_id=group_id, enable=enable, plugin_name=self.name)

    def set_group_special_title(self, gid: int, uid: int, title: str, delay=0):
        self.api.set_group_special_title(delay, gid=gid, uid=uid, title=title, plugin_name=self.name)

    def send_group_sign(self, group_id: int, delay=0):
        self.api.send_group_sign(delay, group_id=group_id, plugin_name=self.name)
