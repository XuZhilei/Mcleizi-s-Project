# -*- coding: utf-8 -*-
import argparse
import logging
import os
import socket
import sys
import threading
import time
import random
import requests
import json

from six import PY2
from six import iteritems

from smart_qq_bot.config import COOKIE_FILE
from smart_qq_bot.logger import logger
from smart_qq_bot.app import bot, plugin_manager
from smart_qq_bot.handler import MessageObserver
from smart_qq_bot.messages import mk_msg
from smart_qq_bot.excpetions import ServerResponseEmpty, NeedRelogin
from smart_qq_bot.signals import bot_inited_registry


def patch():
    if PY2:
        reload(sys)
        sys.setdefaultencoding("utf-8")


def clean_cookie():
    if os.path.isfile(COOKIE_FILE):
        os.remove(COOKIE_FILE)
    logger.info("Cookie file removed.")


def run_http_daemon(host="0.0.0.0", port=8888):
    from threading import Thread
    from smart_qq_bot.httpserver import run_server
    daemon = Thread(
        target=run_server,
        kwargs={"host": host, "port": port}
    )
    daemon.setDaemon(True)
    daemon.start()

def construct_virtual_msg_list(text):
    return [
        {
            'poll_type': 'group_message',
            'value': {
                'content': [
                    ['font', {
                    'color': '000000',
                    'name': '微软雅黑',
                    'size': '10',
                    'style': [0, 0, 0]
                }
                ],
                text
                ],
                'from_uin': 469935712,
                'group_code': 469935712,
                'msg_id': random.randint(1000,9999),
                'msg_type': 4,
                'send_uin': 705672773,
                'time': time.time(),
                'to_uin': 3309095738
            }
        }
    ]

def main_loop(no_gui=False, new_user=False, debug=False, http=False):
    patch()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if http:
        run_http_daemon()
    logger.info("Initializing...")
    plugin_manager.load_plugin()
    if new_user:
        clean_cookie()
    bot.login(no_gui)
    observer = MessageObserver(bot)

    for name, func in iteritems(bot_inited_registry):
        try:
            t = threading.Thread(target=func, args=(bot,))
            t.daemon = True
            t.start()
        except Exception:
            logging.exception(
                "Error occurs while loading plugin [%s]." % name
            )

    #lock = threading.Lock()
    #thisgroupcode = 0

    def monitorLoop():  #监听消息用的循环，用以实现被动回复消息
        while True:
            try:
                msg_list = bot.check_msg()
                if msg_list is not None:
                    print('msg_list = {}'.format(msg_list))
                    observer.handle_msg_list(
                        [mk_msg(msg, bot) for msg in msg_list]
                    )
            except ServerResponseEmpty:
                continue
            except (socket.timeout, IOError):
                logger.warning("Message pooling timeout, retrying...")
            except NeedRelogin:
                exit(0)
            except Exception:
                logger.exception("Exception occurs when checking msg.")

    def initiativeLoop():   #主动发送消息用的循环。
        secretaryship = 346 #秘书舰的ID。346：照月改
        #timecode = 1 #1号是登录语音
        #r = requests.get('http://api.kcwiki.moe/subtitles/' + str(secretaryship))
        #r = json.loads(r.text)
        #baoshitext = r[str(timecode)]
        #try:
        #    bot.send_group_msg(baoshitext, thisgroupcode, random.randint(1000,9999), 0)
        #except:
        #    logger.warning("There is a Error")

        while True:
            print('initiativeLoop is running, time = {}...'.format(time.time()%3600))
            if time.time() % 3600 <= 60:    #如果时间为整点的话就报时
                timecode = time.localtime(time.time()).tm_hour + 30 #30号语音是零点
                r = requests.get('http://api.kcwiki.moe/subtitles/' + str(secretaryship))
                r = json.loads(r.text)
                baoshitext = r[str(timecode)]
                try:
                    bot.send_group_msg(baoshitext, thisgroupcode, random.randint(1000,9999), 0)
                except:
                    logger.warning("There is a Error")
            elif random.randint(1,10000) <= 50: #每分钟有0.5%的概率触发放置语音
                timecode = random.choice([29, 28, 2, 3, 4]) #29号是放置语音
                r = requests.get('http://api.kcwiki.moe/subtitles/' + str(secretaryship))
                r = json.loads(r.text)
                baoshitext = r[str(timecode)]
                try:
                    bot.send_group_msg(baoshitext, thisgroupcode, random.randint(1000,9999), 0)
                except:
                    logger.warning("There is a Error")
            time.sleep(60)

    def twitterMonitorLoop():   #监听官推用的循环
        with open ('tweetid.txt', 'r') as f:
            lasttweet = json.loads(f.read())
            print('Initializing tweets. load tweet as {}'.format(lasttweet))

        while True:
            tweetcontent = ''
            rt = requests.get('http://api.kcwiki.moe/tweet/plain/5')
            rt = json.loads(rt.text)
            if lasttweet == rt: #如果官推没有更新过
                logger.info('No new tweet. last tweet id = {}'.format(rt[0]['id']))
                time.sleep(60)
            else:
                for i in rt:
                    if i['id'] not in [j['id'] for j in lasttweet]:
                        tweetcontent = i['jp'] + '\n' + i['date']
                        logger.info('Sent a tweet, id = {}'.format(i['id']))
                        bot.send_group_msg(tweetcontent, thisgroupcode, random.randint(1000,9999), 0)
                with open ('tweetid.txt', 'w') as f:
                    f.write(json.dumps(rt))
                lasttweet = rt
                time.sleep(60)

    grouplist = bot.get_group_list_with_group_code()
    print ('grouplist = {}'.format(grouplist))
    for i in grouplist: 
        if i['name'] == 'USTC舰狗聚众斗欧':
            thisgroupcode = i['gid']
            print('thisgroupcode = {}'.format(thisgroupcode))

    t2 = threading.Thread(target=monitorLoop)
    t2.start()
    t3 = threading.Thread(target=twitterMonitorLoop)
    t3.start()
    initiativeLoop()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-gui",
        action="store_true",
        default=False,
        help="Whether display QRCode with tk and PIL."
    )
    parser.add_argument(
        "--http",
        action="store_true",
        default=False,
        help="Whether launch a bottle server to serve qrcode."
    )
    parser.add_argument(
        "--new-user",
        action="store_true",
        default=False,
        help="Logout old user first(by clean the cookie file.)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Switch to DEBUG mode for better view of requests and responses."
    )
    args = parser.parse_args()
    main_loop(**vars(args))


if __name__ == "__main__":
    run()
