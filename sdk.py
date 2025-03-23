class Bot:
    def __init__(self, Api: object, p_id: int):
        self.api = Api  # 插件被传入的api类，用来调用各种功能
        self.p_id = p_id  # 插件的hash,用来标记唯一插件

    def init(self, plu_data: dict):
        self.api = plu_data['Api']  # 插件被传入的api类，用来调用各种功能
        self.p_id = plu_data['p_id']  # 插件的hash,用来标记唯一插件

    def send_group_msg(self, group: int, msg: str):
        self.api.send_group_msg(group=group, msg=msg, p_id=self.p_id)
        return 0

    def send_msg(self, dic):
        self.api.send_msg(dic, self.p_id)
        return 0

    def info(self, s: dict):
        self.api.info(s)
        return 0

    def get_skey(self):
        res = self.api.get_skey()
        return res

    def get_gtk(self):
        res = self.api.get_gtk()
        return res

    def delete_friend(self, id: int):
        self.api.delete_friend(id=id, p_id=self.p_id)

    def group_request(self, flag, type, approve, reason):
        self.api.group_request(flag=flag, type=type, approve=approve, reason=reason, p_id=self.p_id)
        return 0

    def friend_request(self, flag, approve, remark):  # 加好友请求的 flag（需从上报的数据中获得）|是否同意请求|添加后的好友备注（仅在同意时有效）
        self.api.friend_request(flag=flag, approve=approve, remark=remark, p_id=self.p_id)
        return 0

    def kick(self, group_id: int, user_id, reject_add_request):
        self.api.kick(group_id=group_id, user_id=user_id, reject_add_request=reject_add_request, p_id=self.p_id)
        return 0

    def ban(self, group_id, user_id, time):  # 群中单人禁言
        self.api.ban(group_id=group_id, user_id=user_id, time=time, p_id=self.p_id)
        return 0

    def set_title(self, group_id, user_id, special_title):
        self.api.set_title(group_id=group_id, user_id=user_id, special_title=special_title, p_id=self.p_id)
        return 0

    def group_ban(self, group_id, enable):
        self.api.group_ban(group_id=group_id, enable=enable, p_id=self.p_id)

    def set_group_special_title(self, gid: int, uid: int, title: str):
        self.api.set_group_special_title(gid=gid, uid=uid, title=title, p_id=self.p_id)
