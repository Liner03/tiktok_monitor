# coding:utf-8
import re
import json
import requests
import push
HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}
#获取真实302地址
def get_real_address(url):
    if url.find('v.douyin.com') < 0:
        return url
    res = requests.get(url, headers=HEADERS, allow_redirects=False)
    newurl = res.headers['Location'] if res.status_code == 302 else None
    return newurl
#正则真实地址获取ID
def realurl(newurl):
    pattern = re.compile(r'sec_uid=(?P<id>.*?)&')
    ree = pattern.finditer(newurl)
    for i in ree:
        return i.group("id")
        break
#拼接抖音信息api
def dyapi(dyid):
    dyapi = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid="+dyid
    ua = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"
    }
    # dyapi = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAAQ-oSJJwR54bQTUvYOptncJXLJ-eF_rjFfcFMYCFND32K8imBbMv2E-Oc7GD5NAG8"
    response = requests.get(dyapi,headers=ua)
    content = json.loads(response.text)

    douyin_info = {}
    # 获取昵称
    douyin_info['昵称'] = content["user_info"]["nickname"]
    douyin_info['ID'] = content["user_info"]["short_id"]
    # 关注的用户数
    douyin_info['关注数'] = content["user_info"]["following_count"]
    # 作品数
    douyin_info['作品数'] = content["user_info"]["aweme_count"]
    # 喜欢

    douyin_info['喜欢'] = content["user_info"]["favoriting_count"]
    # 粉丝

    douyin_info['粉丝数'] = content["user_info"]["follower_count"]

    # 点赞

    douyin_info['获赞数'] = content["user_info"]["total_favorited"]


    return douyin_info


if __name__ == '__main__':
    url = 'https://v.douyin.com/FY1Aj6u/'
    url = get_real_address(url)
    url = realurl(url)
    # print(url)
    json2 = dyapi(url)


file = open('1.json','r',encoding='utf-8')
oldjson= json.load(file)
gz = int(oldjson['关注数']);like =int(oldjson['喜欢']) ; work = int(oldjson['作品数'] ); fan = int(oldjson['粉丝数']) ;
gz1 = int(json2['关注数']) ; like1 =int(json2['喜欢']) ; work1 = int(json2['作品数']) ; fan1 = int(json2['粉丝数']) ;

if (oldjson == json2):
    print('无变动')
else:
    bd = {}
    bd['关注新增'] = (gz1 - gz)
    bd['喜欢新增'] = (like1 - like)
    bd['作品新增'] = (work1 - work)
    bd['粉丝新增'] = (fan1 - fan)
    if (bd['关注新增']> 0):
        mail_msg1 = "关注了" + str(bd['关注新增']) + '个人'+ str(bd['关注新增']) + '分'

    elif (bd['关注新增'] < 0):
        mail_msg1 = "取关了"+str(abs(bd['关注新增']))+'个人' + str(abs(bd['关注新增'])) + '分耶'
    else :
        mail_msg1='关注无新增'
        print("没有变动")

    if (bd['喜欢新增'] > 0):
        mail_msg2 = '喜欢了别人的作品' + str(bd['喜欢新增']) + '分'

    elif (bd['喜欢新增'] < 0):
        mail_msg2 = '讨厌了别人的作品' + str(abs(bd['喜欢新增'])) + '分耶'
    else:
        mail_msg2 = '喜欢无新增'
        print("没有变动")

    if (bd['作品新增'] > 0):
        mail_msg3 = "发布了" + str(bd['作品新增']) + '个新作品'

    elif (bd['作品新增'] < 0):
        mail_msg3 = "删除了" + str(abs(bd['作品新增'])) + '个作品'
    else:
        mail_msg3 = '作品无新增'
        print("没有变动")

    if (bd['粉丝新增'] > 0):
        mail_msg4 = '多了' + str(bd['粉丝新增']) + '个粉丝' + str(bd['粉丝新增']) + '位呢'

    elif (bd['粉丝新增'] < 0):
        mail_msg4 = '少了' + str(abs(bd['粉丝新增'])) + '个粉丝' + str(abs(bd['粉丝新增'])) + '位耶'
    else:
        mail_msg4 = '粉丝无新增'
        print('没有变动')
    mail_msg5 = str(json2)
    mail_msg = mail_msg1+'\n'+'\n'+ mail_msg2+'\n'+'\n'+mail_msg3+'\n'+'\n'+mail_msg4+'\n'+'\n'+mail_msg5
    print(mail_msg)
    if mail_msg == "无变动":
        pass
    else:
        push = push.WXPusher(usr='User', msg=mail_msg)       # usr参数为推送用户名，msg为消息文本  usr为@all时是推送全体成员
        push.send_message()
        # 发信
    json_info = json2
    file = open('1.json', 'w', encoding='utf-8')
    json.dump(json_info, file)
    file.close()
