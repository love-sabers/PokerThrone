import pygame
import sys
from Const import GameEvent
from Const import Config
from Game import Game
from GUI import Button
from GUI import Rod
def main():
    #init pygame
    pygame.init()
    screen=pygame.display.set_mode(Config.WINDOW_SIZE)
    clock=pygame.time.Clock()
    running=True

    #meau circulate
    t=Rod((50,100),'source/start.drawio.png',3)

    while(running):
        screen.fill((0,0,0))
        t.render(screen)
        pygame.display.update()
        #select mode

        #mode run
        

        clock.tick(60)
        #quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if(t.check_click(screen,event)):
                running = 1
        pass
    pass

    #quit pygame
    pygame.quit()
    sys.exit()

main()