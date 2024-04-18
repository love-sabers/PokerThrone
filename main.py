import pygame
import sys
from Const import GameEvent
from Const import Config
from Game import Game
from GUI import Button
def main():
    #init pygame
    pygame.init()
    screen=pygame.display.set_mode(Config.WINDOW_SIZE)
    clock=pygame.time.Clock()
    running=True

    #meau circulate
    t=Button((0,0,380,260),'source/start.drawio.png',3)
    # image = pygame.image.load('source/start.drawio.png')
    # rect=image.get_rect()
    # screen.blit(image,rect)
    # t.render(screen)
    while(running):
        t.render(screen)
        pygame.display.update()
        #select mode

        #mode run
        

        clock.tick(60)
        #quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if(t.check_click(event)):
                running = False
        pass
    pass

    #quit pygame
    pygame.quit()
    sys.exit()

main()