import pygame
from Const import GameEvent
from PokerClass import PokerDeck
import SkillClass
import GUI

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
        self.discard=GUI.Button((pos[0]+100,pos[1]+140),self.DISCARD_PATH,3,option=GUI.CENTER)
        self.pass_round=GUI.Button((pos[0]-100,pos[1]+140),self.PASS_PATH,3,option=GUI.CENTER)
        self.skill_set = {'Medicine': SkillClass.Medicine(self), 
                          'Reshuffle': SkillClass.Reshuffle(self), 
                          'Shield': SkillClass.Shield(self)}
        self.state = []
        self.action = []

    def check_click(self,event):
        self.poker_deck.check_click(event)
        if(self.discard.check_click(event)):
            self.poker_deck.reload_user()
        if(self.pass_round.check_click(event)):
            self.poker_deck.update_revealed()
        return 1,GameEvent.ATTACK
    
    def render(self,surface:pygame.Surface):
        self.discard.render(surface)
        self.pass_round.render(surface)
        self.poker_deck.render(surface)

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
