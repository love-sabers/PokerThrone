from Const import GameEvent
import random


class Skill(object):
    def __init__(self):
        self.result = {'state': GameEvent.SKILL_RELEASE,
                       'MP_cost': GameEvent.NULL,
                       'HP_cost': GameEvent.NULL,
                       'HP_increase': GameEvent.NULL,
                       'pos_effect': GameEvent.NULL,        # 正面效果是带给自己的正面效果
                       'neg_effect': GameEvent.NULL,        # 负面效果是带给别人的负面效果
                       'damage': GameEvent.NULL,
                       'operate': GameEvent.NULL}           # 对游戏其他部分的操作请求，如换牌


class Creature(object):
    """
    The base class of all Creature
    including hero and monster
    """

    base_HP=100
    base_HP_min=0
    base_HP_max=100
    base_MP=2
    base_MP_min=0
    base_MP_max=50

    def __init__(self):
        self.HP=Creature.base_HP
        self.MP=Creature.base_MP
        return
    
    def add_HP(self,value):
        if(self.HP+value>Creature.base_HP_max):
            self.HP=Creature.base_HP_max
            return GameEvent.ADD_HP_OVER
        else:
            self.HP+=value
            return 0
        
    def lose_HP(self,value):
        if(self.HP-value<Creature.base_HP_min):
            self.HP=Creature.base_HP_min
            return GameEvent.LOSE_HP_OVER
        else:
            self.HP-=value
            return 0 
    
    def add_MP(self,value):
        if(self.MP+value>Creature.base_MP_max):
            self.MP=Creature.base_MP_max
            return GameEvent.ADD_MP_OVER
        else:
            self.MP+=value
            return 0
        
    def lose_MP(self,value):
        if(self.MP-value<Creature.base_MP_min):
            self.MP=Creature.base_MP_min
            return GameEvent.LOSE_MP_OVER
        else:
            self.MP-=value
            return 0


class Shield(Skill):        # 普通技能
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 3
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:       # 技能释放失败
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            self.result['pos_effect'] = GameEvent.IMMUNE
            return self.result


class Medicine(Skill):          # 普通技能
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 2
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:  # 技能释放失败
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            self.result['HP_increase'] = 5
            return self.result


class Reshuffle(Skill):         # 普通技能
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 1
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            self.result['operate'] = GameEvent.RESHUFFLE
            return self.result


class Attack(Skill):
    def __init__(self, entity):
        super().__init__()
        self.result['damage'] = 10

    @property
    def activate(self):
        return self.result


class Rage(Skill):              # 较强技能
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 3
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:  # 技能释放失败
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            self.result['HP_cost'] = 5
            self.result['pos_effect'] = GameEvent.RAGE
            return self.result


class Shockwave(Skill):         # 较强技能
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 4
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:   # 技能释放失败
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            self.result['neg_effect'] = GameEvent.SHOCK
            self.result['damage'] = 10
            return self.result


class TrickBag(Skill):      # 较强技能
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 5
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:  # 技能释放失败
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            dice = random.randint(1, 6)     # 投掷骰子，随机抽取下面三个能力中的一个
            if dice <= 2:
                self.result['HP_cost'] = 5        # 扣5点生命并造成20伤害
                self.result['damage'] = 20
            elif dice <= 4:
                self.result['HP_increase'] = 10     # 恢复10点生命
            else:
                self.result['operate'] = GameEvent.RESHUFFLE    # 重新抽牌并获得一个盾
                self.result['pos_effect'] = GameEvent.IMMUNE
            return self.result


class Poison(Skill):
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 5
        self.entity =  entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:   # 技能释放失败
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            dice = random.randint(1, 6)  # 投掷骰子，决定炸弹炸不炸
            if dice <= 3:
                self.result['damage'] = 20      # 毒药有效，否则哑弹
                self.result['neg_effect'] = GameEvent.POISONED
            else:
                self.result['damage'] = 5
            return self.result


class Ultimate(Skill):       # 牛逼的大招
    def __init__(self, entity):
        super().__init__()
        self.result['MP_cost'] = 7
        self.entity = entity

    @property
    def activate(self):
        if self.result['MP_cost'] > self.entity.MP:
            self.result['state'] = GameEvent.SKILL_RELEASE_FAIL
            return self.result
        else:
            self.result['damage'] = 20
            self.result['neg_effect'] = GameEvent.SHOCK
            self.result['pos_effect'] = [GameEvent.RAGE, GameEvent.PURIFY, GameEvent.IMMUNE]
            return self.result


class Hero(Creature):
    def __init__(self):
        super().__init__()
        self.skill_set = {'Medicine': Medicine(self),
                          'Reshuffle': Reshuffle(self),
                          'Shield': Shield(self),
                          'Attack': Attack(self),
                          'Ultimate': Ultimate(self)}
        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    '''def update(self, **kwargs):
        self.state = kwargs['state']'''


class Monster(Creature):
    def __init__(self):
        super().__init__()
        self.skill_set = {'Attack': Attack(self),
                          'Medicine': Medicine(self),
                          'Poison': Poison(self)}
        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    '''def update(self, **kwargs):
        self.state = kwargs['state']'''


# test
h = Hero()
print(h.skill_set['Shield'].activate)
m = Monster()
print(m.skill_set['Medicine'].activate)
