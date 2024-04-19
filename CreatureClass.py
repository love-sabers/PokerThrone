from Const import GameEvent
import random

class Skill(object):
    pass

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


class Shield(Skill):
    def __init__(self, entity):
        self.MP_cost = 3
        self.entity = entity

    @property
    def activate(self):
        if self.MP_cost > self.entity.MP:       # 技能释放失败
            return GameEvent.SKILL_RELEASE_FAIL
        return GameEvent.IMMUNE


class Medicine(Skill):
    def __init__(self, entity):
        self.MP_cost = 2
        self.entity = entity

    @property
    def activate(self):
        if self.MP_cost > self.entity.MP:  # 技能释放失败
            return GameEvent.SKILL_RELEASE_FAIL
        return GameEvent.HEAL

class Rage(Skill):
    def __init__(self, entity):
        self.MP_cost = 3
        self.entity = entity

    @property
    def activate(self):
        if self.MP_cost > self.entity.MP:  # 技能释放失败
            return GameEvent.SKILL_RELEASE_FAIL
        return GameEvent.RAGE

class Shockwave(Skill):
    def __init__(self, entity):
        self.MP_cost = 4
        self.entity = entity

    @property
    def activate(self):
        if self.MP_cost > self.entity.MP:   # 技能释放失败
            return GameEvent.SKILL_RELEASE_FAIL
        return GameEvent.ATTACK, GameEvent.SHOCK

class Reshuffle(Skill):
    def __init__(self, entity):
        self.MP_cost = 1
        self.entity = entity

    @property
    def activate(self):
        if self.MP_cost > self.entity.MP:
            return GameEvent.SKILL_RELEASE_FAIL
        return Reshuffle

class Hero(Creature):
    def __init__(self):
        super().__init__()
        self.skill_set = {'Medicine': Medicine(self), 'Reshuffle': Reshuffle(self), 'Shield': Shield(self)}

        self.state = []
        self.action = []

    def update(self, **kwargs):
        self.state = kwargs['state']
        self.action = kwargs['action']


class Monster(Creature):
    def __init__(self):
        super().__init__()
        self.skill_set = {}
        self.state = []
        self.action = []

    def update(self, **kwargs):
        self.state = kwargs['state']
        self.action = kwargs['action']


# test
h = Hero()
print(h.skill_set['Medicine'].activate)
