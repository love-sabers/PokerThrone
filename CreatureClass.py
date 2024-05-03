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
        if(self.HP-value<=Creature.base_HP_min):
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
        if(self.MP-value<=Creature.base_MP_min):
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
        self.poker_deck.update_revealed()
        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    def deal(self,game_event:dict):
        damage=game_event.get('damage')
        running_flag=1
        if(self.HP<=damage):
            running_flag=0
        else:
            self.HP = self.HP - int(damage)
        return running_flag

    def render_hp(self,surface:pygame.Surface):
        # 定义血条颜色
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)

        # 定义血条位置和尺寸
        x, y = 50, 50  # 血条在屏幕上的位置
        max_width, height = 200, 20  # 血条的最大宽度和高度
        border_thickness = 2  # 边框的厚度

        # 计算当前血条长度
        current_width = max(0, 2*self.HP)  # 假设满血是100

        # 绘制血条背景（红色）
        pygame.draw.rect(surface, RED, (x, y, max_width, height))

        # 绘制当前血量（绿色）
        if current_width > 0:
            pygame.draw.rect(surface, GREEN, (x, y, current_width, height))

        # 绘制黑色边框
        pygame.draw.rect(surface, (0, 0, 0), (x, y, max_width, height), border_thickness)

        # 设置字体和文字
        font = pygame.font.Font(None, 24)  # 使用默认字体，24点大小
        text = font.render(f'{self.HP}/100', True, BLACK)
        text_rect = text.get_rect(center=(x + max_width / 2, y + height / 2))
        surface.blit(text, text_rect)

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
        if(flag==1):
            self.poker_deck.update_revealed()
        return flag,ret_set


    def render(self,surface:pygame.Surface):
        self.discard.render(surface)
        self.pass_round.render(surface)
        self.poker_deck.render(surface)
        hand=self.poker_deck.evaluate_hand()
        # 设置字体和文字
        COLOR_CH = (248, 195, 205)
        font = pygame.font.Font(None, 40)
        if(len(self.poker_deck.disPokered)!=0):
            text = font.render(f'{len(self.poker_deck.disPokered)}', True, COLOR_CH)
            text_rect = text.get_rect(center=(60,360))
            surface.blit(text, text_rect)
        text = font.render(f'{len(self.poker_deck.unrevealed)}', True, COLOR_CH)
        text_rect = text.get_rect(center=(1020, 360))
        surface.blit(text, text_rect)
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
