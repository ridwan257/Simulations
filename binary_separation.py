import pygame
import numpy as np
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio
from classes.points import Point, T
from lib.templates import neuralnet as nn
# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


# typedef to create vector in easy way
c = rmath.c

WIDTH, HEIGHT=800, 800
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(clr.WHITE)
win.framerate = 60

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
def f(x) : return 0.1 + x
tr = T(WIDTH, HEIGHT) # transform 0-1 value in sruface width and height

brain = nn.Perceptron(2)

points = []
total_points = 120
iteration = 0
# ----------------  INITILIZATION  ----------------
for i in range(total_points):
    p = Point(tr)
    p.randomize(f)
    points.append(p)


print('------------------- Initial Condition ---------------------')
print('brain weight', brain.weights)
for pt in points:

    prob = brain.think([pt.x, pt.y]) 
    new_label = 1 if prob > 0.5 else 0

    print(f'{pt.x=:.4f}, {pt.y=:.4f}| {pt.label=} | {prob=:.4f} |{new_label=}')



# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global iteration
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background(clr.LIGHT_GRAY)
    # ui.background(clr.LIGHT_GRAY)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************

    # print('------------------------')
    for pt in points:
        pt.show(pen)

        prob = brain.think([pt.x, pt.y]) 
        new_label = 1 if prob > 0.5 else 0

        pt.show_prediction(pen, new_label)
        pt.sh = False

    pen.no_fill()
    pen.stroke(clr.BLACK)
    pen.Aline(tr.x(0), tr.y(f(0)), tr.x(1), tr.y(f(1)))



    random_pt = np.random.choice(points)
    brain.train([random_pt.x, random_pt.y], random_pt.label)
    iteration += 1





    w0, w1, w2 = brain.weights
    y1 = - w0 / w2
    y2 = - (w0 / w2) - (w1 / w2)
    pen.stroke(clr.RED)
    pen.Aline(tr.x(0), tr.y(y1), tr.x(1), tr.y(y2))

    rio.println(app, f'y = {y1:.4f} + {- (w1 / w2):.4f}x', (10, 10))
    rio.println(app, f'iteration = {iteration}', (10, 25))
    rio.println(app, f'Learning rate = {brain.learning_rate}', (10, 40))


    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blit_surface(app)



# -------------- handling keyboard/mouse event -----------
def event_handler():
    # global

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
            elif key == frame.KEYS['s']:
                pass
            elif key == frame.KEYS['j']:
                pass
            elif key == frame.KEYS['p']:
                pass




if __name__ == "__main__":
    win.set_events_handlers(event_handler)
    main_loop()

