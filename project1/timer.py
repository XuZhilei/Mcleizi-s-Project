#coding=utf-8

#Author: Jiangtian
#Create Date:2018/07/30
#Last Edited:2018/08/06

#主程序，以及计时器

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import heropick
import loginer
import poster
import time
import mailer
import essence
import countdown
import bonus
#import gameplay_mainevent
#import prizepool

def shijian():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def main(): 
    #初始化webdriver
    chrome_options = Options()
    chrome_options.add_argument('window-size=1366x768') #指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.add_argument('--no-sandbox') #root用户需要在此属性下运行

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = loginer.login(driver)

    #这里是需要编辑的帖子URL。
    bantou = 'http://bbs.ngacn.cc/post.php?action=modify&_newui&fid=321&tid=13537753&pid=0&article=0'
    #http://bbs.ngacn.cc/post.php?action=modify&_newui&fid=321&tid=13537753&pid=0&article=0
    #zhuanti = 'https://bbs.ngacn.cc/post.php?action=modify&_newui&fid=321&tid=14599412&pid=0&article=0'
    bantou = 'https://bbs.nga.cn/post.php?action=modify&_newui&fid=-10323371&tid=15206099&pid=0&article=0'

    while True:#主循环
        #####################################
        #          以下内容为通用部分
        #  #记录本次循环开始的时间戳
        isposter = False#初始化发帖开关
        unixtime = time.time()
        if poster.hasLogined(driver) == False:  #如果登录失效的话重新登录，并发送提醒邮件
            mailer.send_email('452198708@qq.com', '登录已失效，请重新登录',("登录失效于:{}".format(shijian())))
            input('登录已失效，请重新登录。按任意键继续...')    #等待确认后再进行登录操作，以免验证码过期
            driver = loginer.login(driver)
        #
        #####################################
        oldtext = poster.viewer(driver, bantou) #获取原先的帖子内容。

        if True:  #每小时读取一次精品区
            essencejudgment = essence.watchdog(driver)  #读精品区帖子内容
            if essencejudgment != 0:   #如果精品区帖子改变了就处理新的精品区。
                [newtext2, newtext3, newtext4] = essencejudgment
                if newtext2 != '':
                    oldtext = poster.replace_content(oldtext, newtext2, 2)
                if newtext3 != '':
                    oldtext = poster.replace_content(oldtext, newtext3, 3)
                if newtext4 != '':
                    oldtext = poster.replace_content(oldtext, newtext4, 4)
                    #oldtext = poster.replace_content(oldtext, newtext4, 6)  #TI特供版

            #并且每小时更新一次倒计时
            #oldtext = poster.replace_content(oldtext, '[size=200%][color=red]{}[/color][/size]天[size=200%][color=red]{}[/color][/size]小时'.format(countdown.run()[0], countdown.run()[1]), 5)
                isposter = True
                print('every hour update essence and countdown')
            

        #if False:#(time.localtime().tm_min % 5) == 1: #每分钟读取一次赛事信息，以及奖金
        #    print ('start to update gameplay')
        #    gameplay_mainevent.catch()
        #    gametext = gameplay_mainevent.writeformat(0)
        #    #ranktext = gameplay.writeformat(2)
        #    oldtext = poster.replace_content(oldtext, gametext, 7)
        #    #oldtext = poster.replace_content(oldtext, ranktext, 0)
        #    prizetext = prizepool.run()
        #    oldtext = poster.replace_content(oldtext, str(prizetext), 8)
        #    isposter = True
        #    print ('updated gameplay')

        if time.localtime().tm_hour == 4:       #每天凌晨4时抓取新的heropick数据。
            newtext = heropick.run()
            print (newtext)
            oldtext = poster.replace_content(oldtext, newtext, 1)
            isposter = True
            print ('update heropick')

        if time.localtime().tm_hour == 12:      #每天中午12点更新本日奖励英雄。
            newtext = bonus.run()
            print (newtext)
            oldtext = poster.replace_content(oldtext, newtext, 8)
            isposter = True
            print ('update bonus hero')

            
        #if essence.judgment():
        #    poster.poster(driver, essence.run)
        if isposter == True:
            timestr = str(time.time())
            with open ('post-' + timestr, 'w') as f:
                f.write(oldtext)
            poster.poster(driver, oldtext, bantou)

        #if isposter == True:    #如果发帖开关被打开了就保存一份修改记录到本地。###不保存了，都搞出MemoryError了
        #    with open ('logger.txt', 'r+', encoding='utf-8') as f:
        #        f.write(f.read() + '\n\n\n\n###################################\n\n    {}\n\n{}\n'.format(shijian(), oldtext))
        
        #编辑专题贴 不编辑了，手动啦
        #oldtext = poster.viewer(driver, zhuanti) #获取原先的帖子内容。
        #newtext = gameplay_mainevent.writeformat(1)
        #oldtext = poster.replace_content(oldtext, newtext, 9)
        #poster.poster(driver, oldtext, zhuanti)

        print("last check:{}".format(shijian()))
        
        time.sleep(3600 - (time.time() - unixtime))   #睡眠时间为3600秒减去本次循环耗费的时间，以保证每个循环用时为1h整

main()
