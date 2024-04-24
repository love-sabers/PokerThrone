import pygame
import SkillClass
import GUI
import random
from Const import GameEvent
import PokerClass
from PokerClass import PokerDeck
 
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

class Hero(Creature):
    DISCARD_PATH='source/discard.png'
    PASS_PATH='source/pass.png'
    def __init__(self,pos:tuple[int,int]):
        super().__init__()
        self.poker_deck=PokerDeck(pos)
        self.discard=GUI.Button((pos[0]+80,pos[1]+150),self.DISCARD_PATH,3,option=GUI.CENTER)
        self.pass_round=GUI.Button((pos[0]-80,pos[1]+150),self.PASS_PATH,3,option=GUI.CENTER)
        w_gap=180
        h_gap=140
        w_fix=70
        h_fix=10
        self.skill_set =[SkillClass.Attack((pos[0]-2*w_gap-w_fix,pos[1]+h_gap+h_fix),PokerClass.ONE_PAIR),
                         SkillClass.Shield((pos[0]-w_gap-w_fix,pos[1]+h_gap+h_fix),PokerClass.THREE_AKIND),
                         SkillClass.Medicine((pos[0]-2*w_gap-w_fix,pos[1]+2*h_gap+h_fix),PokerClass.TWO_PAIRS),
                         SkillClass.Getcard((pos[0]-w_gap-w_fix,pos[1]+2*h_gap+h_fix),PokerClass.FOUR_AKIND),
                         SkillClass.Rage((pos[0]+w_gap+w_fix,pos[1]+h_gap+h_fix),PokerClass.FLUSH),
                         SkillClass.Shockwave((pos[0]+2*w_gap+w_fix,pos[1]+h_gap+h_fix),PokerClass.STRAIGHT),
                         SkillClass.Poison((pos[0]+w_gap+w_fix,pos[1]+2*h_gap+h_fix),PokerClass.STRAIGHT_FLUSH),
                         SkillClass.TrickBag((pos[0]+2*w_gap+w_fix,pos[1]+2*h_gap+h_fix),PokerClass.FULL_HOUSE),
                         SkillClass.Ultimate((pos[0],pos[1]+2*h_gap+h_fix),PokerClass.ROYAL_FLUSH)
        ]
        for skill in self.skill_set:
            skill.ui.disabled()
        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    def check_click(self,event):
        self.poker_deck.check_click(event)
        if self.discard.check_click(event):
            self.poker_deck.reload_user()
        if self.pass_round.check_click(event):
            self.poker_deck.update_revealed()

        flag=0
        ret_set=0
        for skill in self.skill_set:
            if(skill.check_click(event)):
                flag=1
                ret_set=skill.activate()
        return flag,ret_set
    
    def render(self,surface:pygame.Surface):
        self.discard.render(surface)
        self.pass_round.render(surface)
        self.poker_deck.render(surface)
        hand=self.poker_deck.evaluate_hand()
        for skill in self.skill_set:
            if hand != None:
                skill.update(hand)
            skill.render(surface)

class Monster(Creature):
    def __init__(self):
        super().__init__()
        self.skill_set = {'Attack': SkillClass.Attack(self),
                          'Medicine': SkillClass.Medicine(self),
                          'Poison': SkillClass.Poison(self)}
        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    '''def update(self, **kwargs):
        self.state = kwargs['state']'''


# # test
# h = Hero()
# print(h.skill_set['Shield'].activate)
# m = Monster()
# print(m.skill_set['Medicine'].activate)
