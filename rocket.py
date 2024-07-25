import pygame
import numpy as np
from lib import color as c
from lib import frame
from lib import shape
from lib import rmath as r
from lib import utils as utl
from lib import rio
from classes import Rocket, obstracle

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"

WIDTH, HEIGHT=500, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(c.WHITE)
win.framerate = 30

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(0, 0, WIDTH, 550, False)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

# Sruface for other text, button : 400*200
ui = frame.Surface(0, app.h, win.w, win.h - app.h)
# hiding borer of ui surface
ui.border({'hide':True})

# -------------- Simulation Controling Variable Section ---------------
rio.set_font_color(c.ANTIQUE_WHITE)
PUASE_SIMUALTION = False
SHOW_INFO = True

# ------------------ Preload Images and Others Section ----------------------
bg = utl.image('./assets/image/space.jpg', (app.w, app.h))
moon = utl.image('./assets/image/moon-64px.png', (32, 32))
rocket_texture = utl.image('./assets/image/rocket-64px.png', (20, 30))

# ------------------- Simulation Entities Variable Section --------------------
dna_lenght = 350
dna_counter = 0
popsize = 15
population = []
generation_number = 0
target_position = r.c(350, 50)
candidate_index = []
mutation_rate = 15
initial_position = r.c(200, 500)
brick1 = obstracle.SolidBody((120, 200), 120, 20)
brick2 = obstracle.SolidBody((240, 120), 200, 20)

# ----------------  INITILIZATION  ----------------

for i in range(popsize):
    rkt = Rocket.Rocket(rocket_texture, *initial_position)
    rkt.dna.random(dna_lenght)
    population.append(rkt)


rkt = Rocket.Rocket(rocket_texture, *initial_position)
rkt.dna.random(dna_lenght)

# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global dna_counter, population, PUASE_SIMUALTION, generation_number, SHOW_INFO
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background((32, 32, 32))
    # app.surface.blit(bg, (0,0))
    ui.background(c.LIGHT_GRAY)
    # completed backgound fill

    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************
    brick1.show(pen)
    brick2.show(pen)
    app.render(moon, 0, *target_position)



    rkt.calculate_fitness(target_position)
    rkt.draw_ray(pen, [brick1, brick2])
    rkt.show(pen)


    
    # *******************************************************************
    # ------------------ Selection and Reproduction ---------------------
    # *******************************************************************

    
        
    # *******************************************************************
    # ---------------------- Printing Some Stuff ------------------------
    # *******************************************************************

    rio.println(app, f'Reading at : {dna_counter}', (10, 10))
    rio.println(app, f'Moon Distance : {np.linalg.norm(rkt.position - target_position):.4f}', (10, 25))
    rio.println(app, f'Fitness : {rkt.dna.fitness:.4f}%', (10, 40))


    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blit_surface(app, ui)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    global PUASE_SIMUALTION, SHOW_INFO

    # Process events within the loop
    for event in win.events():
        if win.check_for_quit(event):
            return


        keys = pygame.key.get_pressed()

        if keys[frame.KEYS['w']]:
            # rkt.steer_at((0, -1))
            rkt.update2(1)

        if keys[frame.KEYS['a']]:
            rkt.angle += 5

        if keys[frame.KEYS['s']]:
            # rkt.steer_at((0, 1))
            rkt.update2(-1)

        if keys[frame.KEYS['d']]:
            rkt.angle -= 5

        if keys[frame.KEYS['left']]:
            rkt.position[0] -= 5
        if keys[frame.KEYS['right']]:
            rkt.position[0] += 5

        if keys[frame.KEYS['space']]:
            rkt.brake()
        


        # key = win.key_pressed(event)
        # if key:
        #     if key == frame.KEYS['up']:
        #         pass
        #     elif key == frame.KEYS['down']:
        #         pass
        #     elif key == frame.KEYS['left']:
        #         pass
        #     elif key == frame.KEYS['c']:
        #         print('\033c', end="")
        #     elif key == frame.KEYS['p']:
        #         rkt.summary()




if __name__ == "__main__":
    win.set_events_handlers(event_handler)
    main_loop()

