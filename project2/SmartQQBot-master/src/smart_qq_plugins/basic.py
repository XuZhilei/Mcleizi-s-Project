# -*- coding: utf-8 -*-
import random
import re
import time
import json
import requests

from smart_qq_bot.logger import logger
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_discuss_message,
)

# =====唤出插件=====

# 机器人连续回复相同消息时可能会出现
# 服务器响应成功,但实际并没有发送成功的现象
# 所以尝试通过随机后缀来尽量避免这一问题
REPLY_SUFFIX = (
    '~',
    '!',
    '?',
    '||',
)

initialized_playerinfo = {
            'resource': 0,
            'ships': []
}

def ship_construction(resourceamount):
    destoryer_pool = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,93,94,95,96,97,98,122,132,133,134,135,164,165,167,168,169,170]
    light_cruiser_pool = [21,22,23,24,25,51,52,53,54,55,56,99,100,101,113,114,115]
    heavy_cruiser_pool = [59,60,61,62,63,64,65,66,67,68,69,70,71,72,120,123,124,125]
    battleship_pool = [26,27,77,78,79,80,81,85,86,87]
    carrier_pool = [74,74,74,74,75,75,75,76,76,76,83,84,90,90,91,91,92,92,92,89,89,89,89,102,102,102,102,103,103,103,103,110,111,116]
    submarine_pool = [126,127,128,191]
    others_pool = []
    special_pool = [6655,9999]

    def function(x, arg):
        if arg == -1:   #upper is ceiling
            returnvar = 1
        if arg == 0:    #upper is special pool
            returnvar = 0.99
        elif arg == 1:  #upper is others pool
            returnvar = 0.98
        else:
            if arg == 2:  #upper is destroyer pool
                returnvar = (-0.0000012222222222222213*x*x+0.002277777777777778*x-0.015555555555555555)
            elif arg == 3: #upper is light cruiser pool
                returnvar = (-0.0000012222222222222221*x*x+0.0031*x-0.72)
            elif arg == 4: #upper is heavy cruiser pool
                returnvar = (0.0013333333333333333*x-0.5333333333333333)
            elif arg == 5: #upper is battleship pool
                returnvar = (0.0000033333333333333333*x*x-0.004*x+1.1666666666666667)
            elif arg == 6: #upper is carrier pool
                returnvar = 0
            if returnvar > 0.98:
                returnvar = 0.98
            elif returnvar < 0:
                returnvar = 0
        return returnvar
    
    #select pool
    randomseed = random.random()
    pool = [0]  #initial pool
    if randomseed > function(resourceamount, 0):
        pool = special_pool
    elif randomseed > function(resourceamount, 1):
        pool = submarine_pool
    elif randomseed > function(resourceamount, 2):
        pool = destoryer_pool
    elif randomseed > function(resourceamount, 3):
        pool = light_cruiser_pool
    elif randomseed > function(resourceamount, 4):
        pool = heavy_cruiser_pool
    elif randomseed > function(resourceamount, 5):
        pool = battleship_pool
    elif randomseed > function(resourceamount, 6):
        pool = carrier_pool
    construction_result = random.choice(pool)
    if construction_result == 6655:
        return {
            'ship_name': '鸭子 ywwuyi',
            'get_voice': '你醒了，提督，你家米缸已经空了哦！'
        }
    elif construction_result == 9999:
        return {
            'shipname': '冲锋枪 UMP45',
            'get_voice': 'UMP45，来了哦。指挥官，你是想和我好好相处的，对吗♪'
        }
    elif construction_result == 0:
        return 0
    else:
        with open('shipinfo_utf8.json', 'r') as f:
            shipinfo = json.loads(f.read())
        for i in shipinfo:
            if construction_result == i['id']:
                shipname = i['stype_name'] + ' ' + i['name']
                break
        r = requests.get('http://api.kcwiki.moe/subtitles/' + str(construction_result))
        getvoice = json.loads(r.text)['1']
        return {
            'ship_name': shipname,
            'get_voice': getvoice
        }



@on_all_message(name='basic[callout]')
def callout(msg, bot):
    msgcontent = msg.content.split(' ')
    if msg.content == '谁是徐志雷':
        reply = bot.reply_msg(msg, return_function=True)
        logger.info("RUNTIMELOG " + str(msg.from_uin) + " calling me out, trying to reply....")
        reply_content = "是TI冠军！" #+ random.choice(REPLY_SUFFIX)
        reply(reply_content)

