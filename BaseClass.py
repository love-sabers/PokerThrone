from Const import GameEvent
import random
class creature(object):
    """
    The base class of all creature
    including hero and monster
    """

    base_HP=100
    base_HP_min=0
    base_HP_max=100
    base_MP=2
    base_MP_min=0
    base_MP_max=50

    def __init__(self):
        self.HP=creature.base_HP
        self.MP=creature.base_MP
        return
    
    def add_HP(self,value):
        if(self.HP+value>creature.base_HP_max):
            self.HP=creature.base_HP_max
            return GameEvent.ADD_HP_OVER
        else:
            self.HP+=value
            return 0
        
    def lose_HP(self,value):
        if(self.HP-value<creature.base_HP_min):
            self.HP=creature.base_HP_min
            return GameEvent.LOSE_HP_OVER
        else:
            self.HP-=value
            return 0 
    
    def add_MP(self,value):
        if(self.MP+value>creature.base_MP_max):
            self.MP=creature.base_MP_max
            return GameEvent.ADD_MP_OVER
        else:
            self.MP+=value
            return 0
        
    def lose_MP(self,value):
        if(self.MP-value<creature.base_MP_min):
            self.MP=creature.base_MP_min
            return GameEvent.LOSE_MP_OVER
        else:
            self.MP-=value
            return 0

    def create_skill_set(self):
        return self.SkillSet(self)

    class SkillSet(object):
        def __init__(self, outer):
            self.outer = outer
            self.able_to_act = True

        def heal(self):
            if self.outer.HP < 10:
                self.outer.add_HP(20)
            else:
                self.outer.add_HP(10)

        def silence(self):
            self.able_to_act = False

        def reset(self):
            self.able_to_act = True

        def change_carddeck(self):
            pass

        def attack(self, damage=10):
            return damage

        def defense(self, damage=10):
            self.outer.lose_HP(damage)

        
class card(object):
    card_num=3
    def __init__(self):
        self.cardid=0
        pass
    def run(self):
        pass

class carddeck(object):
    pass

class poker(object):
    pass

class pokerdeck(object):
    pass


class Hero(creature):
    def __init__(self):
        super().__init__()
        self.skill_set = self.create_skill_set()
        self.shock_wave = self.skill_set.silence
        self.change_carddeck = self.skill_set.change_carddeck

    def attack(self):   # 被动属性
        if self.HP < 10:
            return self.skill_set.attack(20)
        else:
            return self.skill_set.attack()

    def defence(self):  # 被动属性
        c = random.randint(1, 10)
        if c < 3:
            self.skill_set.defense(5)
        else:
            self.skill_set.defense()


class Monster(creature):
    def __init__(self):
        super().__init__()
        self.skill_set = self.create_skill_set()
        self.shock_wave = self.skill_set.silence
        self.attack = self.skill_set.attack
        self.defence = self.skill_set.defense
        self.change_carddeck = self.skill_set.change_carddeck
