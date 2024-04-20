import pygame
import GUI
import Const
QUIT=0
PLAY=1
OPTION=2
class MainMeau(object):
    LOGO_PATH   ='source/logo.png'
    PALY_PATH   ='source/play.png'
    OPTION_PATH ='source/option.png'
    QUIT_PATH   ='source/quit.png'
    def __init__(self):
        self.logo=  GUI.ImageSet((540,300),MainMeau.LOGO_PATH,1,GUI.CENTER)
        self.play=  GUI.Button((270,550),MainMeau.PALY_PATH,3,GUI.CENTER)
        self.option=GUI.Button((540,550),MainMeau.OPTION_PATH,3,GUI.CENTER)
        self.quit=  GUI.Button((810,550),MainMeau.QUIT_PATH,3,GUI.CENTER)
        pass
    def render(self,surface):
        self.logo.render(surface)
        self.play.render(surface)
        self.option.render(surface)
        self.quit.render(surface)
    def run(self,surface:pygame.Surface):
        while(1):
            surface.fill((0,0,0))
            self.render(surface)
            pygame.display.update()
            pygame.time.Clock().tick(Const.Config.FPS)
            for event in pygame.event.get():
                if self.play.check_click(event):
                    return PLAY
                elif self.option.check_click(event):
                    return OPTION
                elif self.quit.check_click(event):
                    return QUIT
                if event.type == pygame.QUIT:
                    return QUIT
    