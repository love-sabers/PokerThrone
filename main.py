import pygame
import sys
import Meau
from Meau import MainMeau
from Const import GameEvent
from Const import Config

def main():
    #init pygame
    pygame.init()
    screen=pygame.display.set_mode(Config.WINDOW_SIZE)
    clock=pygame.time.Clock()
    running=True

    #meau circulate
    
    meau=MainMeau()
    while(running):
        screen.fill((0,0,0))
        choice=meau.run(screen)

        if(choice==Meau.PLAY):
            pass
        elif(choice==Meau.OPTION):
            pass
        elif(choice==Meau.QUIT):
            running=False
            
    pass

    #quit pygame
    pygame.quit()
    sys.exit()

main()