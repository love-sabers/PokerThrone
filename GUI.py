import pygame

class Button(object):
    def __init__(self, rect, image_file,image_cx):
        self.status = 0
        self.rect = pygame.Rect(rect[0],rect[1],rect[2],rect[3])
        self.image_cx = image_cx

        # 设定底图，每一种 status 一张。
        if image_file is None:
            self.__image = None
            self.image_width = 0
        else:
            self.__image = pygame.image.load(image_file)
            self.__image_set = []

            image_rect = self.__image.get_rect()
            width = int(image_rect.width / image_cx)

            x = 0
            for i in range(self.image_cx):
                self.__image_set.append(self.__image.subsurface((x, 0), (width, image_rect.height)))
                x += width

            self.image_width = width

    def render(self, surface):
        #print(self.__image_set)
        if self.status >= 0:
            if self.__image is not None:
                if self.status < self.image_cx:
                    surface.blit(self.__image_set[self.status], (self.rect.left, self.rect.top))

    def is_over(self, point):
        if self.status <= 0:
            bflag = False      # disabled
        else:
            bflag = self.rect.collidepoint(point)
        return bflag

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.is_over(event.pos)

    def hide(self):
        self.status = -1

    def disabled(self):
        self.status = 0

    def enabled(self):
        self.status = 1

    