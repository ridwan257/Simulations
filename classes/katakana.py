import numpy as np
import pygame
from lib import rio



class Water:
    def __init__(self, font, x, y, velocity=0) -> None:
        self.value = np.random.randint(12448, 12544)
        self.x = x
        self.y = y
        self.velocity = velocity
        self.font = font
        self.first = False
        self.counter = 0
        self.counter_limit = 10
        self.surface = self.font.render(chr(self.value), True, (0, 255, 70))
            
    def set_first(self):
        self.first = True
        self.surface = rio.genarate_pseudo_bold_text(self.font, chr(self.value), (180, 255, 180))


    def update(self):
        self.y += self.velocity
        self.counter += 1
        if self.counter > self.counter_limit:
            self.counter = 0


    def randomize(self):
        if not self.first and self.counter == 1:
            self.value = np.random.randint(12448, 12544)
            self.surface = self.font.render(chr(self.value), True, (0, 255, 70))
            # self.render_pseudo_bold_text()


    def show(self, win):
        win.render(self.surface, 0, self.x, self.y)



class WaterStream:
    def __init__(self, x) -> None:
        self.velocity = 0
        self.size =0
        self.font = None
        self.font_height = 0
        self.font_width = 0
        self.x = x
        self.y = 0  # position of first charecter
        self.water = []
        self.space_index = 0
        
        # self.init_position(w)

    def init_position(self, font_list, y=0):
        self.velocity = np.random.uniform(4, 10)
        self.size = np.random.randint(8, 20)
        self.font = np.random.choice(font_list)
        self.font_height = round(self.font.get_height() * 1.01)
        self.water = []

        for i in range(self.size):
            w = Water(self.font, 
                      self.x, y - i*self.font_height, 
                      self.velocity)
            w.counter_limit = np.random.randint(4, 8)
            # w.render_pseudo_bold_text()
            if i == 0 and np.random.randint(2) == 0: 
                w.set_first()

            self.water.append(w)

    def last_char_position(self):
        # return self.y - self.font_height * self.size
        return self.water[-1].y
    

    def render(self, win, pasueit=False):
        for water in self.water:
            if not pasueit:
                water.update()
                water.randomize()
            water.show(win)
        
