import pygame
import sys
import MeauClass
from MeauClass import MainMeau
from GameClass import Game
from Const import Config

def main():
    #init pygame
    pygame.init()
    screen=pygame.display.set_mode(Config.WINDOW_SIZE)
    clock=pygame.time.Clock()
    running=True
    
    #Game
    meau=MainMeau()
    while(running):
        choice=meau.run(screen)

        if(choice==MeauClass.PLAY):
            game=Game(screen)
            game.game()
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