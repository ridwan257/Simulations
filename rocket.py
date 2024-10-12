import pygame
import numpy as np
from lib import color as col
from lib import frame
from lib import shape
from lib import rmath as r
from lib import utils as utl
from lib import rio
from classes import Rocket

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"

WIDTH, HEIGHT=800, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
# win.background_color(col.WHITE)
win.background_color((32, 32, 32))
win.framerate = 60

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(0, 0, WIDTH, HEIGHT, False)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

# Sruface for other text, button : 400*200
# ui = frame.Surface(0, app.h, win.w, win.h - app.h)
# hiding borer of ui surface
# ui.hideBorder()

# -------------- Simulation Controling Variable Section ---------------
rio.fontColor(col.ANTIQUE_WHITE)
rio.fontSize(22)
PUASE_SIMULATION = False
SHOW_INFO = False

# ------------------ Preload Images and Others Section ----------------------
bg = utl.image('./assets/image/space1.jpg', (app.w, app.h))
moon = utl.image('./assets/image/moon-64px.png', (32, 32))
rocket_texture = utl.image('./assets/image/rocket-64px.png', (15, 25))

# ------------------- Simulation Entities Variable Section --------------------
dna_lenght = 300
dna_counter = 0
popsize = 60
population = []
generation_number = 0
target_position = r.c(460, 120)
candidate_index = []
mutation_rate = 2
initial_position = r.c(WIDTH//3, HEIGHT-50)
brick1 = Rocket.Brick((230, 300), 120, 15)
brick2 = Rocket.Brick((380, 200), 200, 15)
brick3 = Rocket.Brick((360, 100), 15, 60)
brick4 = Rocket.Brick((580, 70), 15, 80)
brick1.setTarget(target_position)
brick2.setTarget(target_position)
brick3.setTarget(target_position)
brick4.setTarget(target_position)

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
    global dna_counter, population, PUASE_SIMULATION, generation_number, SHOW_INFO
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background((32, 32, 32))
    app.surface.blit(bg, (0,0))
    # ui.background(col.LIGHT_GRAY)
    # completed backgound fill
    # win.background_color((32,32,32))

    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************
    brick1.show(pen)
    brick2.show(pen)
    brick3.show(pen)
    brick4.show(pen)
    app.render(moon, 0, *target_position)



    # sgn = [brick1.rocketSign(rkt), brick2.rocketSign(rkt)]
 
    # rkt.check_obstracle(brick1)
    # rkt.check_obstracle(brick2)
    # rkt.calculate_fitness(target_position, [brick1, brick2])
    # rkt.draw_ray(pen, [brick1, brick2])
    # rkt.show(pen)
    # rio.println(app, f'Sign : {sgn}', (10, 60))
    # rio.println(app, f'col : {rkt.collapsed}', (10, 80))
    # rio.println(app, f'cross : {rkt.angle}', (10, 100))
    # rio.println(app, f'Moon Distance : {np.linalg.norm(rkt.position - target_position):.4f}', (10, 25))
    # rio.println(app, f'Fitness : {rkt.dna.fitness:.4f}%', (10, 40))


    # pen.stroke(col.WHITE)
    # pen.line(0, brick1.c, WIDTH, brick1.m*WIDTH+brick1.c)
    # pen.line(0, brick2.c, WIDTH, brick2.m*WIDTH+brick2.c)
    # pen.line(0, brick3.c, WIDTH, brick3.m*WIDTH+brick3.c)
    # pen.line(0, brick4.c, WIDTH, brick4.m*WIDTH+brick4.c)
    # print(brick4.m, brick4.c)
    # pen.line(*rkt.position, *target_position)
    
    max_fitness = -1000
    best_rocket = None
    dist = -1.0

    
    if dna_counter != dna_lenght:
        for rkt in population:
            if not rkt.collapsed and not PUASE_SIMULATION and not rkt.reached:
                force = rkt.read_at(dna_counter)
                rkt.apply_force(force)
                rkt.check_obstracle(brick1)
                rkt.check_obstracle(brick2)
                rkt.check_obstracle(brick3)
                rkt.check_obstracle(brick4)
                rkt.calculate_fitness(target_position, [brick1, brick2, brick3, brick4])
                rkt.update()

            if rkt.dna.fitness >= max_fitness and not rkt.collapsed:
                max_fitness = rkt.dna.fitness
                best_rocket = rkt

            if not rkt.collapsed : rkt.show(pen)
        
        if not PUASE_SIMULATION : dna_counter += 1

        if best_rocket is not None:
            pen.noFill()
            # pen.stroke(col.YELLOW)
            # pen.strokeWeight(2)
            # pen.circle(*best_rocket.position, 16)
            # best_rocket.drawPath(pen)
            # best_rocket.show(pen)

            dist = np.linalg.norm(best_rocket.position - target_position)
            # if dist < 16:
            #     PUASE_SIMULATION = True



    

    
    # *******************************************************************
    # ------------------ Selection and Reproduction ---------------------
    # *******************************************************************
    elif not PUASE_SIMULATION:
        population = sorted(population, key=lambda x: x.dna.fitness, reverse=True)
        
        for rkt in population:
            rkt.show(pen)
        
        # pen.noFill()
        # pen.stroke(col.YELLOW)
        # pen.circle(*population[0].position, 20)

        population = Rocket.reproduce(population, initial_position, mutation_rate/100)
        dna_counter = 0
        generation_number += 1
        
    # *******************************************************************
    # ---------------------- Printing Some Stuff ------------------------
    # *******************************************************************

    rio.println(app, f'DNA reading at : {dna_counter}/{dna_lenght}', (380, 5))
    rio.println(app, f'Genaration : {generation_number}', (10, 5))
    rio.println(app, f'Max Fitness : {max_fitness:.2f}', (10, 25))
    rio.println(app, f'Min Distance : {dist:.2f}', (380, 25))
    rio.println(app, f'Mutation Rate : {mutation_rate}%', (10, 45))
    # rio.println(app, f'Pause : {PUASE_SIMULATION}', (10, 70))



    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blitSurfaces(app)
    # win.blitSurfaces(app, ui)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    global PUASE_SIMULATION, SHOW_INFO

    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
            return


        keys = pygame.key.get_pressed()

        if keys[frame.KEYS['w']]:
            # rkt.steer_at((0, -1))
            rkt.update2(1)
            # rkt.position[1] -= 5

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

        # if keys[frame.KEYS['space']]:
        #     PAUSE_SIMULATION = utl.toggle(PAUSE_SIMULATION)
        


        key = win.key_pressed(event)
        if key:
            if key == frame.KEYS['space']:
                PUASE_SIMULATION = utl.toggle(PUASE_SIMULATION)
        #     elif key == frame.KEYS['down']:
        #         pass
        #     elif key == frame.KEYS['left']:
        #         pass
        #     elif key == frame.KEYS['c']:
        #         print('\033c', end="")
        #     elif key == frame.KEYS['p']:
        #         rkt.summary()




if __name__ == "__main__":
    win.setEventsHandler(event_handler)
    main_loop()
    



