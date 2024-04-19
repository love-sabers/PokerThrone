import pygame
class Game(object):
    def __init__(self):
        pass
    def game_init(self):
        pass
    def game_run(self):
        pass
    def game_quit(self):
        pass
    def game_save(self):
        pass
    def game_load(self):
        pass
    def game(self,screen:pygame.Surface):
        #游戏初始化
        self.game_init()
        self.game_load()
        while(1):
            self.game_run()
            self.game_save()
        self.game_quit()
        pass
    pass