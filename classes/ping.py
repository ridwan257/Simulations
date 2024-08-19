import numpy as np
import pygame
import classes.ping
from lib import color, frame, rmath
from lib.shape import AShape

class Ball:
    def __init__(self, x, y) -> None:
        self.__initial_position = rmath.Vec2d(x, y)
        self.position = self.__initial_position.copy()
        self.velocity = np.array([1.0, 0.0])
        self.r = 10
        self.maxV = 10
        self.velocity = rmath.set_mag(self.velocity, self.maxV)
    
    def update(self, w, h):
        x, y = self.position
        if self.position[0] < self.r:
            # self.position = self.__initial_position.copy()
            self.velocity[1] += np.random.uniform(-3, 3)
            self.velocity[0] = np.random.uniform(5, 25)
            # self.velocity[0] *= abs(self.velocity[0])
            self.velocity = rmath.set_mag(self.velocity, self.maxV)
            # return (-1, (x, y))
    
        elif self.position[0] > w - self.r:
            self.position = self.__initial_position.copy()
            return (1, (x, y))
        
        if self.position[1] < self.r or self.position[1] > h - self.r:
            self.velocity *= (1, -1)

        self.position += self.velocity
        return (0, (x, y)) 
    
    def collision(self, other):
        x1 = other.x
        x2 = x1 + other.w
        y1 = other.y
        y2 = other.y + other.h

        x, y = self.position

        if y > y1 and y < y2 and x > x1-self.r and x < x2+self.r:
            self.velocity *= (-1, 1)
        



            


    def show(self, pen:AShape):
        pen.noStroke()
        pen.fill(color.WHITE)
        pen.circle(self.position, self.r)


class Bat:
    def __init__(self, x, y=0) -> None:
        self.w = 20
        self.h = 120
        self.x = x
        self.y = y
        self.dy = 20
        self.direction = 0
        self.color = color.RED
        self.surface = frame.createSurface(self.w, self.h)
        
    def update(self):
        self.y += self.dy * self.direction

    def move(self, direction):
        self.direction = direction
    
    def moveX(self, dir):
        self.x += 15 * dir

    def show(self, window):
        if self.y > window.h - self.h:
            self.y =  window.h - self.h

        if self.y < 0 :
            self.y = 0


        pygame.draw.rect(self.surface, (*color.RED, 100), (0, 0, self.w, self.h))
        window.blit(self.surface, (self.x, self.y))
