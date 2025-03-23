import json
import re
import socket
# from time import sleep
# import threading
from queue import Queue

USE_WEBSOCKET = True
try:
    from websocket import create_connection
except ImportError:  # 启用http协议
    USE_WEBSOCKET = False

    HttpResponseHeader = '''HTTP/1.1 200 OK\r\n
    Content-Type: text/html\r\n\r\n
    '''


def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i] == "{" and msg[-1] == "\n":
            return json.loads(msg[i:])
    return None


class HttpClient:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ListenSocket.bind(('127.0.0.1', 5701))
        self.ListenSocket.listen(100)
        # pass

    def rev_msg(self):  # json or None
        Client, Address = self.ListenSocket.accept()
        Request = Client.recv(1024).decode(encoding='utf-8')
        rev_json = request_to_json(Request)
        Client.sendall(HttpResponseHeader.encode(encoding='utf-8'))
        Client.close()
        return rev_json

    def send_msg(self, resp_dict):
        payload = ''
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((self.ip, 5700))

        msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
        number = resp_dict['number']  # 回复账号（群号/好友号）
        msg = resp_dict['msg']  # 要回复的消息

        # 将字符中的特殊字符进行url编码
        msg = msg.replace(" ", "%20")
        msg = msg.replace("\n", "%0a")

        if msg_type == 'group':
            payload = "GET /send_group_msg?group_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + self.ip + ":5700\r\nConnection: close\r\n\r\n"
        elif msg_type == 'private':
            payload = "GET /send_private_msg?user_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + self.ip + ":5700\r\nConnection: close\r\n\r\n"
        # print("发送" + payload)
        client.send(payload.encode("utf-8"))
        client.close()
        return 0

    def send_group_msg(self, group, msg):
        group_id = int(group)
        self.send_msg({'msg_type': 'group', 'number': group_id, 'msg': msg})

    def ban(self, group_id, user_id, time):  # 群中单人禁言
        payload = "GET /set_group_ban?user_id=" + str(
            user_id) + "&group_id=" + str(group_id) + "&duration=" + str(
            time) + " HTTP/1.1\r\nHost:" + self.ip + ":5700\r\nConnection: close\r\n\r\n"
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((self.ip, 5700))
        client.send(payload.encode("utf-8"))
        client.close()

    def group_ban(self, group_id, enable):
        payload = "GET /set_group_whole_ban?group_id=" + str(group_id) + "&enable=" + str(
            enable) + " HTTP/1.1\r\nHost:" + self.ip + ":5700\r\nConnection: close\r\n\r\n"
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((self.ip, 5700))
        client.send(payload.encode("utf-8"))
        client.close()
        return

    def set_title(self, group_id, user_id, special_title):
        special_title = special_title.replace(" ", "%20")
        special_title = special_title.replace("\n", "%0a")  # 进行url编码

        payload = "GET /set_group_special_title?group_id=" + str(group_id) + "&user_id=" + str(
            user_id) + + "&special_title=" + special_title + " HTTP/1.1\r\nHost:" + self.ip + ":5700\r\nConnection: " \
                                                                                              "close\r\n\r\n "
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((self.ip, 5700))
        client.send(payload.encode("utf-8"))
        client.close()
        return

    def set_group_special_title(self, gid: int, uid: int, title: str):  # 设置群专属头衔
        """gid,群号,uid，QQ号,title,专属头衔，不填为删除头衔"""
        self.set_title(group_id=gid, user_id=uid, title=title)


