import pygame

class Plane2D:
    def __init__(self, size, bg_color = (191,191,191)):
        self.size = size
        self.pos = (0, 0)
        self.bg_color = bg_color
        self.surface = pygame.Surface(self.size)
        self.origin = (size[0] // 2, size[1] // 2)
        self.color = (0,255,0)
        self.stroke_weight = 1
        self.__scl_x = 1
        self.__scl_y = 1
        self.axis_info = {
            "color" : (0, 0, 0),
            "indicate" : True,
            "step" : (10,10),
            "number-show" : True
        }
        #method:
        
        self.surface.fill(self.bg_color)

    def scale(self, sclx, scly):
        # scale x ==> 1 unit is equal to the sclx small box along x-axis
        self.__scl_x = sclx
        self.__scl_y = scly

    def __get_point(self, x, y):
        x *= self.__scl_x
        y *= self.__scl_y
        p = transform(x, y, self.origin, True)
        return p

    def set_pos(self, x, y):
        self.pos = (x, y)
    
    def stroke(self, color):
        self.color = color

    def show_axis(self):
        pygame.draw.line(self.surface, self.axis_info["color"], (0, self.origin[1]), (self.size[0], self.origin[1]))
        pygame.draw.line(self.surface, self.axis_info["color"], (self.origin[0], 0), (self.origin[0], self.size[1]))
        if self.axis_info["indicate"]:
            pass
    
    def point(self, p):
        x1, y1 = self.__get_point(p[0], p[1])
        pygame.draw.circle(self.surface, self.color, (x1, y1), self.stroke_weight)
    
    def points(self, point_list):
        for p in point_list:
            x1, y1 = self.__get_point(p[0], p[1])
            pygame.draw.circle(self.surface, self.color, (x1, y1), self.stroke_weight)

    def line(self, point_list):
        new_list = list(map(lambda p: self.__get_point(p[0], p[1]), point_list))
        pygame.draw.lines(self.surface, self.color, False, new_list, self.stroke_weight)


    def render(self, window):
        window.blit(self.surface, self.pos)
        self.surface.fill(self.bg_color)
        


def transform(x, y, origin, rnd = False):
    newX = origin[0] + x
    newY = origin[1] - y
    return (newX, newY) if not rnd else (round(newX), round(newY))
