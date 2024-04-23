from Const import GameEvent
import random

class Skill(object):
    def __init__(self) -> None:
        pass
    pass

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
