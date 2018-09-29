#coding=utf-8

#Author: Jiangtian
#Create Date:2018/09/29
#Last Edited:2018/09/29

#获取今日的奖励英雄。

import datetime, json

def codetoname(code):
    return {
        'antimage': '敌法师',
        'axe': '斧王',
        'bane': '祸乱之源',
        'bloodseeker': '嗜血狂魔',
        'crystal_maiden': '水晶室女',
        'drow_ranger': '卓尔游侠',
        'earthshaker': '撼地者',
        'juggernaut': '主宰',
        'mirana': '米拉娜',
        'nevermore': '影魔',
        'morphling': '变体精灵',
        'phantom_lancer': '幻影长矛手',
        'puck': '帕克',
        'pudge': '帕吉',
        'razor': '剃刀',
        'sand_king': '沙王',
        'storm_spirit': '风暴之灵',
        'sven': '斯温',
        'tiny': '小小',
        'vengefulspirit': '复仇之魂',
        'windrunner': '风行者',
        'zuus': '宙斯',
        'kunkka': '昆卡',
        'lina': '莉娜',
        'lich': '巫妖',
        'lion': '莱恩',
        'shadow_shaman': '暗影萨满',
        'slardar': '斯拉达',
        'tidehunter': '潮汐猎人',
        'witch_doctor': '巫医',
        'riki': '力丸',
        'enigma': '谜团',
        'tinker': '修补匠',
        'sniper': '狙击手',
        'necrolyte': '瘟疫法师',
        'warlock': '术士',
        'beastmaster': '兽王',
        'queenofpain': '痛苦女王',
        'venomancer': '剧毒术士',
        'faceless_void': '虚空假面',
        'skeleton_king': '冥魂大帝',
        'death_prophet': '死亡先知',
        'phantom_assassin': '幻影刺客',
        'pugna': '帕格纳',
        'templar_assassin': '圣堂刺客',
        'viper': '蝮蛇',
        'luna': '露娜',
        'dragon_knight': '龙骑士',
        'dazzle': '戴泽',
        'rattletrap': '发条技师',
        'leshrac': '拉席克',
        'furion': '先知',
        'life_stealer': '噬魂鬼',
        'dark_seer': '黑暗贤者',
        'clinkz': '克林克兹',
        'omniknight': '全能骑士',
        'enchantress': '魅惑魔女',
        'huskar': '哈斯卡',
        'night_stalker': '暗夜魔王',
        'broodmother': '育母蜘蛛',
        'bounty_hunter': '赏金猎人',
        'weaver': '编织者',
        'jakiro': '杰奇洛',
        'batrider': '蝙蝠骑士',
        'chen': '陈',
        'spectre': '幽鬼',
        'doom_bringer': '末日使者',
        'ancient_apparition': '远古冰魄',
        'ursa': '熊战士',
        'spirit_breaker': '裂魂人',
        'gyrocopter': '矮人直升机',
        'alchemist': '炼金术士',
        'invoker': '祈求者',
        'silencer': '沉默术士',
        'obsidian_destroyer': '殁境神蚀者',
        'lycan': '狼人',
        'brewmaster': '酒仙',
        'shadow_demon': '暗影恶魔',
        'lone_druid': '德鲁伊',
        'chaos_knight': '混沌骑士',
        'meepo': '米波',
        'treant': '树精卫士',
        'ogre_magi': '食人魔魔法师',
        'undying': '不朽尸王',
        'rubick': '拉比克',
        'disruptor': '干扰者',
        'nyx_assassin': '司夜刺客',
        'naga_siren': '娜迦海妖',
        'keeper_of_the_light': '光之守卫',
        'wisp': '艾欧',
        'visage': '维萨吉',
        'slark': '斯拉克',
        'medusa': '美杜莎',
        'troll_warlord': '巨魔战将',
        'centaur': '半人马战行者',
        'magnataur': '马格纳斯',
        'shredder': '伐木机',
        'bristleback': '刚背兽',
        'tusk': '巨牙海民',
        'skywrath_mage': '天怒法师',
        'abaddon': '亚巴顿',
        'elder_titan': '上古巨神',
        'legion_commander': '军团指挥官',
        'ember_spirit': '灰烬之灵',
        'earth_spirit': '大地之灵',
        'terrorblade': '恐怖利刃',
        'phoenix': '凤凰',
        'oracle': '神谕者',
        'techies': '工程师',
        'winter_wyvern': '寒冬飞龙',
        'arc_warden': '天穹守望者',
        'monkey_king': '齐天大圣',
        'pangolier': '石鳞剑士',
        'dark_willow': '邪影芳灵',
        'grimstroke': '天涯墨客'
    }.get(code)

def doit():
    with open ('fuck.txt', 'r') as f:
        txt = f.read()
    
    import re
    arr = re.findall(r'"name": "npc_dota_hero_(.*?)"',txt)
    j = 1
    for i in arr:
        print ('\'{}\': \'\','.format(i))
        j += 1

def bonus():
    lines = {}
    with open ('bonus.txt', 'r') as f:
        for line in f.readlines():
            thisline = line[:-1]
            thisline = thisline.split(':')
            thisline[1] = thisline[1].split(',')
            def func(arr):
                return arr.replace(' ', '_')[1:]
            thisline[1] = list(map(func, thisline[1]))
            #print(thisline)
            lines[thisline[0]] = thisline[1]

    with open ('bonus_kai.json', 'w') as f:
        f.write(json.dumps(lines))
        
def run():
    with open ('bonus_kai.json', 'r') as f:
        bonuslist = json.loads(f.read())
    nowtime = datetime.datetime.today().date()
    tomorrowtime = nowtime+datetime.timedelta(days=1)
    todayheroes = list(map(codetoname, bonuslist[str(nowtime)]))
    tomheroes = list(map(codetoname, bonuslist[str(tomorrowtime)]))
    txttd = ''
    txttm = ''
    for i in todayheroes:
        txttd += i
        txttd += ' '
    for i in tomheroes:
        txttm += i
        txttm += ' '
    text = '{today}\n{h1}\n[h][/h]\n{tm}\n{tmh}'.format(today=str(nowtime), h1=txttd, tm=str(tomorrowtime), tmh=txttm)
    return text
