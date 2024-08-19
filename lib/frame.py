from sys import exit
import pygame
import numpy as np
from templates.abstract import RSurface


# const
ALPHA = pygame.SRCALPHA
KEYS = {
    "esc" : pygame.K_ESCAPE,
    "return" : pygame.K_RETURN,
    "space" : pygame.K_SPACE,
    "right" : pygame.K_RIGHT,
    "down" : pygame.K_DOWN,
    "left" : pygame.K_LEFT,
    "up" : pygame.K_UP,
    "a" : pygame.K_a,
    "b" : pygame.K_b,
    "c" : pygame.K_c,
    "d" : pygame.K_d,
    "e" : pygame.K_e,
    "f" : pygame.K_f,
    "g" : pygame.K_g,
    "h" : pygame.K_h,
    "i" : pygame.K_i,
    "j" : pygame.K_j,
    "k" : pygame.K_k,
    "l" : pygame.K_l,
    "m" : pygame.K_m,
    "n" : pygame.K_n,
    "o" : pygame.K_o,
    "p" : pygame.K_p,
    "q" : pygame.K_q,
    "r" : pygame.K_r,
    "s" : pygame.K_s,
    "t" : pygame.K_t,
    "u" : pygame.K_u,
    "v" : pygame.K_v,
    "w" : pygame.K_w,
    "x" : pygame.K_x,
    "y" : pygame.K_y,
    "z" : pygame.K_z
}

# def __default_event_handler():
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()

def createSurface(w, h):
    return pygame.Surface((w, h), pygame.SRCALPHA)

class Window(RSurface):
    def __init__(self, w=400, h=300, title='Hello World'):
        super().__init__(0, 0, w, h, False)
        self.title = title
        self.__fps = 30
        self.__running = True
        self.__esc_to_exit = True
        self.__clock = pygame.time.Clock()
        
        self.__fill_color = (255, 255, 255)

        pygame.init()
        self.surface = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption(title)
        self.__events = self.__default_event_handler

    def __call__(self):
        return self.surface

    @property
    def framerate(self):
        return self.__fps

    @framerate.setter
    def framerate(self, n):
        self.__fps = n
    
    @property
    def is_running(self):
        return self.__running

    def set_esc_to_quit(self):
        self.__esc_to_exit = True
    
    def __default_event_handler(self):
        for event in pygame.event.get():
            self.checkForQuit(event)

    def events(self):
        return pygame.event.get()


    def background_color(self, rgb):
        self.__fill_color = rgb
    
    def checkForQuit(self, event):
        if event.type == pygame.QUIT or \
            (self.__esc_to_exit and self.key_pressed(event) == KEYS['esc']):
            self.__running = False
            return True
        return False
    
    def setEventsHandler(self, func):
        self.__events = func

    def game_loop(self, draw):
        def wrapper():
            while self.__running :
                # controll frame rate and check for exit 
                self.__clock.tick(self.__fps)
                self.surface.fill(self.__fill_color)
                
                self.__events()
                # main game logic
                draw()

                pygame.display.flip()

            pygame.quit()
            exit()

        return wrapper
         
    def key_pressed(self, event):
        if event.type == pygame.KEYDOWN:
            return event.key
        return None


class Surface(RSurface):
    def __init__(self, x, y, w, h, alpha=True):
        super().__init__(x, y, w, h, alpha)
        self.border_info = {
            "hide" : False,
            "width" : 1,
            "color" : (0,0,0)
        }
        self.surface = pygame.Surface((w, h))
        if alpha:
            self.surface = self.surface.convert_alpha()
            self.surface.fill((0, 0, 0, 0))
            
    def __call__(self):
        return self.surface

    def background(self, color):
        self.surface.fill(color)
        # this draw an border around the surface
        if not self.border_info["hide"]:
            pygame.draw.rect(self.surface, 
                             self.border_info["color"], 
                             (0,0,self.w,self.h), 
                             self.border_info["width"])

    def showBorder(self): self.border_info["hide"] = False
    def hideBorder(self): self.border_info["hide"] = True

    def set_pos(self, x, y):
        self.pos = (x, y)