# 需要循环执行，返回值为json格式
class qqbot:  # 使用的是正向websocket
    def __init__(self):
        self.connection = None
        # self.lock = threading.RLock()
        self.recv_queue = Queue()
        self.send_queue = Queue()

    def connect(self, address="ws://127.0.0.1:6700/"):
        if USE_WEBSOCKET:
            # self.lock.acquire()
            self.connection = create_connection(address)
            # self.connection.settimeout(0)
            # self.lock.release()
        else:
            self.connection = HttpClient()

    def send_group_msg(self, group, msg):
        group_id = int(group)
        # self.lock.acquire()
        # self.connection.send()
        res = self.connection.send(
            json.dumps({"action": "send_group_msg", "params": {'group_id': group_id, 'message': msg}}))
        # print(self.recv_queue.get_nowait())
        # print(res)
        # self.lock.release()

    def send_private_msg(self, user_id, msg):
        self.send_queue.put(json.dumps({"action": "send_private_msg", "params": {"message_type": 'private',
                                                                                 'user_id': user_id
            , 'message': msg}}))
        # print(self.rev_msg())

    def rev_msg(self):  # dict_ or None
        # self.lock.acquire()
        rec = self.connection.recv()
        # self.lock.release()
        rev = json.loads(rec)
        if rev is None:
            pass

        # elif 'post_type' in rev and rev['post_type'] != 'meta_event':
        else:
            return rev

    def send_msg(self, dict_):  # 发送消息
        # group_id = dict_['number']
        message_type = dict_['msg_type']
        if message_type == 'private':
            # self.lock.acquire()
            # self.connection.send()
            res = self.connection.send(json.dumps({"action": "send_private_msg", "params": {
                'user_id': dict_['number']
                , 'message': dict_['msg']}}))
            print('private', self.connection.recv())
            # self.lock.release()
        if message_type == 'group':
            # self.lock.acquire()
            res = self.connection.send(json.dumps({"action": "send_group_msg", "params": {'message_type': 'group'
                , 'group_id': dict_['number']
                , 'message': dict_['msg']}}))
            print('group', self.connection.recv())

    def del_msg(self, msg_id):  # 撤回消息
        id1 = int(msg_id)
        self.send_queue.put(json.dumps({"action": "delete_msg", "params": {"message_id": id1}}))
        return self.connection.recv()

    def kick(self, group_id, user_id, reject_add_request):  # reject_add_request意为是否拒绝此人的加群请求,true/false
        gr_id = int(group_id)
        us_id = int(user_id)
        self.send_queue.put(json.dumps({"action": "set_group_kick", "params": {"group_id": gr_id, 'user_id': us_id
            , 'reject_add_request': reject_add_request}}))
        return 0

    def ban(self, group_id, user_id, time):  # 群中单人禁言
        gr_id = int(group_id)
        us_id = int(user_id)
        duration = int(time)
        self.send_queue.put(json.dumps({"action": "set_group_ban", "params": {"group_id": gr_id, 'user_id': us_id
            , 'duration': duration}}))
        return 0

    def group_ban(self, group_id, enable):  # 群禁，enable为是否禁言,true/false
        gr_id = int(group_id)
        self.send_queue.put(
            json.dumps({"action": "set_group_whole_ban", "params": {"group_id": gr_id, 'is_enable': enable}}))
        return 0

    def leave(self, group_id, is_dismiss):  # 是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散
        gr_id = int(group_id)
        self.send_queue.put(
            json.dumps({"action": "set_group_whole_ban", "params": {"group_id": gr_id, 'is_dismiss': is_dismiss}}))

    def set_title(self, group_id, user_id, special_title):
        # gr_id = int(group_id)
        us_id = int(user_id)
        self.send_queue.put(json.dumps({"action": "set_group_special_title",
                                        "params": {"group_id": group_id, 'us_id': us_id,
                                                   'special_title': special_title}}))

    def friend_request(self, flag, approve, remark):  # 加好友请求的 flag（需从上报的数据中获得）|是否同意请求|添加后的好友备注（仅在同意时有效）
        fl = str(flag)
        self.send_queue.put(json.dumps({"action": "set_friend_add_request",
                                        "params": {"flag": fl, 'approve': approve, 'remark': remark}}))

    def group_request(self, flag, type, approve, reason):
        fl = str(flag)
        ty = str(type)
        self.send_queue.put(json.dumps({"action": "set_group_add_request",
                                        "params": {"flag": fl, 'type': ty, 'approve': approve, 'reason': reason}}))

    def delete_friend(self, id):  # 删好友
        id1 = int(id)
        self.send_queue.put(json.dumps({"action": "delete_friend",
                                        "params": {"friend_id": id1}}))

    # @classmethod
    @staticmethod
    def AIfacetoQ(s):
        res1 = re.findall('.face:...}', s)
        if not res1:
            res2 = re.findall('.face:..}', s)
            if not res2:
                res3 = re.findall('.face:.}', s)
                end = res3
            else:
                end = res2
        else:
            end = res1
        # print(end)
        bqid = end[0].replace('{face:', '')
        bq = bqid.replace('}', '')
        th = '[CQ:face,id=' + bq + ']'
        s2 = s.replace(end[0], th)
        return s2

    @staticmethod
    def QfacetoAI(s):
        res1 = re.findall('.CQ:face,id=...]', s)
        if not res1:
            res2 = re.findall('.CQ:face,id=..]', s)
            if not res2:
                res3 = re.findall('.CQ:face,id=.]', s)
                end = res3
            else:
                end = res2
        else:
            end = res1
        bqid = end[0].replace('[CQ:face,id=', '')
        bq = bqid.replace(']', '')
        th = '[CQ:face,id=' + bq + ']'
        s2 = s.replace(end[0], th)
        return s2

    def stranger_info(self, user_id):
        uid = int(user_id)
        self.send_queue.put(json.dumps({"action": "get_stranger_info", "params": {"user_id": uid}}))
        while True:
            rec = json.loads(self.connection.recv())
            if 'data' in rec:
                return rec
                break

    def set_group_special_title(self, gid: int, uid: int, title: str):  # 设置群专属头衔
        """gid,群号,uid，QQ号,title,专属头衔，不填为删除头衔"""
        self.send_queue.put(json.dumps({"action": "set_group_special_title", "params": {"group_id": gid,
                                                                                        'user_id': uid,
                                                                                        'special_title': title,
                                                                                        'duration': -1}}))

    def send_group_sign(self, group_id: int):
        self.send_queue.put(json.dumps({"action": "send_group_sign", "params": {"group_id": group_id}}))
# class qqbot1:  # 这部分为http协议
#     def rev_msg(self):  # json or None
#         ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         ListenSocket.bind(('127.0.0.1', 5701))
#         ListenSocket.listen(100)
#         Client, Address = ListenSocket.accept()
#         Request = Client.recv(1024).decode(encoding='utf-8')
#         rev_json = request_to_json(Request)
#         Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
#         Client.close()
#         return rev_json
#
#     def send_msg(resp_dict):
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         ip = '127.0.0.1'
#         client.connect((ip, 5700))
#         msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
#         number = resp_dict['number']  # 回复账号（群号/好友号）
#         msg = resp_dict['msg']  # 要回复的消息
#         # 将字符中的特殊字符进行url编码
#         msg = msg.replace(" ", "%20")
#         msg = msg.replace("\n", "%0a")
#         if msg_type == 'group':
#             payload = "GET /send_group_msg?group_id=" + str(
#                 number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
#         elif msg_type == 'private':
#             payload = "GET /send_private_msg?user_id=" + str(
#                 number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
#         print("发送" + payload)
#         client.send(payload.encode("utf-8"))
#         client.close()
#         return 0
