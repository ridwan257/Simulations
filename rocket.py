from h11 import PAUSED
import pygame
import numpy as np
from lib import color as c
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import pyio
from classes import Rocket

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"

WIDTH, HEIGHT=400, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(c.WHITE)

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(0, 0, 400, 500)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

# Sruface for other text, button : 400*200
ui = frame.Surface(0, app.h, win.w, win.h - app.h)
# hiding borer of ui surface
ui.border({'hide':True})


# -------------- Global Variable section ---------------

dna_lenght = 100
dna_counter = 0
popsize = 15
population = []
target_position = rmath.c(350, 50)
candidate_index = []
mutation_rate = 1
initial_position = rmath.c(app.w/2, app.h)
PUASE_SIMUALTION = False

# ----------------  INITILIZATION  ----------------
bg = pygame.image.load('./assets/image/space.jpg')
bg = pygame.transform.smoothscale(bg, (app.w, app.h))
moon = utl.image('./assets/image/moon-32px.png')
rocket_texture = utl.image('./assets/image/rocket4-64px.png')
rocket_texture = pygame.transform.smoothscale(rocket_texture, (24, 24))
for i in range(popsize):
    r = Rocket.Rocket(rocket_texture, *initial_position)
    r.dna.random(dna_lenght)
    population.append(r)

# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global dna_counter, population, PUASE_SIMUALTION
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background((128, 128, 128))
    # app.surface.blit(bg, (0,0))
    ui.background(c.LIGHT_GRAY)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************
    pen.no_stroke()
    pen.fill(c.ROYAL_BLUE)
    # pen.Acircle(target_position, 10)
    app.render(moon, 0, *target_position)

    if dna_counter < dna_lenght:
        for r in population:
            if not PUASE_SIMUALTION:
                force = r.read_at(dna_counter)
                force += r.boundary2(app.w, app.h, 20, 1)
                r.apply_force(force)
                r.update()
                r.calculate_fitness(target_position)
                print(r.dna.fitness)
            r.show(app)
            
    
        if not PUASE_SIMUALTION: 
            dna_counter += 1
            print()
    
    # *******************************************************************
    # ------------------ Selection and Reproduction ---------------------
    # *******************************************************************
    else:
        print('have been readed...')
        population = Rocket.reproduce(population, initial_position, mutation_rate)
        # for r in population:
        #     r.dna.shuffle()
        #     r.position = rmath.c(app.w/2, app.h)
        #     r.velocity = np.zeros(2)
        #     r.show(app)
        dna_counter = 0
        pygame.time.delay(1000)
            

    # for r in rk:
    #     r.show(app)
    
    
        





    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blit_surface(app, ui)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    global PUASE_SIMUALTION

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
                PUASE_SIMUALTION = False if PUASE_SIMUALTION else True




if __name__ == "__main__":
    win.set_events_handlers(event_handler)
    main_loop()

