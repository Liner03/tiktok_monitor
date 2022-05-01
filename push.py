# 搭建教程可参考 https://github.com/easychen/wecomchan

# coding:utf-8


import requests
import json


class WXPusher:
    def __init__(self, usr, msg):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.corpid = ''     # 你的企业ID
        self.corpsecret = ''     # 你的Secret
        self.agentid = 1000002         # 填写你的企业ID，不加引号，是个整型常数,就是上图的AgentId
        self.usr = usr
        self.msg = msg

    def get_access_token(self):
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(self):
        data = self.get_message()
        req_urls = self.req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(self):
        data = {
            "touser": self.usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": self.msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data
