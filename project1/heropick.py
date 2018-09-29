#coding=utf-8

#Author: Jiangtian
#Create Date:2018/07/30
#Last Edited:2018/09/29

#从dotamax网站获取今日/本周英雄的胜率和使用次数，并生成版头文本

from bs4 import BeautifulSoup
import requests
import datetime

class hero(object): #定义hero类用以存放数据
        def __init__(self, name, rate, number):
                self.name = name
                self.rate = rate
                self.number = number

def bubble_num(nums):   #按使用次数冒泡排序
	for i in range(len(nums) - 1):
		for j in range(len(nums) - i - 1):
			if int(nums[j].number.replace(',','')) > int(nums[j+1].number.replace(',','')):
				nums[j], nums[j+1] = nums[j+1], nums[j]
	return nums

def bubble_rate(nums):  #按胜率冒泡排序
	for i in range(len(nums) - 1):
		for j in range(len(nums) - i - 1):
			if float(nums[j].rate[0:-1]) > float(nums[j+1].rate[0:-1]):
				nums[j], nums[j+1] = nums[j+1], nums[j]
	return nums
    

def formatting(herolist):   #处理数据为所需的格式
    herolist = bubble_rate(herolist)
    herolist.reverse()
    herolist = herolist[:5] + herolist[-5:]
    newlastlist = []
    with open('lastlist','r', encoding='utf-8') as f:
        lastlist = f.read().split(',')
    outtext = "{}\n全球VH局数据\n[h][/h]\n".format(datetime.datetime.today().strftime('%Y-%m-%d'))
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if i == 5:
            outtext += '…\n'
        outtext += herolist[i].name + ' ' + herolist[i].rate + ' '
        newlastlist.append(herolist[i].name)
        if herolist[i].name in lastlist:
            rankchange = lastlist.index(herolist[i].name) - i
            if rankchange > 0:
                rankchange = "[color=red]↑{}[/color]".format(rankchange)
            elif rankchange < 0:
                rankchange = "[color=green]↓{}[/color]".format(-rankchange)
            else:
                rankchange = '-'
        else:
            rankchange = '[color=orange]New[/color]'
        outtext += rankchange + '\n'
    #outtext += "[/td][/align]\n[td][align=center]今日英雄黑榜\n{}[h][/h]\n".format(datetime.datetime.today().strftime('%Y-%m-%d'))
    '''
    for i in [-5, -4, -3, -2, -1]:
        outtext += herolist[i].name + ' ' + herolist[i].rate + ' '
        newlastlist.append(herolist[i].name)
        if herolist[i].name in lastlist:
            rankchange = 4 - lastlist.index(herolist[i].name) - i   #FOUR IS A MAGIC!
            if rankchange > 0:
                rankchange = "[color=red]↑{}[/color]".format(rankchange)
            elif rankchange < 0:
                rankchange = "[color=green]↓{}[/color]".format(-rankchange)
            else:
                rankchange = '-'
        else:
            rankchange = '[color=orange]New[/color]'
        outtext += rankchange + '\n'
    '''
    with open('lastlist','w', encoding='utf-8') as f:
        f.write(','.join(newlastlist))
    return outtext

def run():  #获取数据
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36', 'referer': 'http://www.dotamax.com/'}
        url = 'http://www.dotamax.com/hero/rate/?time=week&skill=vh'

        html = requests.get(url, headers=headers)

        soup = BeautifulSoup(html.text, 'lxml')

        #print(soup)

        heroes = soup.find_all('span', class_="hero-name-list")
        heroes = list(map(BeautifulSoup.get_text, heroes))
        rate = soup.find_all('div', style='height: 10px')
        rate = list(map(BeautifulSoup.get_text, rate))
        number = []
        for i in reversed(range(len(rate))):
                if i%2 != 0: #odd
                        number.append(rate[i])
                        rate.pop(i)
        number = list(reversed(number))
        mainlist = []
        for i in range(len(heroes)):
                #print("hero:{} rate:{} number:{}".format(heroes[i], rate[i], number[i]))
                mainlist.append(hero(heroes[i],rate[i],number[i]))
        #mainlist = bubble_num(mainlist)
        #numlist = bubble_num(mainlist)
        #ratelist = bubble_rate(mainlist)

        text = formatting(mainlist)
        return text #这里返回的文本是版头中需要修改的部分。
