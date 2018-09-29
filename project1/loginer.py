#coding=utf-8

#Author: Jiangtian
#Create Date:2018/07/30
#Last Edited:2018/07/30

#登录到NGA论坛。

from selenium import webdriver
import urllib
import time
import mailer
from PIL import Image

account_id = '_江天万里霜_'
account_password = ''

def login(bs):
    #bs = webdriver.Chrome()
    bs.set_window_size(1366,768)                        #设置浏览器尺寸为1366*768
    bs.get("https://bbs.ngacn.cc/")                     #定位到nga首页
    time.sleep(3)                                       #睡眠3秒以加载页面
    bs.find_element_by_link_text("登录").click()        #点击登录按钮
    time.sleep(4)                                       #睡眠4秒以加载登录界面框架
    loginframe = bs.find_element_by_tag_name('iframe')  #定位登录界面框架
    bs.switch_to_frame(loginframe)
    bs.switch_to_frame(bs.find_element_by_id('iff'))
    inputname = bs.find_element_by_id('name')           #寻找输入框
    inputpassword = bs.find_element_by_id('password')
    inputname.send_keys(account_id)
    inputpassword.send_keys(account_password)
    login = bs.find_element_by_link_text("登 录")       #寻找登录按钮
    login.click()                                       #并点击
    #截屏获取验证码图片
    time.sleep(1)#睡眠1秒加载验证码
    bs.get_screenshot_as_file('captcha.png')
    captchaimage = Image.open('captcha.png')
    captchaimage = captchaimage.crop((300, 50, 1000, 200))
    captchaimage.save('captcha.png')
    #    picture = bs.find_element_by_tag_name('img')
    #    picture_url = picture.get_attribute('src')
    #    data = urllib.request.urlopen(picture_url).read()
    #    with open('captcha.png', 'wb') as f:
    #        f.write(data)

    #将验证码图片发送给指定邮箱
    mailer.send_image('452198708@qq.com','NGA自动登录验证码','无标题')

    captcha = input('输入验证码：')                                   #输入验证码
    inputcaptcha = bs.find_element_by_xpath("//*[@placeholder='输入图形验证码以继续']")
    inputcaptcha.send_keys(captcha)
    login = bs.find_element_by_link_text("继 续")
    login.click()                                       #登录
    time.sleep(5)                                       
    bs.switch_to_alert().accept()                       #取消掉提示弹窗，并返回bs状态
    return bs
