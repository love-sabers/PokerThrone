import pygame
import sys
import GUI
from PokerClass import PokerDeck

game_running=1

class Game(object):
    DISCARD_PATH='source/discard.png'
    PASS_PATH='source/pass.png'
    def __init__(self,screen:pygame.Surface):
        self.screen=screen
        self.poker_deck=PokerDeck((540,360))
        self.discard=GUI.Button((640,500),self.DISCARD_PATH,3,option=GUI.CENTER)
        self.pass_round=GUI.Button((440,500),self.PASS_PATH,3,option=GUI.CENTER)
        pass
    def game_init(self):
        self.poker_deck.update_revealed()
        pass
    def game_run(self):
        self.screen.fill((0,0,0))
        for event in pygame.event.get():
            self.poker_deck.check_click(event)
            if(self.discard.check_click(event)):
                self.poker_deck.reload_user()
            if(self.pass_round.check_click(event)):
                self.poker_deck.update_revealed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.discard.render(self.screen)
        self.pass_round.render(self.screen)
        self.poker_deck.render(self.screen)
        pygame.display.update()
        pygame.time.Clock().tick(60)
        pass
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