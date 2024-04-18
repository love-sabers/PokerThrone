import pygame
import GUI
import Const
QUIT=0
PLAY=1
OPTION=2
class MainMeau(object):
    PALY_PATH   ='source/Play.drawio.png'
    OPTION_PATH ='source/Option.drawio.png'
    QUIT_PATH   ='source/Quit.drawio.png'
    def __init__(self):
        self.play=  GUI.Button((540,100),MainMeau.PALY_PATH,3,GUI.CENTER)
        self.option=GUI.Button((540,300),MainMeau.OPTION_PATH,3,GUI.CENTER)
        self.quit=  GUI.Button((540,500),MainMeau.QUIT_PATH,3,GUI.CENTER)
        pass
    def render(self,surface):
        self.play.render(surface)
        self.option.render(surface)
        self.quit.render(surface)
    def run(self,surface):
        while(1):
            self.render(surface)
            pygame.display.update()
            pygame.time.Clock().tick(Const.Config.FPS)
            for event in pygame.event.get():
                if self.play.check_click(surface,event):
                    return PLAY
                elif self.option.check_click(surface,event):
                    return OPTION
                elif self.quit.check_click(surface,event):
                    return QUIT
                if event.type == pygame.QUIT:
                    return QUIT
    