#coding=utf-8

#Author: Jiangtian
#Create Date:2018/08/13
#Last Edited:2018/08/13

import requests, json
import time

#my steam api key is ACEB542E8E93033CACD987BD5DA301E6
key = 'ACEB542E8E93033CACD987BD5DA301E6'
# The International 2018's league id is 9870
ti8leagueid = 9870
# the last qualifier game id is 3973246064. all group stage and main event is below it.
#http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1?key=ACEB542E8E93033CACD987BD5DA301E6&league_id=9870
timepoint = 3973246064  #randomly choose a match for test

def get_team_id(team_name):
    return {
        'lgd': 15,
        'og': 2586976,
        'ig': 5,
        'mski': 543897,
        'eg': 39,
        'vgj.t': 5027210,
        'tl': 2163,
        'fnc': 350190,
        'vg': 726228,
        'vgj.s': 5228654,
        'nb': 1375614,
        'tnc': 2108395,
        'secret': 1838315,
        'serenity': 5066616,
        'vp': 1883502,
        'optic': 5026801,
        'winstrike': 5229127,
        'pain': 67
    }.get(team_name)

def get_team_name(team_id):
    team_id = str(team_id)
    return {
        '15': 'PSG.LGD',
        '2586976': 'OG',
        '5': 'Invictus Gaming',
        '543897': 'Mineski',
        '39': 'Evil Geniuses',
        '5027210': 'VGJ Thunder',
        '2163': 'Team Liquid',
        '350190': 'Fnatic',
        '726228': 'ViCi Gaming',
        '5228654': 'VGJ Storm',
        '1375614': 'Newbee',
        '2108395': 'TNC Pro Team',
        '1838315': 'Team Secret',
        '5066616': 'Team Serenity',
        '1883502': 'Virtus.Pro',
        '5026801': 'OpTic Gaming',
        '5229127': 'Winstrike',
        '67': 'paiN Gaming'
    }.get(team_id)

def domatchlist():
    with open ('falsematchlist.json', 'r') as f:
        matchlist = json.loads(f.read())
    for i in range(len(matchlist)):
        matchlist[i][0] = get_team_id(matchlist[i][0])
        matchlist[i][1] = get_team_id(matchlist[i][1])
        if matchlist[i][0] > matchlist[i][1]:
            matchlist[i][0], matchlist[i][1] = matchlist[i][1], matchlist[i][0]
    with open ('falsematchlist.json', 'w') as f:
        f.write(json.dumps(matchlist))

def catch():
    #first load matchlist
    while True:
        r = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1?key=ACEB542E8E93033CACD987BD5DA301E6&league_id=9870')
        if json.loads(r.text) != {}:
            break
        time.sleep(3)
        print('Getting API data...')
        
    with open ('truematchlist.json', 'r') as f:
        matchlist = json.loads(f.read())
        #team1/team2/series/status(0=not yet, 1=live, 2=finished)/score(0, 1, 2, 10, 11, 20)/[matchid1, matchid2]

    #catch living match
    r = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1?key=ACEB542E8E93033CACD987BD5DA301E6&league_id=9870')  #测试中，结束后加上&league_id=9870
    #r = requests.get('https://api.opendota.com/api/live')
    r = json.loads(r.text)['result']['games']

    #temparr = r
    #r = []
    #for i in temparr:
    #    if i['league_id'] == 9870:
    #        r.append(i)
    #with open ('falselive.json', 'r') as f:
    #    r = json.loads(f.read())['result']['games']

    if r == []: #if no living match:
        pass #output 'no living match'
    else: #if have living match
        for i in r: #traversing living match
            for j in range(len(matchlist)): #traversing matchlist
                if (i['radiant_team']['team_id'] in matchlist[j][0:2]) & (i['dire_team']['team_id'] in matchlist[j][0:2]):    #match this match from teamid
                    matchlist[j][3] = 1 #1 = live
                    break

    #catch finished game
    r = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1?key=ACEB542E8E93033CACD987BD5DA301E6&league_id=9870')
    r = json.loads(r.text)['result']['matches']
    #with open ('falsefinish.json', 'r') as f:
    #    r = json.loads(f.read())['result']['matches']

    for i in r:
        if i['match_id'] < timepoint:   #if qualifier continue
            continue
        for j in range(len(matchlist)):
            if (i['radiant_team_id'] in matchlist[j][0:2]) & (i['dire_team_id'] in matchlist[j][0:2]):    #match this match from teamid
                if i['match_id'] in matchlist[j][5]:    #if this match can be found in matchlist, continue to next match
                    break
                else:   #if not, add it to matchlist
                    matchlist[j][5].append(i['match_id'])
                    rsingle = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?key=ACEB542E8E93033CACD987BD5DA301E6&match_id=' + str(i['match_id']))
                    rsingle = json.loads(rsingle.text)['result']
                    if len(matchlist[j][5]) == 2: #if it's the second match in a series; it means status=1(live)
                        matchlist[j][3] = 2 #2=finished
                    if (rsingle['radiant_win'] == False) & (i['radiant_team_id'] < i['dire_team_id']):
                        matchlist[j][4] += 1
                    elif (rsingle['radiant_win'] == True) & (i['radiant_team_id'] > i['dire_team_id']):
                        matchlist[j][4] += 1
                    else:
                        matchlist[j][4] += 10

    

    with open ('truematchlist.json', 'w') as f:
        f.write(json.dumps(matchlist))
    return 0