#所有的被动消息都放在basic里。
    if msgcontent[0] == '!查询':#re.match(r'!查询 *', msg.content):
        reply = bot.reply_msg(msg, return_function=True)
        reply_content = random.choice(['哇咔奶~', '希腊奶~'])
        reply(reply_content)

    if msgcontent[0] == '!决斗':#re.match(r'!决斗 *', msg.content):
        reply = bot.reply_msg(msg, return_function=True)
        sendercard = (msg.src_sender_card or msg.src_sender_name or '你')
        if len(msgcontent) >= 2:
            fightername = msgcontent[1]
            if random.random() <= 0.5:
                sendercard, fightername = fightername, sendercard
            if (time.localtime().tm_hour >= 19) & (time.localtime().tm_hour <= 20):
                reply_content = '{}在决斗中战胜了{}'.format(sendercard, fightername)
            else:
                reply_content = '决斗场只在每天19:00-21:00开放。'
        else:
            reply_content = '你必须先指定一个目标。'
        
        reply(reply_content)
    
    if msgcontent[0] == '!roll':#re.match(r'!roll *', msg.content):
        reply = bot.reply_msg(msg, return_function=True)
        reply_content = '你对{}掷出{}点。'.format(msg.content[6:], random.randint(0,100))
        reply(reply_content)
    
    if msg.content == '!签到':
        with open('online.txt', 'r') as f:
            playerinfo = json.loads(f.read())
        with open('qiandao.txt', 'r')as f:
            qiandaoinfo = json.loads(f.read())
        todaydate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        senderqq = msg.src_sender_name
        if senderqq not in playerinfo:
            playerinfo[senderqq] = initialized_playerinfo
        if todaydate not in qiandaoinfo:
            qiandaoinfo[todaydate] = []
        if senderqq not in qiandaoinfo[todaydate]:
            qiandaoinfo[todaydate].append(senderqq)
            playerinfo[senderqq]['resource'] += 500
            reply_content = '签到成功！你的资源增加了500。'
        else:
            reply_content = '你今天已经签到过了。你现在有{}资源和下列舰娘：\n{}'.format(playerinfo[senderqq]['resource'], [i['ship_name'] for i in playerinfo[senderqq]['ships']])
        with open('online.txt', 'w') as f:
            f.write(json.dumps(playerinfo))
        with open('qiandao.txt', 'w') as f:
            f.write(json.dumps(qiandaoinfo))
        reply = bot.reply_msg(msg, return_function=True)
        reply(reply_content)


    if msgcontent[0] == '!建造':
        with open('online.txt', 'r') as f:
            playerinfo = json.loads(f.read())

        senderqq = msg.src_sender_name

        if senderqq not in playerinfo:
            playerinfo[senderqq] = initialized_playerinfo
        if len(msgcontent) <= 1:
            resource_amount = 100
        else:
            try:
                resource_amount = int(msgcontent[1])
            except:
                resource_amount = 100

        if playerinfo[senderqq]['resource'] < resource_amount:
            reply_content = '你没有足够的资源。'
        elif resource_amount > 1000:
            reply_content = '普通建造的资源上限为1000。'
        elif resource_amount < 100:
            reply_content = '普通建造的资源下限为100。'
        else:
            playerinfo[senderqq]['resource'] -= resource_amount

            constructionresult = ship_construction(resource_amount)

            if constructionresult == 0:
                reply_content = '很抱歉，建造失败…'
            else:
                reply_content = '你使用{}资源建造出了：\n{}\n“{}”'.format(resource_amount, constructionresult['ship_name'], constructionresult['get_voice'])
                playerinfo[senderqq]['ships'].append(constructionresult)

        with open('online.txt', 'w') as f:
            f.write(json.dumps(playerinfo))

        reply = bot.reply_msg(msg, return_function=True)
        reply(reply_content)  

    if msg.content == '!大建':
        reply = bot.reply_msg(msg, return_function=True)
        reply_content = '你没有完成大建所需的任务。'
        reply(reply_content)

    if msg.content == '谁是B黑':
        reply = bot.reply_msg(msg, return_function=True)
        reply_content = '宇宙人'
        reply(reply_content)



# =====复读插件=====
class Recorder(object):
    def __init__(self):
        self.msg_list = list()
        self.last_reply = ""

recorder = Recorder()


@on_group_message(name='basic[repeat]')
def repeat(msg, bot):
    global recorder
    reply = bot.reply_msg(msg, return_function=True)

    if len(recorder.msg_list) > 0 and recorder.msg_list[-1].content == msg.content and recorder.last_reply != msg.content:
        if (str(msg.content).strip() not in ("", " ", "[图片]", "[表情]")):
            logger.info("RUNTIMELOG " + str(msg.group_code) + " repeating, trying to reply " + str(msg.content))
            reply(msg.content)
            recorder.last_reply = msg.content
    recorder.msg_list.append(msg)


@on_group_message(name='basic[三个问题]')
def nick_call(msg, bot):
    if "我是谁" == msg.content:
        bot.reply_msg(msg, "你是{}({})!".format(msg.src_sender_card or msg.src_sender_name, msg.src_sender_id))

    elif "我在哪" == msg.content:
        bot.reply_msg(msg, "你在{name}({id})!".format(name=msg.src_group_name, id=msg.src_group_id))

    elif msg.content in ("我在干什么", "我在做什么"):
        bot.reply_msg(msg, "你在调戏我!!")


@on_discuss_message(name='basic[讨论组三个问题]')
def discuss_three_questions(msg, bot):
    if "我是谁" == msg.content:
        bot.reply_msg(msg, "你是{}!".format(msg.src_sender_name))

    elif "我在哪" == msg.content:
        bot.reply_msg(msg, "你在{name}!".format(name=msg.src_discuss_name))

    elif msg.content in ("我在干什么", "我在做什么"):
        bot.reply_msg(msg, "你在调戏我!!")