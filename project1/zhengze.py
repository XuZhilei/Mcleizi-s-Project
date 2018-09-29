#coding=utf-8
#我以后再用正则我是狗
import re, json, os

def fuck():
    with open('matchlist.txt') as f:
        text = f.read()

    relist = re.findall('\|player1=\{\{\w+\/\w+\}\}\n.+', text)

    battle = []
    for i in relist:
        player1 = re.match('(\|player1=\{\{team2Short)\/(.+)\}\}', i).group(2)
        player2 = re.findall('(\|player2=\{\{teamShort)\/(.+)\}\}', i)[0][1]
        battle.append([player1, player2])

    with open ('matchlist.json', 'w') as f:
        f.write(json.dumps(battle))

def suck():
    with open('matchlist.json') as f:
        text = json.loads(f.read())

    ballll = []
    for i in range(len(text)):
        ballll.append([text[i][0], text[i][1], (i // 4+1), 0, 0, []])

    with open ('truematchlist.json', 'w') as f:
            f.write(json.dumps(ballll))

suck()