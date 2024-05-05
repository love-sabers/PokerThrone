import pygame
import time
import os
from typing import Dict, Tuple, Sequence,List

LEFTTOP = 0
CENTER = 1
RIGHTTOP = 2
LEFTCENTER = 3
RIGHTCENTER = 4
PATH_IN = 5 # 从路径读取图片
FILE_IN = 6 # 从变量获取图片
LIST_IN = 7 # 直接传入图片

class ImageSet(object):
    def __init__(self,
                pos:Tuple[int,int],
                image_file:str|pygame.Surface|List[pygame.Surface],
                image_cx:int,
                option=LEFTTOP,
                mode=PATH_IN) -> None:
        self.status = 0
        self.image_cx = image_cx

        # 设定底图，每一种 status 一张。
        if image_file is None:
            self.image = None
            self.image_width = 0
            self.image_heigh = 0
        else:

            #按照规则读取文件
            
            if mode == PATH_IN:
                if type(image_file)==str :
                    if os.path.exists(image_file) :
                        self.image = pygame.image.load(image_file)
                    else:
                        raise Exception('No such file: '+image_file)
                else:
                    raise Exception("image_file is not a image path")
            elif mode == FILE_IN :
                if isinstance(image_file, pygame.Surface) :
                    self.image=image_file
                else:
                    raise Exception("image_file is not a surface")
            elif mode == LIST_IN :
                if isinstance(image_file, list) and all(isinstance(item, pygame.Surface) for item in image_file):
                    if(len(image_file)!=0):
                        self.image=1
                        self.image_set=image_file
                    else:
                        raise Exception("image_file is empty")
                else:
                    raise Exception("image_file is not a surface list")
            else:
                raise Exception('No such mode')

            if mode == LIST_IN :
                self.image_heigh = self.image_set[0].get_rect().height
                self.image_width = self.image_set[0].get_rect().width
            else :
                self.image_set = []
                image_rect = self.image.get_rect()
                width = int(image_rect.width / image_cx)
                x = 0
                for i in range(self.image_cx):
                    self.image_set.append(self.image.subsurface((x, 0), (width, image_rect.height)))
                    x += width
                self.image_heigh = image_rect.height
                self.image_width = width

            self.set_pos(pos,option)
    def render(self, surface:pygame.Surface):
        if self.status >= 0:
            if self.image is not None:
                if self.status < self.image_cx:
                    surface.blit(self.image_set[self.status], (self.rect.left, self.rect.top))
    def set_pos(self,pos:Tuple[int,int],option=LEFTTOP):
        if option == LEFTTOP :
            self.rect = pygame.Rect(pos[0],\
                                    pos[1],\
                                    self.image_width,\
                                    self.image_heigh)
        elif option==CENTER :
            self.rect = pygame.Rect(pos[0]-int(self.image_width/2),\
                                    pos[1]-int(self.image_heigh/2),\
                                    self.image_width,\
                                    self.image_heigh)
        elif option==RIGHTTOP :
            self.rect = pygame.Rect(pos[0]-self.image_width,\
                                    pos[1],\
                                    self.image_width,\
                                    self.image_heigh)
        elif option==LEFTCENTER :
            self.rect = pygame.Rect(pos[0],\
                                    pos[1]-int(self.image_heigh/2),\
                                    self.image_width,\
                                    self.image_heigh)
        elif option==RIGHTCENTER :
            self.rect = pygame.Rect(pos[0]-self.image_width,\
                                    pos[1]-int(self.image_heigh/2),\
                                    self.image_width,\
                                    self.image_heigh)
        else :
            raise Exception("No such option")
    def change_status(self,value:int):
        self.status=value

class Button(ImageSet):
    """
    A button, could be short compressed
    self.status:
        -1 hide
        0 disable
        1 enable
        2 becompressed 
    """
    def __init__(self, 
                pos: Tuple[int],
                image_file: str | pygame.Surface | List[pygame.Surface], 
                image_cx: int, 
                option=LEFTTOP, 
                mode=PATH_IN) -> None:
        super().__init__(pos, image_file, image_cx, option, mode)
        self.status=1

    def is_over(self, point):
        if self.status <= 0:
            bflag = False      # disabled
        else:
            bflag = self.rect.collidepoint(point)
        return bflag

    def check_click(self, event):
        if(self.status<=0):
            return 0
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(event.pos):
            self.selected()
            return 0
        elif event.type == pygame.MOUSEBUTTONUP :
            flag=0
            if self.status == 2 and self.is_over(event.pos):
                flag=1
            self.enabled()
            return flag
        else:
            return 0

    def hide(self):
        self.status = -1

    def disabled(self):
        self.status = 0

    def enabled(self):
        self.status = 1

    def selected(self):
        self.status = 2

    def is_selected(self):
        return self.status==2


class Rod(Button):
    """
    A button, could be selected
    self.status:
        -1 hide
        0 disable
        1 enable
        2 beselected 
    """

    UPPER_PIX=50#the distance that move up when be selected
    def __init__(self, 
                pos: Tuple[int],
                image_file: str | pygame.Surface | List[pygame.Surface], 
                image_cx: int, 
                option=LEFTTOP, 
                mode=PATH_IN) -> None:
        super().__init__(pos, image_file, image_cx, option, mode)
    def render(self, surface:pygame.Surface):
        if self.status >= 0:
            if self.image is not None:
                if(self.status==2):#be selected so move up
                    surface.blit(self.image_set[self.status-1], (self.rect.left, self.rect.top-Rod.UPPER_PIX))
                else:
                    surface.blit(self.image_set[self.status], (self.rect.left, self.rect.top))
    def is_over(self, point):
        if self.status <= 0:
            bflag = False      # disabled
        else:
            if(self.status==2):
                t_point=(point[0],point[1]+Rod.UPPER_PIX)#fix the area of the card
                bflag = self.rect.collidepoint(t_point)
            else:
                bflag = self.rect.collidepoint(point)
        return bflag
    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(event.pos):
            self.status=3-self.status
            return 1
        else:
            return 0
    def is_selected(self):
        return self.status==2