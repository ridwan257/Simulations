import pygame
import pygame.gfxdraw
import numpy as np
from lib import rmath
import lib
import lib.frame

class Shape:
    def __init__(self, surface=None):
        self.surface = surface
        self.color = (255,0,0)
        self._stroke_weight = 1
        self._stroke_color = (0,0,0)
        self._fill = True
        self._stroke = True

    def set_surface(self, surface):
        self.surface = surface

    def fill(self, rgb):
        self.color = rgb
        self._fill = True

    def stroke(self, rgb):
        """
        Function to set stroke color of drawing.

        Parameters:
        rgb -> tuple(r, g, b): color code for stroke line.

        Returns: None
        """
        self._stroke_color = rgb
        self._stroke = True

    def strokeWeight(self, n):
        self._stroke_weight = n
    
    def no_fill(self):
        self._fill = False

    def no_stroke(self):
        self._stroke = False

    def line(self, x1, y1, x2, y2):
        # x1, y1, x2, y2 = to_int(x1, y1, x2, y2)
        if self._stroke:
            pygame.draw.line(self.surface, self._stroke_color, (x1,y1), (x2,y2), self._stroke_weight)

    def lines(self, points):
        # points = list(map(lambda p: to_int(p[0], p[1]), points))
        if self._stroke:
            if len(points) > 1:
                pygame.draw.lines(self.surface, self._stroke_color, False, points, self._stroke_weight)
    
    
    def point(self, x, y):
        # x, y = to_int(x, y)
        if self._stroke:
            pygame.draw.rect(self.surface, self._stroke_color, (x,y,2,2))
    
    def rect(self, x, y, w, h):
        # x, y, w, h = to_int(x, y, w, h)
        if self._fill:
            pygame.draw.rect(self.surface, self.color, (x,y,w,h))
        if self._stroke:
            pygame.draw.rect(self.surface, self._stroke_color, (x,y,w,h), self._stroke_weight)

    def circle(self, *args:tuple)->None:
        """
        Function to draw circle with arguments (x, y, r) or (positoin_vactor, r)
        """
        # x, y, r = to_int(x, y, r)
        if len(args) == 2:
            pos, r = args
        elif len(args) == 3:
            pos, r = args[:2], args[2]
        if self._fill:
            pygame.draw.circle(self.surface, self.color, pos, r)
        if self._stroke:
            pygame.draw.circle(self.surface, self._stroke_color, pos, r, self._stroke_weight)

    def ellipse(self, x, y, a, b):
        x = x - (a/2)
        y = y - (b/2)
        # x, y, a, b = to_int(x, y, a, b)
        if self._fill:
            pygame.draw.ellipse(self.surface, self.color, (x, y, a, b))
        if self._stroke:
            pygame.draw.ellipse(self.surface, self._stroke_color, (x,y,a,b), self._stroke_weight)

    def polygon(self, points):
        # points = list(map(lambda p: to_int(p[0], p[1]), points))
        if self._fill:
            pygame.draw.polygon(self.surface, self.color, points)
        if self._stroke:
            pygame.draw.polygon(self.surface,self._stroke_color, points,self._stroke_weight)



class AShape(Shape):
    def __init__(self, screen : lib.frame.Surface, scale=8):
        super().__init__(screen.surface)
        self.screen = screen
        self.__scale = scale
    
    def Aline(self, x1, y1, x2, y2):
        # x1, y1, x2, y2 = to_int(x1, y1, x2, y2)
        pygame.draw.aaline(self.screen.surface, self._stroke_color, (x1, y1), (x2,y2), 1)

    def Acircle(self, *args:tuple)->None:
        """
        Function to draw circle with arguments (x, y, r) or (positoin_vactor, r)
        """
        # x, y, r = to_int(x, y, r)
    
        if len(args) == 2:
            pos, r = args
        elif len(args) == 3:
            pos, r = args[:2], args[2]

        r = int(r)
        pos = list(map(lambda n:int(n), pos))

        
        high_res_surface = pygame.Surface((self.__scale * 2 * r, self.__scale * 2 * r), pygame.SRCALPHA)
        high_res_surface.fill((0, 0, 0, 0))
        scaled_points = (self.__scale * r, self.__scale * r)

        if self._fill:
            pygame.draw.circle(high_res_surface, self.color, scaled_points, self.__scale*r)
            aa_surface = pygame.transform.smoothscale(high_res_surface, (2*r, 2*r))
            self.screen.render(aa_surface, 0, *pos)
            if self._stroke:
                for i in range(self._stroke_weight):
                    pygame.gfxdraw.aacircle(self.screen.surface, *pos, r-i, self._stroke_color)
            return
        
        if self._stroke:
            for i in range(self._stroke_weight):
                pygame.gfxdraw.aacircle(self.screen.surface, *pos, r-i, self._stroke_color)
        
    
    def Apolygon(self, x, y, w, h, points, angle=0, mode='c'):
        """
        Function to draw circle with arguments (x, y, w, h, points)
        param:
        x, y : positon
        """
        high_res_surface = pygame.Surface((self.__scale * w, self.__scale * h), pygame.SRCALPHA)
        high_res_surface.fill((0, 0, 0, 0))
        scaled_points = [(self.__scale * px, self.__scale * py) for px, py in points]

        if self._fill:
            pygame.draw.polygon(high_res_surface, self.color, scaled_points)
            aa_surface = pygame.transform.smoothscale(high_res_surface, (w, h))
            if self._stroke:
                pygame.draw.aalines(aa_surface, self._stroke_color, True, points, 1)
        
            self.screen.render(aa_surface, angle, x, y, mode)
            return
        
        transformed_points = np.array([(x+dx, y+dy) for dx, dy in points])
        if angle == 0 and mode != 'c':
            pygame.draw.aalines(self.screen.surface, self._stroke_color, True, transformed_points, 2)
            return
        elif angle == 0 and mode == 'c':
            transformed_points -= [w/2, h/2]
            pygame.draw.aalines(self.screen.surface, self._stroke_color, True, transformed_points, 2)
            return

        transformed_points = np.array(points) - [w/2, h/2]
        transformed_points = transformed_points @ rmath.R2d(angle).T
        transformed_points += [x, y]
        if mode != 'c':
            transformed_points += [w/2, h/2]
        pygame.draw.aalines(self.screen.surface, self._stroke_color, True, transformed_points, 2)
        
   
        
