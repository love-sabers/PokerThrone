import pygame
import random
import GUI
from GUI import Button
from Const import GameEvent

class Skill(object):
    IMAGE_PATH='source/play.png'
    def __init__(self,pos:tuple[int,int],handtype_check_code_list:int):
        self.result = {'MP_cost': GameEvent.NULL,#int
                       'HP_cost': GameEvent.NULL,#int
                       'MP_increase': GameEvent.NULL,#int
                       'HP_increase': GameEvent.NULL,#int
                       'pos_effect': GameEvent.NULL,#list        # 正面效果是带给自己的正面效果
                       'neg_effect': GameEvent.NULL,#list        # 负面效果是带给别人的负面效果
                       'damage': GameEvent.NULL,#int
                       'operate': GameEvent.NULL#list            # 对游戏其他部分的操作请求，如换牌
        }
        self.ui=Button(pos,self.IMAGE_PATH,3,GUI.CENTER)         
        self.handtype_check_code_list=handtype_check_code_list

    def update(self,handtype_code:list[int]):
        if any(self.handtype_check_code_list==code for code in handtype_code) :
            self.ui.enabled()
        else :
            self.ui.disabled()

    def render(self,surface:pygame.Surface):
        self.ui.render(surface)

    def check_click(self,event):
        return self.ui.check_click(event)        

class Shield(Skill):        # 普通技能
    IMAGE_PATH=''
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)

    @property
    def activate(self):
        self.result['pos_effect'] = [GameEvent.IMMUNE]
        return self.result


class Medicine(Skill):          # 普通技能
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)
        self.result['HP_increase'] = 5
    @property
    def activate(self):
        return self.result


class Reshuffle(Skill):         # 普通技能
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)

    @property
    def activate(self):
        self.result['operate'] = [GameEvent.RESHUFFLE]
        return self.result


class Attack(Skill):
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)
        self.result['damage'] = 10
    @property
    def activate(self):
        return self.result


class Rage(Skill):              # 较强技能
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)
    @property
    def activate(self):
        self.result['HP_cost'] = 5
        self.result['pos_effect'] = [GameEvent.RAGE]
        return self.result


class Shockwave(Skill):         # 较强技能
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)
    @property
    def activate(self):
        self.result['neg_effect'] = [GameEvent.SHOCK]
        self.result['damage'] = 10
        return self.result


class TrickBag(Skill):      # 较强技能
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)
    @property
    def activate(self):
        dice = random.randint(1, 6)     # 投掷骰子，随机抽取下面三个能力中的一个
        if dice <= 2:
            self.result['HP_cost'] = 5        # 扣5点生命并造成20伤害
            self.result['damage'] = 20
        elif dice <= 4:
            self.result['HP_increase'] = 10     # 恢复10点生命
        else:
            self.result['operate'] = [GameEvent.RESHUFFLE]    # 重新抽牌并获得一个盾
            self.result['pos_effect'] = [GameEvent.IMMUNE]
        return self.result


class Poison(Skill):
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)

    @property
    def activate(self):
        dice = random.randint(1, 6)  # 投掷骰子，决定炸弹炸不炸
        if dice <= 3:
            self.result['damage'] = 20      # 毒药有效，否则哑弹
            self.result['neg_effect'] = [GameEvent.POISONED]
        else:
            self.result['damage'] = 5
        return self.result


class Ultimate(Skill):       # 牛逼的大招
    def __init__(self, pos: tuple[int, int], handtype_check_code_list: list[int]):
        super().__init__(pos, handtype_check_code_list)
    @property
    def activate(self):
        self.result['damage'] = 20
        self.result['neg_effect'] = [GameEvent.SHOCK]
        self.result['pos_effect'] = [GameEvent.RAGE, GameEvent.PURIFY, GameEvent.IMMUNE]
        return self.result