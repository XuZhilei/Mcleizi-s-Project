#coding=utf-8

import requests, json

def run():
    r = requests.get('http://api.steampowered.com/IEconDOTA2_570/GetTournamentPrizePool/v1?key=ACEB542E8E93033CACD987BD5DA301E6&leagueid=9870')
    print (json.loads(r.text))
    pool = format(json.loads(r.text)['result']['prize_pool'], ',')
    return '[size=200%][color=red]${}[/color][/size]'.format(pool)