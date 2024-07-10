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

# Initialize Pygame
pygame.init()

# Set up the display
screen = frame.Window(800, 600)
pygame.display.set_caption("Pygame Antialiased Image")
screen.background_color((255, 255, 255))
Apen = shape.AShape(screen, 25)

aa_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
aa_surface.fill((0, 0, 0, 0))
# pygame.draw.aalines(aa_surface, (255, 0, 0, 255), True, [
#     	(w/2, 0), (w, h),
#     	(w/2, 2*h/3), (0, h)
#     ], 1)

pygame.gfxdraw.aacircle(aa_surface, 50, 50, 50, (255, 0, 0))

@screen.game_loop
def main():

    # Draw an antialiased circle
    draw_antialiased_image(screen.surface, (0, 0, 255), 8, (100, 100))
    draw_antialiased_image(screen.surface, (0, 0, 255), 1, (150, 100))
    draw_antialiased_image(screen.surface, (0, 0, 255), 25, (200, 100))


    pygame.draw.aalines(screen.surface,(255, 0, 0),True, [
    	(250+w/2, 100), (250+w, 100+h),
    	(250+w/2, 100+2*h/3), (250, 100+h)
    ], 2)

    # pygame.gfxdraw.filled_polygon(screen.surface, [
    # 	(300+w/2, 100), (300+w, 100+h),
    # 	(300+w/2, 100+2*h/3), (300, 100+h)
    # ], (0, 0, 255))
    # pygame.draw.polygon(screen.surface, "red", [
    # 	(500+w/2, 100), (500+w, 100+h),
    # 	(500+w/2, 100+2*h/3), (500, 100+h)
    # ], 1)
    screen.surface.blit(aa_surface, (500, 100))
    # Apen.no_stroke()
    # Apen.fill((250, 0, 0))
    Apen.no_fill()
    Apen.stroke('blue')
    Apen.Apolygon(0, 0, w, h,
        [
    	(w/2, 0), (w, h),
    	(w/2, 2*h/3), (0, h)
    ], 45, 't')

    Apen.fill((250, 0, 0))
    Apen.no_stroke()
    Apen.Apolygon(0, 0, w, h,
        [
    	(w/2, 0), (w, h),
    	(w/2, 2*h/3), (0, h)
    ], -45, 't')

    
    # Apen.fill('red')
    Apen.strokeWeight(10)

    Apen.no_fill()
    Apen.stroke((0, 0, 255))
    Apen.circle(100, 200, 50)
    Apen.fill((255, 0, 0))
    Apen.Acircle(220, 200, 50)
    Apen.strokeWeight(1)

    pygame.gfxdraw.aacircle(screen.surface, 340, 200, 50, (0, 0, 255))

    # pygame.gfxdraw.aacircle(screen.surface, 280 , 200, 50, (255, 0, 0))



main()

