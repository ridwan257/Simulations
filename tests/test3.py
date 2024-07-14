import pygame
import pygame.gfxdraw
import sys
from lib import shape
from lib import frame
from lib import rio
from lib.rio import InputBox

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

aa_surface = frame.Surface(100, 100, 100, 100)
pygame.draw.rect(aa_surface.surface, (0, 0, 0), (0, 0, 100, 100), 1)
# pygame.draw.aalines(aa_surface, (255, 0, 0, 255), True, [
#     	(w/2, 0), (w, h),
#     	(w/2, 2*h/3), (0, h)
#     ], 1)

# pygame.gfxdraw.aacircle(aa_surface, 50, 50, 50, (255, 0, 0))
# pygame.draw.circle(aa_surface, (255, 0, 0), (50, 50), 50, 1)
pygame.font.init()
fontbox = pygame.font.SysFont("Consolas", 14)
box = InputBox(screen, fontbox, (0, 0, 0), (255, 232, 197),(50, 250, 400, 30), (255, 1))
print('hi baby')
print(fontbox.get_linesize())

@screen.game_loop
def main():

    aa_surface.background((0, 0, 0, 0))
    pygame.draw.circle(aa_surface.surface, (255, 0, 0), (50, 50), 50, 1)
    # box.is_focused()
    
    rio.println(aa_surface, f'{box.focused}', (20, 60))



    text = box.show()
    if text:
        print(text)


    screen.surface.blit(aa_surface.surface, (100, 100))


# -------------- handling keyboard/mouse event -----------
def event_handler():
    global PUASE_SIMUALTION, SHOW_INFO

    # Process events within the loop
    for event in screen.events():
        if screen.check_for_quit(event):
            return
        
        box.is_focused(event)  

        key = screen.key_pressed(event)
        if key:
            if box.focused:
                box.update(event)
            elif key == frame.KEYS['up']:
                pass
            elif key == frame.KEYS['down']:
                pass
            elif key == frame.KEYS['left']:
                pass
            elif key == frame.KEYS['right']:
                pass
            elif key == frame.KEYS['s']:
                pass
            elif key == frame.KEYS['o']:
                pass
            elif key == frame.KEYS['p']:
                print('ppp...')





screen.set_events_handlers(event_handler)
main()

