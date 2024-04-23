import pygame
import sys
import GUI
from Const import Config
from CreatureClass import Hero

game_running=1

class Game(object):
    def __init__(self,screen:pygame.Surface):
        self.screen=screen
        self.hero=Hero((540,360))
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
            self.hero.render(self.screen)        
            pygame.display.update()
            pygame.time.Clock().tick(Config.FPS)
        # deal(game_event_set)
        
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
            self.game_run()
            self.game_save()
        self.game_quit()
        pass
    pass