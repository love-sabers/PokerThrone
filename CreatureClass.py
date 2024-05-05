#此部分为游戏中生物，包括hero与monster
import pygame
import SkillClass
import GUI
import random
from Const import GameEvent
import PokerClass
from PokerClass import PokerDeck
 
class Creature(object):
    """
    这个类是所有生物的父类
    包括hero与monster
    The base class of all Creature
    including hero and monster
    """

    #生物的基本属性
    base_HP=100
    base_HP_min=0
    base_HP_max=100
    base_MP=2
    base_MP_min=0
    base_MP_max=50

    #生物初始化
    def __init__(self):
        self.HP=Creature.base_HP
        self.MP=Creature.base_MP#当前版本不涉及蓝量
        return
    
    #加血
    def add_HP(self,value):
        if(self.HP+value>Creature.base_HP_max):
            self.HP=Creature.base_HP_max
            return GameEvent.ADD_HP_OVER
        else:
            self.HP+=value
            return 0
        
    #减血
    def lose_HP(self,value):
        if(self.HP-value<=Creature.base_HP_min):
            self.HP=Creature.base_HP_min
            return GameEvent.LOSE_HP_OVER
        else:
            self.HP-=value
            return 0 
    
    #加蓝
    def add_MP(self,value):
        if(self.MP+value>Creature.base_MP_max):
            self.MP=Creature.base_MP_max
            return GameEvent.ADD_MP_OVER
        else:
            self.MP+=value
            return 0

    #减蓝    
    def lose_MP(self,value):
        if(self.MP-value<=Creature.base_MP_min):
            self.MP=Creature.base_MP_min
            return GameEvent.LOSE_MP_OVER
        else:
            self.MP-=value
            return 0
        
    #渲染血条   
    def render_hp(self,pos,surface:pygame.Surface,max_width=200,height=20):
        '''
        pos 血条位置
        max_width 血条显示长度
        height 血条显示宽度
        '''
        # 定义血条颜色
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)

        # 定义血条位置和尺寸
        x, y = pos[0], pos[1]  # 血条在屏幕上的位置
        # max_width, height 血条的最大宽度和高度
        border_thickness = 2  # 边框的厚度

        # 计算当前血条长度
        current_width = max(0, (self.HP/self.base_HP_max)*max_width)  # 假设满血是100

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

class Hero(Creature):
    #内含组件的资源路径
    DISCARD_PATH='source/discard.png'
    PASS_PATH='source/pass.png'
    def __init__(self,pos:tuple[int,int]):
        super().__init__()
        self.pos=pos
        #牌组
        self.poker_deck=PokerDeck(pos)
        #重抽按钮
        self.discard=GUI.Button((pos[0]+80,pos[1]+150),self.DISCARD_PATH,3,option=GUI.CENTER)
        self.discard_num_max=3
        self.discard_num=self.discard_num_max
        #过牌按钮
        self.pass_round=GUI.Button((pos[0]-80,pos[1]+150),self.PASS_PATH,3,option=GUI.CENTER)
        
        #位置调整参数
        w_gap=180
        h_gap=140
        w_fix=70
        h_fix=10
        #英雄技能包
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
        #初始化牌组
        self.poker_deck.update_revealed()

        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    def check_click(self,event):
        flag=0
        ret_set={}
        #牌组按钮检查
        self.poker_deck.check_click(event)
        
        #重抽 过牌按钮检查与处理
        if self.discard.check_click(event):
            if(self.discard_num>0):
                self.discard_num-=self.poker_deck.reload_user()
        if self.pass_round.check_click(event):
            flag=1

        #技能包按钮检查
        for skill in self.skill_set:
            if(skill.check_click(event)):
                flag=1
                ret_set=skill.activate()

        #过牌或者放技能均视作回合结束        
        if(flag==1):
            self.discard_num=self.discard_num_max
            self.poker_deck.update_revealed()
    
        return flag,ret_set


    def render(self,surface:pygame.Surface):
        #渲染组件
        self.discard.render(surface)
        self.pass_round.render(surface)
        self.poker_deck.render(surface)
        self.render_hp((self.pos[0]-100,self.pos[1]+200),surface)

        #渲染手牌
        hand=self.poker_deck.evaluate_hand()
        for skill in self.skill_set:
            if hand != None:
                skill.update(hand)
            skill.render(surface)

        #渲染剩余重抽数
        COLOR_CH = (255, 255, 255)
        font = pygame.font.Font(None, 40)
        text = font.render(f'{self.discard_num}', True, COLOR_CH)
        text_rect = text.get_rect(center=(540+140, 360+130))
        surface.blit(text, text_rect)    


class Monster(Creature):
    def __init__(self,pos:tuple[int,int]):
        super().__init__()
        self.pos=pos
        self.skill_set = {'Attack':SkillClass.Attack((0,0),0),
                         'Shield':SkillClass.Shield((0,0),0),
                         'Medicine':SkillClass.Medicine((0,0),0)}
        self.state = []         # 存状态token（如SHOCK，RAGE等）
        self.info = ''          # 放角色介绍之类的

    def render(self,surface:pygame.Surface):
        self.render_hp(self.pos,surface,max_width=400)

    def activate(self):
        #monster依据当前状态决定如何释放技能
        if(self.HP>50):
            return self.skill_set['Attack'].activate()
        elif(self.HP>20):
            rand=random.randint(1,2)
            if(rand==1):
                return self.skill_set['Medicine'].activate()
            else:
                return self.skill_set['Attack'].activate()
        else :
            rand=random.randint(1,4)
            if(rand==1):
                return self.skill_set['Shield'].activate()
            else:
                return self.skill_set['Medicine'].activate()