#coding=utf-8

#Author: Jiangtian
#Create Date:2018/07/30
#Last Edited:2018/08/03

#发帖模块，获取帖子内容的模块，以及判断登录的模块

from selenium import webdriver
import urllib
import time
import loginer


def hasLogined(bs):     #判断是否登录成功。其实这个应该放在loginer里吧
    bs.get("https://bbs.ngacn.cc/read.php?tid=14613314")
    time.sleep(33)	#sleeping for 33s to jump over ad
    try:                #如果登录成功能够进入浏览帖子的页面，应该可以搜索到“登出”按钮
        element = bs.find_element_by_link_text("登出")
        return True     #如果正常地搜索到了这个按钮，说明处在登录状态下，返回True
    except: 
        return False     #否则一律返回False

def replace_content(oldcontent, replacetext, numofplace): #替换部分帖子内容。将需要替换的部分放在下面的字段内。
    startplace = oldcontent.find('[size=0%]自动编辑内容起始{}[/size]'.format(numofplace))
    endplace = oldcontent.find('[size=0%]自动编辑内容结束{}[/size]'.format(numofplace))
    return (oldcontent[0:(startplace+25)] + replacetext + oldcontent[endplace:])

def viewer(bs, url): #浏览帖子内容。
    bs.get(url)
    content_area = bs.find_element_by_name('post_content')  #抓取帖子原本的内容
    return (content_area.get_attribute('value'))

def poster(bs, postcontent, url):     #自动编辑帖子内容。在调用之前需要使用hasLogined函数确认登录状态；
    bs.get(url)
    content_area = bs.find_element_by_name('post_content')  #抓取帖子原本的内容
    content_area.clear()                #清空发帖框
    content_area.send_keys(postcontent) #并将新的内容填入
    bs.find_element_by_link_text("提 交(Ctrl+Enter)").click()
    #time.sleep(6)           #发布帖子后5秒自动跳转，留出1秒的等待响应时间
    bs.refresh()    #发布帖子后刷新 
    print("posted a tiezi to {}", url)
    return bs
