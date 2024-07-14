import pygame
import numpy as np
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


# typedef to create vector in easy way
c = rmath.c

WIDTH, HEIGHT=500, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(clr.WHITE)
win.framerate = 30

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(0, 0, WIDTH, HEIGHT)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

# Sruface for other text, button : 400*200
# ui = frame.Surface(0, app.h, win.w, win.h - app.h)
# hiding borer of ui surface
# ui.border({'hide':True})

# -------------- Simulation Controling Variable Section ---------------

# ------------------ Preload Images and Others Section ----------------------

# ------------------- Simulation Entities Variable Section --------------------
x1, y1, w1, h1 = 100, 100, 80, 50
x2, y2, w2, h2 = 200, 200, 60, 40
a1, a2 = 0, 0
collided = False




# ----------------  INITILIZATION  ----------------



# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global collided
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background(clr.POWDER_BLUE)
    # ui.background(clr.LIGHT_GRAY)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************

    collided = rmath.polygon_colision([(x1+w1/2, y1), (x1+w1, y1+h1), (x1, y1+h1)], 
               [(x2, y2), (x2+w2, y2), (x2+w2, y2+h2), (x2, y2+h2)])


    pen.no_stroke()
    
    if collided : pen.fill(clr.RED)
    else : pen.fill(clr.GREEN)
    pen.Apolygon(x1, y1, w1, h1, [(w1/2, 0), (w1, h1), (0, h1)],  mode='t')
    pen.rect(x2, y2, w2, h2)


    
    
    # pen.fill(clr.GREEN)
    # pen.Acircle(x2, y2, 3)
    # pen.Acircle(x1, y1, 3)






    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blit_surface(app)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    global x1, y1, x2, y2, a1, a2, w1, w2, h1, h2

    # Process events within the loop
    for event in win.events():
        if win.check_for_quit(event):
            return

        key = win.key_pressed(event)
        if key:
            if key == frame.KEYS['up']:
                pass
            elif key == frame.KEYS['down']:
                pass
            elif key == frame.KEYS['left']:
                pass
            elif key == frame.KEYS['right']:
                pass
            elif key == frame.KEYS['w']:
                y1 -= 10
            elif key == frame.KEYS['a']:
                x1 -= 10
            elif key == frame.KEYS['s']:
                y1 += 10
            elif key == frame.KEYS['d']:
                x1 += 10
            elif key == frame.KEYS['q']:
                a1 += 5
            elif key == frame.KEYS['e']:
                a1 -= 5
            elif key == frame.KEYS['i']:
                y2 -= 10
            elif key == frame.KEYS['j']:
                x2 -= 10
            elif key == frame.KEYS['k']:
                y2 += 10
            elif key == frame.KEYS['l']:
                x2 += 10
            
            elif key == frame.KEYS['p']:
               print([(x1+w1/2, y1), (x1+w1, y1+h1), (x1, y1+h1)]) 
               print([(x2, y2), (x2+w2, y2), (x2+w2, y2+h2), (x2, y2+h2)])






if __name__ == "__main__":
    win.set_events_handlers(event_handler)
    main_loop()