def writeformat(canshu, whichday):#0为难民，1为皇家，2为积分表
    with open ('truematchlist.json', 'r') as f:
        matchlist = json.loads(f.read())
        #team1/team2/series/status(0=not yet, 1=live, 2=finished)/score(0, 1, 2, 10, 11, 20)/[matchid1, matchid2]

    writetext = ''

    def formatunit(team1, team2, score):
        score1 = score // 10
        score2 = score % 10
        if score1 != 0:
            score1 = '[color=red][b]{}[/b][/color]'.format(score1)
        if score2 != 0:
            score2 = '[color=red][b]{}[/b][/color]'.format(score2)    
        formattedtext = '[l][b]{t1}[/b][/l][r][b]{t2}[/b][/r][align=center]{s1} - {s2}[/align]'.format(t1=get_team_name(team1), t2=get_team_name(team2), s1=score1, s2=score2)
        return (formattedtext)

    finishedtext = ''
    for i in matchlist:
        if i[3] != 2:
            continue
        finishedtext += formatunit(i[0], i[1], i[4])

    livetext = ''
    for i in matchlist:
        if i[3] != 1:
            continue
        livetext += formatunit(i[0], i[1], i[4])

    def formatunit2(team1, team2):
        formattedtext = '[l][b]{t1}[/b][/l][r][b]{t2}[/b][/r][align=center]vs.[/align]'.format(t1=get_team_name(team1), t2=get_team_name(team2))
        return (formattedtext)

    nexttext = ''
    lennext = 0
    for i in matchlist:
        if i[3] == 0:
            lennext += 1
            nexttext += formatunit2(i[0], i[1])
        if lennext >= 4:
            break

    writetext = '{t1}\n\n[/collapse][color=red][b]LIVE![/b][/color]\n{t2}[h][/h]\n[b]NEXT:[/b]\n{t3}[/font][h][/h]\n———————————————数据更新于{t4}'.format(t1=finishedtext, t2=livetext, t3=nexttext, t4=time.strftime("%H:%M", time.localtime()))

    ranklist = [[15,0,0], [2586976,0,0], [5,0,0], [543897,0,0], [39,0,0], [5027210,0,0], [2163,0,0], [350190,0,0], [726228,0,0], [5228654,0,0], [1375614,0,0], [2108395,0,0], [1838315,0,0], [5066616,0,0], [1883502,0,0], [5026801,0,0], [5229127,0,0], [67,0,0]]
    for i in matchlist:
        for j in range(len(ranklist)):
            if i[0] == ranklist[j][0]:
                if i[4] == 20:
                    ranklist[j][1] += 2
                if i[4] == 11:
                    ranklist[j][1] += 1
                    ranklist[j][2] += 1
                if i[4] == 10:
                    ranklist[j][1] += 1
                if i[4] == 2:
                    ranklist[j][2] += 2
                if i[4] == 1:
                    ranklist[j][2] += 1
                continue
            if i[1] == ranklist[j][0]:
                if i[4] == 20:
                    ranklist[j][2] += 2
                if i[4] == 11:
                    ranklist[j][2] += 1
                    ranklist[j][1] += 1
                if i[4] == 10:
                    ranklist[j][2] += 1
                if i[4] == 2:
                    ranklist[j][1] += 2
                if i[4] == 1:
                    ranklist[j][1] += 1

    def bubbleSort(nums):
        for i in range(len(nums)-1):    # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(nums)-i-1):  # ｊ为列表下标
                if nums[j][1] > nums[j+1][1]:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
        for i in range(3):    # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(nums)-1):  # ｊ为列表下标
                if (nums[j][2] < nums[j+1][2]) & (nums[j][1] == nums[j+1][1]):
                    nums[j], nums[j+1] = nums[j+1], nums[j]
        return nums
    ranklist = bubbleSort(ranklist)
    ranklist.reverse()

    ranktexta = '[b][align=center]Group A[/align][/b][h][/h]\n'
    ranktextb = '[h][/h][b][align=center]Group B[/align][/b][h][/h]\n'
    ranka = 0
    rankb = 0
    for i in ranklist:
        if i[0] in [5229127, 350190, 15, 543897, 39, 5027210, 2163, 2586976, 5]:
            ranka += 1
            ranktexta += '[l][b]{rank}. {name}[/b][/l][r][b]{w}-{l}[/b][/r][align=center][/align]\n'.format(rank=ranka, name=get_team_name(i[0]), w=i[1], l=i[2])
            if ranka == 4:
                ranktexta += '[h][/h]'
            if ranka == 8:
                ranktexta += '[h][/h]'
        elif i[0] in [726228, 67, 5066616, 5026801, 1883502, 2108395, 5228654, 1838315, 1375614]:
            rankb += 1
            ranktextb += '[l][b]{rank}. {name}[/b][/l][r][b]{w}-{l}[/b][/r][align=center][/align]\n'.format(rank=rankb, name=get_team_name(i[0]), w=i[1], l=i[2])
            if rankb == 4:
                ranktextb += '[h][/h]'
            if rankb == 8:
                ranktextb += '[h][/h]'
    ranktext = ranktexta + ranktextb + ' \n'

    def royal_team_name(teamid):
        teamid = str(teamid)
        return {
            '15': '[img]./mon_201806/03/8xQ5-f1slKjT8S1e-1e.png[/img]PSG.LGD',
            '2586976': '[img]./mon_201803/28/8xQ5-801mKhS1e-1e.png[/img]OG',
            '5': '[img]./mon_201703/13/8xQ2g-e8d5KkT8S1e-1e.png[/img]Invictus Gaming',
            '543897': '[img]./mon_201806/03/8xQ5-8s0cKiT8S1e-1e.png[/img]Mineski',
            '39': '[img]./mon_201806/03/8xQ5-iyixKhT8S1e-1e.png[/img]Evil Geniuses',
            '5027210': '[img]./mon_201806/03/8xQ5-2v7zKiT8S1e-1e.png[/img]VGJ Thunder',
            '2163': '[img]./mon_201806/03/8xQ5-36owKgT8S1e-1e.png[/img]Team Liquid',
            '350190': '[img]./mon_201707/31/8xQ13r-cz7wKhT8S1e-1e.png[/img]Fnatic',
            '726228': '[img]./mon_201806/03/8xQ5-jumcKkT8S1e-1e.png[/img]Vici Gaming',
            '5228654': '[img]./mon_201806/03/8xQ5-8h6qKhT8S1e-1e.png[/img]VGJ Storm',
            '1375614': '[img]./mon_201806/03/8xQ5-kltgKkT8S1e-1e.png[/img]Newbee',
            '2108395': '[img]./mon_201806/03/8xQ5-4r0hKgT8S1e-1e.png[/img]TNC Predator',
            '1838315': '[img]./mon_201806/03/8xQ5-779kKgT8S1e-1e.png[/img]Team Secret',
            '5066616': '[img]./mon_201808/15/8xQ5-6ifKfT8S1e-1e.png[/img]Team Serenity',
            '1883502': '[img]./mon_201808/15/8xQ5-cochKjT8S1e-1e.png[/img]Virtus.pro',
            '5026801': '[img]./mon_201806/03/8xQ5-djvjKhT8S1e-1e.png[/img]OpTic Gaming',
            '5229127': '[img]./mon_201808/15/8xQ5-ga9kKjT8S1e-1e.png[/img]Winstrike',
            '67': '[img]./mon_201803/28/8xQ5-hoidKhS1e-1e.png[/img]paiN Gaming'
        }.get(teamid)

    def royal_series_format(series):
        day1time = 1534348800
        dayplus = 86400
        seriesplus = 9000
        seriestime = day1time + (series // 5) * dayplus + (series % 5) * seriesplus
        timearray = time.localtime(seriestime)
        day = time.strftime('%d',timearray)
        hourmin = time.strftime('%H:%M',timearray)
        if (series % 2 == 0):
            group = 'A'
        else:
            group = 'B'
        trueseries = (series // 2) + 1
        return ('[td rowspan=4][align=center]8月{day}日 {hourmin}\n{group}组\n第{series}轮[/align][/td]\n'.format(day=day, hourmin=hourmin, group=group, series=trueseries))

    royal_text = ''

    for i in range(len(matchlist)):
        if i < ((whichday - 1) * 20):
            continue
        if i % 4 == 0:
            royal_text += royal_series_format((i//4))
        if matchlist[i][3] != 2:
            royal_text += '[td]{t1}[/td]\n[td][align=center]-[/align][/td]\n[td]{t2}[/td]\n[td][/td][/tr]\n[tr]\n'.format(t1=royal_team_name(matchlist[i][0]), t2=royal_team_name(matchlist[i][1]))
        else:
            royal_text += '[td]{t1}[/td]\n[td][align=center]{s1} - {s2}[/align][/td]\n[td]{t2}[/td]\n[td][/td][/tr]\n[tr]\n'.format(t1=royal_team_name(matchlist[i][0]), t2=royal_team_name(matchlist[i][1]), s1=(matchlist[i][4] // 10), s2=(matchlist[i][4] % 10))


    if canshu == 0:
        returntext = writetext
    if canshu == 1:
        returntext = royal_text
    if canshu == 2:
        returntext = ranktext

    return returntext
