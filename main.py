import pygame
import sys
import MeauClass
from MeauClass import MainMeau
from Const import GameEvent
from Const import Config
from PokerClass import Poker
from GUI import Rod

def main():
    #init pygame
    pygame.init()
    screen=pygame.display.set_mode(Config.WINDOW_SIZE)
    clock=pygame.time.Clock()
    running=True

    #meau circulate
    
    # r=rob()
    # p=Poker('Ace','Clubs')

    # while(running):
    #     screen.fill((0,0,0))
    #     p.render(screen)
    #     pygame.display.update()
    #     for event in pygame.event.get():
    #         p.ui.check_click(screen,event)
    #         if event.type == pygame.QUIT:
    #             running=0
    meau=MainMeau()
    while(running):
        choice=meau.run(screen)

        if(choice==MeauClass.PLAY):
            pass
        elif(choice==MeauClass.OPTION):
            pass
        elif(choice==MeauClass.QUIT):
            running=False
            
    pass

    #quit pygame
    pygame.quit()
    sys.exit()

main()