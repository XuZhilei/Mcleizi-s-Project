#coding=utf-8

#Author: Jiangtian
#Create Date:2018/08/06
#Last Edited:2018/08/06

#在进程意外结束之后发送提示邮件至指定的邮箱。需要和shell脚本配合食用

import mailer

mailer.send_email('452198708@qq.com', '主进程意外结束',"主进程意外结束")