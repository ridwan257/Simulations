import pygame
import pygame.gfxdraw
import sys
from lib import shape
from lib import frame

w = 50
h = 80



def draw_antialiased_image(surface, color, scale, pos):

    high_res_surface = pygame.Surface((scale*w, scale*h), pygame.SRCALPHA)
    points = [
    	(scale*w/2, 0), (scale*w, scale*h),
    	(scale*w/2, 2*scale*h/3), (0, scale*h)
    ]
    pygame.draw.polygon(high_res_surface, color, points, 1)

    aa_surface = pygame.transform.smoothscale(high_res_surface, (w, h))

    surface.blit(aa_surface, pos)


# Set up the display
screen = frame.Window(800, 600)
pygame.display.set_caption("Pygame Antialiased Image")
screen.background_color((255, 255, 255))
pen = shape.AShape(screen, 25)

aa_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
aa_surface.fill((0, 0, 0, 0))
# pygame.draw.aalines(aa_surface, (255, 0, 0, 255), True, [
#     	(w/2, 0), (w, h),
#     	(w/2, 2*h/3), (0, h)
#     ], 1)

pygame.gfxdraw.aacircle(aa_surface, 50, 50, 50, (255, 0, 0))

@screen.game_loop
def main():

    pen.strokeWeight(5)
    pen.Aline(100, 100, 300, 400)
    pen.Aline(100, 100, 300, 100)
    pygame.draw.aaline(screen.surface, (255, 0, 0), (120, 100), (320, 400), 2)
    # pygame.draw.line(screen.surface, (255, 0, 0), (100, 100), (300, 400))
    # prn
    



main()

