#coding=utf-8

#Author: Jiangtian
#Create Date:2018/08/03
#Last Edited:2018/08/04

#从刀区精华区的帖子列表中获取精品贴，并生成供版头使用的文本。因泥潭未登录时访问页面会经跳转，还是使用selenium实现

from selenium import webdriver
import poster

def removetags(text):    #去掉tag
    while text.find('[') != -1:
        bra = text.find('[')
        ket = text.find(']')
        text = text[:bra] + text[(ket+1):]
    if text[0] == ' ':
        text = text[1:]
    return text


def watchdog(bs): #判断精品贴的内容是否发生变化。如果精品贴的内容不变，返回0；否则返回变化后的文本，
                #并分别存入essence.txt、farmdepartment.txt、reddit.txt
    bs.get('http://bbs.ngacn.cc/thread.php?&recommend=1&fid=321&order_by=postdatedesc')

    
    with open ('lastpost.txt', 'r', encoding='utf-8') as f:
        lastpost = f.read()
    elements = bs.find_elements_by_class_name('topic')

    if elements[0].text == lastpost:    #如果第一项没有变化，则直接返回0，退出函数
        return 0
    
    #如果否的话再更新内容
    with open ('essence.txt', 'r', encoding='utf-8') as f:
        jingpin = f.read().split('split')
    with open ('farmdepartment.txt', 'r', encoding='utf-8') as f:
        famubu = f.read().split('split')
    with open ('reddit.txt', 'r', encoding='utf-8') as f:
        hongdiwang = f.read().split('split')

    topic = []
    for i in elements:
        topic.append([i.text, i.get_attribute('href')]) #将帖子标题和url赋到list topic里

    #寻找lastpost在topic中的位置，来裁剪topic；然后再把topic的第一项赋给lastpost.txt
    lpplace = -1
    for i in range(len(topic)):
        if topic[i][0] == lastpost:
            lpplace = i
            break
    topic = topic[:lpplace]
    with open ('lastpost.txt', 'w', encoding='utf-8') as f:
        f.write(topic[0][0])

    #然后将topic倒序，从旧往新开始更新内容
    #先初始化开关和内容
    switch1 = 0
    switch2 = 0
    switch3 = 0
    text1 = ''
    text2 = ''
    text3 = ''
    topic.reverse()
    for i in topic:
        if (i[0].find('reddit周报') != -1) | (i[0].find('Reddit周报') != -1):    #如果是红迪网周报
            processedurl = i[1].split('http://bbs.ngacn.cc')[1]
            processedcon = i[0][(i[0].find('eddit周报')+12):(i[0].find('eddit周报')+14)] #期数为两位数，在100期之后会发生问题……管他的，100期之后这玩意还有没有用都说不定了呢
            addtext = '[url={}][b]第{}期[/b][/url]'.format(processedurl, processedcon)
            hongdiwang.insert(0, addtext)
            hongdiwang.pop(-1)
            switch1 = 1
        elif i[0].find('阀木部') != -1:    #如果是阀木部相关帖子
            processedurl = i[1].split('http://bbs.ngacn.cc')[1]
            processedcon = removetags(i[0])
            addtext = '[url={}][b]{}[/b][/url]'.format(processedurl, processedcon)
            famubu.insert(0, addtext)
            famubu.pop(-1)
            switch2 = 1
        else:   #如果是一般的精品贴
            processedurl = i[1].split('http://bbs.ngacn.cc')[1]
            processedcon = removetags(i[0])
            addtext = '[url={}][b]{}[/b][/url]'.format(processedurl, processedcon)
            jingpin.insert(0, addtext)
            jingpin.pop(-1)
            switch3 = 1

    if switch1 == 1:#自动更新标记放在[size=140%][color=red][b]NEW！[/b][/color][/size]后面
        text1 = '[size=120%]{st1}[/size]\n[size=110%]{nd2}[/size]\n[size=100%]{rd3}[/size]\n[/align][align=center]{th4} {th5} {th6} {th7} {th8} {th9} {th10}[/align]'.format(st1=hongdiwang[0], nd2=hongdiwang[1], rd3=hongdiwang[2], th4=hongdiwang[3], th5=hongdiwang[4], th6=hongdiwang[5], th7=hongdiwang[6], th8=hongdiwang[7], th9=hongdiwang[8], th10=hongdiwang[9])
        #和[align=right][pid=265787209][b]更多节奏盘点[/b][/pid][/align][/td]前面
        with open ('reddit.txt', 'w', encoding='utf-8') as f:
            f.write('split'.join(hongdiwang))

    if switch2 == 1:#标记放在[l]后面和[/l]前面
        text2 = '[list]\n[*]{st1}[color=red]~new~[/color]\n[*]{st2}[color=red]~new~[/color]\n[*]{st3}[color=red]~new~[/color]\n[*]{st4}\n[*]{st5}\n[*]{st6}\n[*]{st7}\n[/list]'.format(st1=famubu[0], st2=famubu[1], st3=famubu[2], st4=famubu[3], st5=famubu[4], st6=famubu[5], st7=famubu[6])
        with open ('farmdepartment.txt', 'w', encoding='utf-8') as f:
            f.write('split'.join(famubu))

    if switch3 == 1:#标记放在[/h]后面和[/td]前面
        text3 = '[list]\n[*]{st1}\n[*]{st2}\n[*]{st3}\n[*]{st4}\n[*]{st5}\n[*]{st6}\n[*]{st7}\n[/list]'.format(st1=jingpin[0], st2=jingpin[1], st3=jingpin[2], st4=jingpin[3], st5=jingpin[4], st6=jingpin[5], st7=jingpin[6])
        with open ('essence.txt', 'w', encoding='utf-8') as f:
            f.write('split'.join(jingpin))
            
    return [text1, text2, text3]
    
