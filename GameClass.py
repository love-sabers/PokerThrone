import pygame
import sys
from PokerClass import PokerDeck
class Game(object):
    def __init__(self,screen:pygame.Surface):
        self.screen=screen
        self.p=PokerDeck((540,360))
        pass
    def game_init(self):
        self.p.update_revealed()
        self.p.update_revealed()
        pass
    def game_run(self):
        self.screen.fill((0,0,0))
        self.p.render(self.screen)
        pygame.display.update()
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            self.p.check_click(self.screen,event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pass
    def game_quit(self):
        pass
    def game_save(self):
        pass
    def game_load(self):
        pass
    def game(self):
        #游戏初始化
        self.game_init()
        self.game_load()
        while(1):
            self.game_run()
            self.game_save()
        self.game_quit()
        pass
    pass