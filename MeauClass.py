import pygame
import GUI
import Const
import re
import time

from tkinter import simpledialog

QUIT=0
PLAY=1
OPTION=2
class MainMeau(object):
    '''
    主菜单界面
    '''
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
                    return self.log_in()
                elif self.option.check_click(event):
                    return OPTION
                elif self.quit.check_click(event):
                    return QUIT
                if event.type == pygame.QUIT:
                    return QUIT
            
    def log_in(self):
        """
        -点击主菜单的PLAY之后,会弹窗要求输入用户名
        -用户名要求,只含有数字0-9以及26个英语字母,支持大小写
        -不符合要求的用户名会重新弹窗,要求重新输入
        -成功输入返回PLAY,可开始游戏,点击cancel返回QUIT,可退出游戏
        -成功输入后会将当时时间和用户信息写入./source/log.txt中
        """
        self.path = './source/log.txt'
        window = True
        wrong_input = False
        # 输入字符串
        while window:
            if not wrong_input:
                entry_str = simpledialog.askstring(title='用户名输入',
                                                   prompt='用户名中只能含有26个英语字母及其大小写和阿拉伯数字0-9')
            else:
                entry_str = simpledialog.askstring(title='用户名输入',
                                                   prompt='格式错误！请重新输入！\n'
                                                   '用户名中只能含有26个英语字母及其大小写和阿拉伯数字0-9')

            try:
                str = re.search(r'[A-Z0-9a-z]+', entry_str)
            except TypeError:
                return QUIT             # Press Cancel

            try:
                str.group()         # In case of matching nothing
            except AttributeError:
                wrong_input = True
                continue

            if str.group() == entry_str:
                with open(self.path, 'a') as f:
                    f.write(time.asctime(time.localtime(time.time())) + ' ' + entry_str + '\n')
                return PLAY
            else:
                wrong_input = True
