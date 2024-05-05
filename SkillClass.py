import pygame
import random
import GUI
from GUI import Button
from Const import GameEvent

class Skill(object):
    IMAGE_PATH='source/play.png'
    def __init__(self,pos:tuple[int,int],handtype_check_code:int):
        self.result = {'MP_cost': 0,#int
                       'HP_cost': 0,#int
                       'MP_increase': 0,#int
                       'HP_increase': 0,#int
                       'pos_effect': [],#list        # 正面效果是带给自己的正面效果
                       'neg_effect': [],#list        # 负面效果是带给别人的负面效果
                       'damage': 0,#int
                       'operate': []#list            # 对游戏其他部分的操作请求，如换牌
        }
        self.ui=Button(pos,self.IMAGE_PATH,3,GUI.CENTER)         
        self.handtype_check_code=handtype_check_code

    def update(self,handtype_code:list[int]):
        if(self.ui.is_selected()):
            return
        if any(self.handtype_check_code==code for code in handtype_code) :
            self.ui.enabled()
        else :
            self.ui.disabled()

    def render(self,surface:pygame.Surface):
        self.ui.render(surface)

    def check_click(self,event):
        return self.ui.check_click(event)        

class Shield(Skill):        # 普通技能
    IMAGE_PATH='source/santiao.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['pos_effect'] = [GameEvent.IMMUNE]

    
    def activate(self):
        return self.result


class Medicine(Skill):          # 普通技能
    IMAGE_PATH='source/liangdui.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['HP_increase'] = 5
    
    def activate(self):
        return self.result


class Getcard(Skill):         # 普通技能
    IMAGE_PATH='source/sitiao.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['operate'] = [GameEvent.GETCARD]

    def activate(self):
        return self.result


class Attack(Skill):
    IMAGE_PATH='source/duizi.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['damage'] = 10

    def activate(self):
        return self.result


class Rage(Skill):              # 较强技能
    IMAGE_PATH='source/tonghua.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['HP_cost'] = 5
        self.result['pos_effect'] = [GameEvent.RAGE]
    
    def activate(self):
        return self.result


class Shockwave(Skill):         # 较强技能
    IMAGE_PATH='source/shunzi.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['neg_effect'] = [GameEvent.SHOCK]
        self.result['damage'] = 10
    
    def activate(self):
        return self.result


class TrickBag(Skill):      # 较强技能
    IMAGE_PATH='source/hulu.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
    
    def activate(self):
        dice = random.randint(1, 6)     # 投掷骰子，随机抽取下面三个能力中的一个
        if dice <= 2:
            self.result['HP_cost'] = 5        # 扣5点生命并造成20伤害
            self.result['HP_increase'] = 0
            self.result['damage'] = 20
            self.result['operate'] = []    
            self.result['pos_effect'] = []
        elif dice <= 4:
            self.result['HP_cost'] = 0
            self.result['HP_increase'] = 10     # 恢复10点生命
            self.result['damage'] = 0
            self.result['operate'] = []    
            self.result['pos_effect'] = []
        else:
            self.result['HP_cost'] = 0
            self.result['HP_increase'] = 0    
            self.result['damage'] = 0
            self.result['operate'] = [GameEvent.GETCARD]    # 重新抽牌并获得一个盾
            self.result['pos_effect'] = [GameEvent.IMMUNE]
        return self.result


class Poison(Skill):
    IMAGE_PATH='source/tonghuashun.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)

    
    def activate(self):
        dice = random.randint(1, 6)  # 投掷骰子，决定炸弹炸不炸
        if dice <= 4:
            self.result['damage'] = 20      # 毒药有效，否则哑弹
            self.result['neg_effect'] = [GameEvent.POISONED]
        else:
            self.result['damage'] = 5
            self.result['neg_effect'] = []
        return self.result


class Ultimate(Skill):       # 牛逼的大招
    IMAGE_PATH='source/huanjiatonghuashun.png'
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: int):
        super().__init__(pos, handtype_check_code_list)
        self.result['damage'] = 20
        self.result['neg_effect'] = [GameEvent.SHOCK]
        self.result['pos_effect'] = [GameEvent.RAGE, GameEvent.PURIFY, GameEvent.IMMUNE,GameEvent.IMMUNE,GameEvent.IMMUNE]
    
    def activate(self):
        return self.result