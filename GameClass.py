import pygame
import sys
import GUI
from Const import Config
from CreatureClass import *

game_running=1


class Game(object):
    def __init__(self,screen:pygame.Surface):
        self.screen=screen
        self.hero=Hero((540,360))
        self.hero_fake=Hero((540,180))
        self.empty_event = {             # For test
            'MP_cost': 0,  # int
            'HP_cost': 0,  # int
            'MP_increase': 0,  # int
            'HP_increase': 0,  # int
            'pos_effect': [],  # list        # 正面效果是带给自己的正面效果
            'neg_effect': [],  # list        # 负面效果是带给别人的负面效果
            'damage': 0,  # int
            'operate': []  # list            # 对游戏其他部分的操作请求，如换牌
        }
        pass
    def game_init(self):
        pass
    def game_run(self):
        game_event_set=[]
        running=1
        while(running):
            self.screen.fill((0,0,0))
            for event in pygame.event.get():
                ret,game_event=self.hero.check_click(event)
                # game_event_set.append(game_event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if(ret==1):
                    a = self.deal_event(self.hero, self.hero_fake, game_event)
                    b = self.deal_event(self.hero_fake, self.hero, self.empty_event)
                    running = min(a, b)

            self.hero_fake.render_hp(self.screen)
            self.hero.render(self.screen)        
            pygame.display.update()
            pygame.time.Clock().tick(Config.FPS)
            return running
        
    def game_quit(self):
        pass
    def game_save(self):
        pass
    def game_load(self):
        pass
    def game(self):
        self.game_init()
        self.game_load()
        game_running=1
        while(game_running):
            game_running=self.game_run()
            self.game_save()
        self.game_quit()
        pass

    @staticmethod
    def deal_event(host: Hero, target: Hero, game_event: dict):
        """
        Deal the game event returned by skill.
        :param host:Hero or Monster:
        :param target: Hero or Monster:
        :param game_event: dict:
        """
        MP_cost = game_event.get('MP_cost')         # Unpack game event
        HP_cost = game_event.get('HP_cost')
        MP_increase = game_event.get('MP_increase')
        HP_increase = game_event.get('HP_increase')
        pos_effect = game_event.get('pos_effect')
        neg_effect = game_event.get('neg_effect')
        damage = game_event.get('damage')
        operate = game_event.get('operate')

        ret = host.lose_MP(MP_cost)                       # 操作方HP，MP的更改
        if ret == GameEvent.LOSE_MP_OVER:
            return 0
        ret = host.lose_HP(HP_cost)
        if ret == GameEvent.LOSE_HP_OVER:
            return 0
        host.add_MP(MP_increase)
        host.add_HP(HP_increase)

        if len(pos_effect) != 0:
            host.state.append(*pos_effect)               # 状态更改
        if len(neg_effect) != 0:
            target.state.append(*neg_effect)

        if GameEvent.PURIFY in host.state:          # Purify 处理
            host.state.remove(GameEvent.PURIFY)
            while GameEvent.POISONED in host.state:
                host.state.remove(GameEvent.POISONED)
            while GameEvent.SHOCK in host.state:
                host.state.remove(GameEvent.SHOCK)

        if GameEvent.RAGE in host.state and damage > 0:            # Rage 处理
            damage *= 2
            host.state.remove(GameEvent.RAGE)

        if GameEvent.POISONED in host.state:        # Poisoned 处理
            ret = host.lose_HP(5)
            if ret == GameEvent.LOSE_HP_OVER:
                return 0
            host.state.remove(GameEvent.POISONED)
            host.state.append(GameEvent.POISONED2)
        elif GameEvent.POISONED2 in host.state:       # 持续三回合的中毒效果，引入另外两个表示中毒的event
            ret = host.lose_HP(5)
            if ret == GameEvent.LOSE_HP_OVER:
                return 0
            host.state.remove(GameEvent.POISONED2)
            host.state.append(GameEvent.POISONED3)
        elif GameEvent.POISONED3 in host.state:
            ret = host.lose_HP(5)
            if ret == GameEvent.LOSE_HP_OVER:
                return 0
            host.state.remove(GameEvent.POISONED3)

        if GameEvent.SHOCK in host.state:           # Shock 处理
            damage /= 2
            host.state.remove(GameEvent.SHOCK)

        while damage > 0:                           # Shield 处理
            if GameEvent.IMMUNE in target.state:
                target.state.remove(GameEvent.IMMUNE)
                damage -= 5
            if GameEvent.IMMUNE not in target.state:
                break

        ret = target.lose_HP(damage)                      # 所用event执行完之后再对target扣血
        if ret == GameEvent.LOSE_HP_OVER:
            return 0

        # print('Host state:', host.state)   # For debug and test
        # print('Target state:', target.state)
        return 1            # 执行到这一步表示游戏正常进行
