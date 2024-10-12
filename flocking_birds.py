import pygame
import numpy as np
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio
from classes import boid
from copy import deepcopy

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


# typedef to create vector in easy way
# c = rmath.c

WIDTH, HEIGHT=1200, 800
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(clr.WHITE)
win.framerate = 30

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(0, 0, WIDTH, HEIGHT-30, False)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

# Sruface for other text, button : 400*200
ui = frame.Surface(0, app.h, win.w, win.h - app.h)
# hiding borer of ui surface
ui.hideBorder()

# -------------- Simulation Controling Variable Section ---------------

# ------------------ Preload Images and Others Section ----------------------
fontObj = rio.load_font(size=16)
input_box = rio.InputBox(ui, (0, 0, ui.w, ui.h), font_color=clr.BLACK, bg_color=clr.PINK )
sliderA = rio.Slider(app, 0.1, 3, 1.2, w = 120, r=6, h = 1, bar_color=(0, 0, 0))
sliderC = rio.Slider(app, 0.1, 3, 0.6, w = 120, r=6, h = 1, bar_color=(0, 0, 0))
sliderS = rio.Slider(app, 0.1, 3, 1, w = 120, r=6, h = 1, bar_color=(0, 0, 0))
# ------------------- Simulation Entities Variable Section --------------------
agents = []
total_agents = 100
aggregation_factor = 1.2
cohesion_factor = 0.6
separation_factor = 1


# ----------------  INITILIZATION  ----------------
def initialize_birds():
    global agents
    agents = []
    for i in range(total_agents):
        x = np.random.randint(0, app.w)
        y = np.random.randint(0, app.h)
        bird = boid.Boid(x, y)
        bird.velocity = np.random.uniform(-2, 2, 2)
        agents.append(bird)

initialize_birds()

# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global cohesion_factor, separation_factor, aggregation_factor, \
            total_agents
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background((200, 200, 200))
    # ui.background(clr.LIGHT_GRAY)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************

    current_agents = deepcopy(agents)

    for agent in agents:
        force = agent.flocking(current_agents, 
                               aggregation_factor, 
                               cohesion_factor, 
                               separation_factor)

        agent.apply_force(force)
        agent.boundary(app.w, app.h)

        agent.update()
        agent.show(pen)


    if text := input_box.getInput():
        text = rio.InputBox.process_cmd(text)
        print(text)
        if text[0] == 'factorA':
            aggregation_factor = float(text[1])
        elif text[0] == 'factorC':
            cohesion_factor = float(text[1])
        elif text[0] == 'factorS':
            separation_factor = float(text[1])
        elif text[0] == 'agent':
            total_agents = int(text[1])
            initialize_birds()
        elif text[0] == 'reset':
            initialize_birds()


    sliderA.show(220, 30)
    sliderC.show(220, 45)
    sliderS.show(220, 60)

    aggregation_factor = sliderA.value
    cohesion_factor = sliderC.value
    separation_factor = sliderS.value

    rio.FONT_OPT['size'] = 12
    rio.println(app, f'Total Birds = {total_agents}', (10, 10))
    rio.println(app, f'Aggregation Factor = {aggregation_factor:.3f}', (10, 25))
    rio.println(app, f'Cohesion Factor = {cohesion_factor:.3f}', (10, 40))
    rio.println(app, f'Separation Factor = {separation_factor:.3f}', (10, 55))


    # update window or chaging the current frame by next one
    input_box.show()
    # this is the end step of this function
    win.blitSurfaces(app, ui)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    # global

    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
            return

        # print(event)

        input_box.update(event)
        sliderA.update(event)
        sliderC.update(event)
        sliderS.update(event)

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
    win.setEventsHandler(event_handler)
    main_loop()

