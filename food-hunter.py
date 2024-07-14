import pygame
import numpy as np
from lib import color as c
from lib import frame
from lib import shape
from lib import utils as utl
from lib import rio
from classes.veichle import VeichleA, Food, reproduce_vehicles

from os import environ
environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"

# main window created
win = frame.Window(w=600, h=600, title="Smart Rocket")
win.set_esc_to_quit()
win.background_color(c.WHITE)



# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(0, 0, win.w, 400)
# setting color on screen
app.background(c.LIGHT_BLUE)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)


# Sruface for other text, button : 400*200
ui = frame.Surface(0, app.h, win.w, win.h - app.h)
ui.background(c.LIGHT_GRAY)
# hiding borer of ui surface
ui.border({'hide':True})

surface1 = pygame.Surface((60,60))
surface1.set_colorkey((0,0,0))
surface1.set_alpha(100)
pygame.draw.circle(surface1, c.YELLOW, (30,30), 30)

PAUSE_SIMULATION = False
# -------------- Global Variable section ---------------
# number of food and poison and a dictionary to keep the record
total_food = 100
total_poison = 70
food_report = {
    'food' : total_food,
    'poison' : total_poison
}
# container for food and popualtion
buckets = []
veichles = []
# total number of vehicle in a current generation
pop_size = 6
total_alive = pop_size
generaion_number = 1
# mutaion rate of dna and track mutaoin info
mutation_rate = 25
mutated_child = 0
# the best vehicle of a generation
best_vehicle_index = -1
# varialbe for track when parent should choose
select_candidate = False
# list of parent index that will reproduce
candidates_index = []
# tark total lifespan of generation
start_time = 0
generation_life_span = 0
# alter
show_perception = False

# ----------------  INITILIZATION  ----------------
# creating food at random location
for i in range(total_food):
    x = np.random.randint(0, app.w + 1)
    y = np.random.randint(0, app.h + 1)
    posistion = np.array([x, y])
    buckets.append(Food(posistion, 'g'))
# these are some bad food
for i in range(total_poison):
    x = np.random.randint(0, app.w + 1)
    y = np.random.randint(0, app.h + 1)
    posistion = np.array([x, y])
    buckets.append(Food(posistion, 'b'))
np.random.shuffle(buckets)

# creating vehicles at random location
for i in range(pop_size):
    x = np.random.randint(0, app.w + 1)
    y = np.random.randint(0, app.h + 1)
    v = VeichleA(x, y)
    v.velocity = np.random.uniform(-2, 2, 2)
    v.dna[0] = np.random.uniform(0, 3)
    v.dna[1] = np.random.uniform(-3, 0)
    v.dna[2] = np.random.randint(0, 100)
    v.dna[3] = np.random.randint(0, 100)
    veichles.append(v)

start_time = pygame.time.get_ticks()
# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global best_health, best_vehicle_index, select_candidate, \
    candidates_index, veichles, PAUSE_SIMULATION, total_alive, \
    generaion_number, food_report, start_time, generation_life_span, \
    mutated_child
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background(c.POWDER_BLUE)
    ui.background(c.LIGHT_GRAY)
    # completed backgound fill

    
    best_health = 0

    # display all food
    Food.show_all(pen, buckets)

    # *******************************************************************
    # ------------------ draw vehicles and update -----------------------
    # *******************************************************************
    for i, v in enumerate(veichles):
        # if any vehicle is dead then go next vehicle
        if v.dead:
            continue
        
        # if vechiles is alive then this bolck will run
        # storing the index of candidate vehicle if total alive is half of population
        if v.health == 0:
            v.dead = True
            total_alive -= 1
            if total_alive < pop_size // 2:
                candidates_index.append(i)
            continue

        # here we finding the index of best vehicle
        if v.health > best_health:
            best_health = v.health
            best_vehicle_index = i
        
        
        # first adding a conditon to check game is paused or not
        # if pause then just veicle should not update but draw
        if not PAUSE_SIMULATION:
            v.health = -0.1
            force, food_report = v.eat(buckets, app.w, app.h)
            force += v.boundary2(app.w, app.h, 5, 1)
            v.apply_force(force)
            v.update()
        if show_perception : v.show(pen)
        else : v.show(pen)

        # print(best_vehicle_index)
        # print(best_health)

    # *******************************************************************
    # -------------------- genation controls ----------------------------
    # *******************************************************************
    # if total_alive == pop_size // 2:
    #     select_candidate = True
    #     print('total alive 4')
    # if len(candidates_index) == 4:
        # print(candidates_index)
    
    if total_alive == 0:
        #calcute the lifespan of previous generation
        generation_life_span = utl.get_elapsed_time(start_time)
        # print('reproducing children....')
        # print('please wait...')
        veichles, mutated_child = reproduce_vehicles(veichles, candidates_index, app.w, app.h, mutation_rate)
        candidates_index = []
        # PAUSE_SIMULATION = True
        total_alive = pop_size
        generaion_number += 1
        # print('Do you want to continue...')
        start_time = pygame.time.get_ticks()










    # *******************************************************************
    # -------------------- diplaying in ui ------------------------------
    # *******************************************************************
    # after counting total veichle, here is showing in ui
    rio.println(ui, f'Current Generation - {generaion_number}', (10, 10))
    rio.println(ui, f'Ancestor Lifespan - {generation_life_span:.2f}s', (10, 25))
    rio.println(ui, f'Total Alive - {total_alive}', (10, 40))
    rio.println(ui, f'Mutation Rate - {mutation_rate}%', (10, 55))
    rio.println(ui, f'Mutated Child - {mutated_child}', (10, 70))
    rio.println(ui, f'Current - {food_report["food"] + food_report["poison"]}', (250, 10))
    rio.println(ui, f'food - {food_report["food"]}/{total_food}', (250, 25))
    rio.println(ui, f'poison - {food_report["poison"]}/{total_poison}', (250, 40))
    
    # if we find the best vechiles then we should print it information
    best_one = veichles[best_vehicle_index]
    if best_vehicle_index > -1:
        rio.println(ui, f'Best One:', (390, 10))
        rio.println(ui, f'Health - {best_one.health:.2f}', (390, 25))
        rio.println(ui, f'Position - {utl.to_string(best_one.position, 1, "|")}', (390,40))
        rio.println(ui, f'Velocity - {utl.to_string(best_one.velocity, 2, "|")}', (390, 55))
        rio.println(ui, f'Factor - {best_one.dna[0]:.2f} | {best_one.dna[1]:0.2f}', (390, 70))
        rio.println(ui, f'Radii - {best_one.dna[2]:.2f} | {best_one.dna[3]:0.2f}', (390, 85))
        # i am marking the best one
        # i only draw if any one is left else no
        if total_alive > 0:
            x, y = best_one.position
            app.render(surface1, 0, x, y)
            best_one.show(pen)

    
    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blit_surface(app, ui)


# -------------- handling keyboard/mouse event -----------
def event_handler():
    global PAUSE_SIMULATION, show_perception

    mx, my = utl.mouse()

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
                show_perception = False if show_perception else True
            elif key == frame.KEYS['j']:
                pass
            elif key == frame.KEYS['p']:
                if PAUSE_SIMULATION:
                    PAUSE_SIMULATION = False
                else : 
                    PAUSE_SIMULATION = True

                

if __name__ == "__main__":
    win.set_events_handlers(event_handler)
    main_loop()
