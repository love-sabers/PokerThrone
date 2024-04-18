import pygame
import time

LEFTTOP = 0
CENTER = 1
class Button(object):
    """
    A button, could be short compressed
    self.status:
        -1 hide
        0 disable
        1 enable
        2 becompressed 
    """
    def __init__(self, pos, image_file,image_cx,option=LEFTTOP):
        self.status = 1
        self.image_cx = image_cx

        # 设定底图，每一种 status 一张。
        if image_file is None:
            self.image = None
            self.image_width = 0
            self.image_heigh = 0
        else:
            self.image = pygame.image.load(image_file)
            self.image_set = []

            image_rect = self.image.get_rect()
            width = int(image_rect.width / image_cx)

            x = 0
            for i in range(self.image_cx):
                self.image_set.append(self.image.subsurface((x, 0), (width, image_rect.height)))
                x += width

            self.image_heigh = image_rect.height
            self.image_width = width
        if(option==CENTER):
            self.rect = pygame.Rect(pos[0]-int(self.image_width/2),\
                                    pos[1]-int(self.image_heigh/2),\
                                    self.image_width,\
                                    self.image_heigh)
        else:
            self.rect = pygame.Rect(pos[0],\
                                    pos[1],\
                                    self.image_width,\
                                    self.image_heigh)


    def render(self, surface):
        #print(self.image_set)
        if self.status >= 0:
            if self.image is not None:
                if self.status < self.image_cx:
                    surface.blit(self.image_set[self.status], (self.rect.left, self.rect.top))

    def is_over(self, point):
        if self.status <= 0:
            bflag = False      # disabled
        else:
            bflag = self.rect.collidepoint(point)
        return bflag

    def check_click(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(event.pos):
            self.selected()
            self.render(screen)
            pygame.display.update()
            time.sleep(0.1)
            self.enabled()
            self.render(screen)
            pygame.display.update()

            return 1
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
    def __init__(self, rect, image_file, image_cx):
        super().__init__(rect, image_file, image_cx)
    def render(self, surface):
        #print(self.image_set)
        if self.status >= 0:
            if self.image is not None:
                if self.status < self.image_cx:
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
    def check_click(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(event.pos):
            self.status=3-self.status
            self.render(screen)
            pygame.display.update()
            return 1
        else:
            return 0
    def is_selected(self):
        return self.status==2