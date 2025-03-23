from threading import Thread

from Plugin import Plugin

# import traceback
# from pybot import qqbot
plu_dic = list()  # list[Plugin]
Api = object
last_message_id = 0


def mainloop(qqbot, ui):
    # print(1)
    while True:
        rev = qqbot.rev_msg()
        # print(rev)
        if not rev:
            break
        if rev.get('message_type') == 'group':
            ui.s.sendmsg.emit({'type': 'recv_group_message', 'sender': '框架', 'text': str(rev)})
            for i in plu_dic:
                if i.respond_group_msg and i.enable and i.if_groupMsg:
                    t = Thread(target=i.on_group_msg, args=(rev,))
                    t.start()
        elif rev.get('message_type') == 'private':
            ui.s.sendmsg.emit({'type': 'recv_private_message', 'sender': '框架', 'text': str(rev)})
            for i in plu_dic:
                if i.respond_private_msg and i.enable and i.if_privateMsg:
                    t = Thread(target=i.on_private_msg, args=(rev,))
                    t.start()
        elif rev.get('post_type') == 'notice':
            ui.s.sendmsg.emit({'type': 'info', 'sender': '收到消息', 'text': str(rev)})
            for i in plu_dic:
                if i.respond_notice and i.enable and i.if_notice:
                    t = Thread(target=i.on_notice, args=(rev,))
                    t.start()
        elif rev.get('post_type') == 'request':
            ui.s.sendmsg.emit({'type': 'info', 'sender': '收到request', 'text': str(rev)})
            for i in plu_dic:
                if i.respond_request and i.enable:
                    t = Thread(target=i.on_request, args=(rev,))
                    t.start()
        elif rev.get('post_type') == 'meta_event' and rev.get("meta_event_type") == 'heartbeat':
            if rev.get('heartbeat'):
                if rev.get('status') == 'good':
                    pass
        elif rev.get('status'):  # 发送消息的返回值
            if rev.get('data'):
                global last_message_id
                last_message_id = rev.get('data')['message_id']

        else:
            ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': str(rev)})
    # print(1)


def loop_recv(qqbot):
    # print(2)
    while True:
        rev = qqbot.rev_msg()
        if rev is None:
            continue
        elif "message_type" not in rev:
            print("looprecv", rev)

        else:
            print('rev', rev)
            qqbot.recv_queue.put(rev)


def send_msg_thread(qqbot):
    while 1:
        t = qqbot.send_queue.get()
        if not t:
            break
        # print('send', t)
        qqbot.connection.send(t)


# def send_msg_thread(qqbot):
#     while 1:
#         # print(qqbot.recv_queue)
#         t = qqbot.send_queue.get()
#         if not t:
#             break
#         # print('t', t)
#         print('send', t)
#         qqbot.connection.send(t)


def deliver_msg(ui, plu_dic_, qqbot, BotApi):  # 启动消息分发线程
    global plu_dic
    global Api
    Api = BotApi
    plu_dic = plu_dic_
    if qqbot is None:
        ui.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '注意，没有链接到gocq，将不会接受和处理消息'})
    else:
        # t = Thread(target=loop_recv, daemon=True, args=(qqbot,))
        # t.start()
        t1 = Thread(target=mainloop, daemon=True, args=(qqbot, ui))
        t1.start()
        t2 = Thread(target=send_msg_thread, daemon=True, args=(qqbot,))
        t2.start()


def enable_plugin(pid):
    for i in plu_dic:
        if i.pid == pid:
            i.is_enable = True
            i.enable_func(Api=Api, p_id=pid)
    return


def disable_plugin(pid):
    for i in plu_dic:
        if i.pid == pid:
            i.is_enable = False
            i.disable_func()
    return


def setPlugin(pid: int):
    for i in plu_dic:
        if i.pid == pid:
            i.is_enable = True
            i.setting()


def del_plugin(plugin: Plugin):
    plu_dic.remove(plugin)
