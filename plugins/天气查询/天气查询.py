import configparser
import tkinter

name = '天气查询'
import requests

# from sdk import Bot
conf = configparser.ConfigParser()
conf.read('./data/天气查询/conf.ini')
key1 = conf.get('main', 'key')  # 心知天气私钥
rev = {}
gp_id = 0
qqbot = None
complain = '查询天气'


def init(p_id: int, Api: object):  # 插件第一次安装时调用
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    return {'name': name, 'complain': complain, 'author': 'None', 'ver': '0.1', 'p_id': p_id, 'respond_group_msg': True,
            'respond_private_msg': True, 'respond_notice': False, 'respond_request': False}


def enable():  # 插件被启用时被调用
    pass


qq = list()


def on_private_msg(dic):
    global qq
    if dic['message'] == 'raw_message':
        global rev
        rev = dic
        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '请发送一个城市'})
        qq.append(dic['user_id'])
    elif dic['user_id'] in qq:
        qq.remove(dic['user_id'])
        url = 'https://api.seniverse.com/v3/weather/now.json?key={0}&location={1}&language=zh-Hans&unit=c'.format(
            key1,
            dic['message'])
        res = requests.get(url).json()
        fin = res['results'][0]['location']["path"] + '\n' + res['results'][0]['now']['text'] + '\n' + \
              res['results'][0]['now']['temperature'] + '摄氏度'
        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': fin}, delay=1)


def on_group_msg(dic):
    if dic['raw_message'] == '天气查询':
        global rev
        rev = dic
        qqbot.send_group_msg(dic['group_id'], '请发送城市', delay=0.9)
        global qq
        qq.append(dic['user_id'])
    elif dic['user_id'] in qq:
        qq.remove(dic['user_id'])
        url = 'https://api.seniverse.com/v3/weather/now.json?key={0}&location={1}&language=zh-Hans&unit=c'.format(
            key1,
            dic['raw_message'])
        res = requests.get(url).json()
        # print(res)
        fin = res['results'][0]['location']["path"] + '\n' + res['results'][0]['now']['text'] + '\n' + \
              res['results'][0]['now']['temperature'] + '摄氏度'
        qqbot.send_group_msg(dic['group_id'], fin, delay=2)


def on_notice(dic):
    pass


def disable():
    pass


def setting():
    tk = tkinter.Tk()
    tk.geometry('300x200')
    tk.title('天气查询')
    tkinter.Label(tk, text='key').pack()
    e = tkinter.Entry(tk)
    e.pack()
    e.insert(0, key1)

    def writting_config():
        conf['main']['key'] = e.get()
        with open('conf.ini', 'w') as f:
            conf.write(f)

    b = tkinter.Button(text='保存', command=writting_config)
    b.pack()
    tk.mainloop()


if __name__ == '__main__':
    key1 = "SO-owjXNal9_usfNs"
    url_ = 'https://api.seniverse.com/v3/weather/now.json?key={0}&location={1}&language=zh-Hans&unit=c'.format(
        key1,
        "北京")
    print(requests.get(url_).json())
