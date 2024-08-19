from abc import ABC, abstractmethod
import pygame
import numpy as np


class RSurface():
    def __init__(self, x, y, w, h, alpha=True) -> None:
        self.pos = (x, y)
        self.w = w
        self.h = h

    def blit(self, surface, position):
        self.surface.blit(surface, position)

    def blitSurfaces(self, *screens):
        for screen in screens:
            self.surface.blit(screen.surface, screen.pos)

    def render(self, surface, angle, x, y, mode='c'):
        # drawing from, mode = (c)enter | (t)opleft
        if mode == 'c':
            if angle == 0:
                rect = surface.get_rect(center=(x, y))
                self.surface.blit(surface, rect.topleft)
                return
            
            temp_image = pygame.transform.rotate(surface, angle)
            rect = temp_image.get_rect(center=(x, y))
            self.surface.blit(temp_image, rect.topleft)
            
        else :
            if angle == 0:
                rect = surface.get_rect(topleft=(x, y))
                self.surface.blit(surface, (x, y))
                return
            
            temp_image = pygame.transform.rotate(surface, angle)
            orect = surface.get_rect(topleft=(x, y))
            rect = temp_image.get_rect(center=orect.center)
            self.surface.blit(temp_image, rect)
