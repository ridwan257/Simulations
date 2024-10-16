import pygame
import numpy as np
from lib.color import *
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio
from classes import ant
from scipy.spatial.distance import cdist
from math import inf

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


# typedef to create vector in easy way
c = rmath.c

WIDTH, HEIGHT=850, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(WHITE)
win.framerate = 30

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(250, 0, 600, HEIGHT, False)
app.hideBorder()
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

# Sruface for other text, button : 400*200
ui = frame.Surface(0, 0, 250, win.h)
# hiding borer of ui surface
ui.hideBorder()

# -------------- Simulation Controling Variable Section ---------------
SHOW_BEST = False
DRAW_PATH = True
PAUSE_SIMULATION = False
HIDE_ANTS = False
HIDE_CITIES = False
SHOW_GLOBAL_BEST = False
# ------------------ Preload Images and Others Section ----------------------

font = rio.load_font()
velocity_position = (10, 20)
velocity_text = font.render('Velocity', True, BLACK)
velocity_slider = rio.Slider(ui, 1, 250, 80, 
    x=velocity_text.get_width()+20, 
    y=velocity_position[1] + velocity_text.get_height()/2, 
    w=150, bar_color='#000000', r=6)



##
HOVER_PROPERTIES = {
    'bg_color' : (0, 200, 0, 100),
    # 'font_color' : RED,
    # 'size' : 16,
    'bold' : True
}
best_path_button = rio.Button(ui, (10, 50, 100, 20), 'Show Best', border_radius=4)
best_path_button.setHoverProperties(HOVER_PROPERTIES)

draw_path_button = rio.Button(ui, (120, 50, 100, 20), 'Hide Paths', border_radius=4)
draw_path_button.setHoverProperties(HOVER_PROPERTIES)

hide_ant_button = rio.Button(ui, (10, 75, 100, 20), 'Hide Ants', border_radius=4)
hide_ant_button.setHoverProperties(HOVER_PROPERTIES)

hide_cities_button = rio.Button(ui, (120, 75, 100, 20), 'Hide Cities', border_radius=4)
hide_cities_button.setHoverProperties(HOVER_PROPERTIES)


### 
textbox_x0 = 150

rnd_state_text = font.render('Random Seed', True, BLACK)
rnd_state_pos = (textbox_x0 - 10 - rnd_state_text.get_width(), 120 + 2)
rnd_state_input_box = rio.InputBox(ui, (textbox_x0, 120, 60, 20), holder='...', colon_focus=False)

city_text = font.render('Total Cities', True, BLACK)
city_pos = (textbox_x0 - 10 - city_text.get_width(), 145 + 2)
city_input_box = rio.InputBox(ui, (textbox_x0, 145, 60, 20), holder='...', colon_focus=False)

ant_text = font.render('Total Ants', True, BLACK)
ant_pos = (textbox_x0 - 10 -ant_text.get_width(), 170 + 2)
ant_input_box = rio.InputBox(ui, (textbox_x0, 170, 60, 20), holder='...', colon_focus=False)

alpha_text = font.render('Alpha', True, BLACK)
alpha_pos = (textbox_x0 - 10 - alpha_text.get_width(), 195 + 2)
alpha_input_box = rio.InputBox(ui, (textbox_x0, 195, 60, 20), holder='...', colon_focus=False)

beta_text = font.render('Beta', True, BLACK)
beta_pos = (textbox_x0 - 10 - beta_text.get_width(), 220 + 2)
beta_input_box = rio.InputBox(ui, (textbox_x0, 220, 60, 20), holder='...', colon_focus=False)

evaporation_text = font.render('Evaporation Rate', True, BLACK)
evaporation_pos = (textbox_x0 - 10 - evaporation_text.get_width(), 245 + 2)
evaporation_input_box = rio.InputBox(ui, (textbox_x0, 245, 60, 20), holder='...', colon_focus=False)

pheromone_text = font.render('Initial Pheromone', True, BLACK)
pheromone_pos = (textbox_x0 - 10 - evaporation_text.get_width(), 270 + 2)
pheromone_input_box = rio.InputBox(ui, (textbox_x0, 270, 60, 20), holder='...', colon_focus=False)

elitism_text = font.render('Elitism Factor', True, BLACK)
elitism_pos = (textbox_x0 - 10 - elitism_text.get_width(), 295 + 2)
elitism_input_box = rio.InputBox(ui, (textbox_x0, 295, 60, 20), holder='...', colon_focus=False)

global_factor_text = font.render('Global Evaporation', True, BLACK)
global_factor_pos = (textbox_x0 - 10 - global_factor_text.get_width(), 295 + 2)
global_factor_input_box = rio.InputBox(ui, (textbox_x0, 295, 60, 20), holder='...', colon_focus=False)

exploitation_text = font.render('Exploitation Factor', True, BLACK)
exploitation_pos = (textbox_x0 - 10 - exploitation_text.get_width(), 295 + 2)
exploitation_input_box = rio.InputBox(ui, (textbox_x0, 295, 60, 20), holder='...', colon_focus=False)

submit_param_button = rio.Button(ui, (10, 320, 220, 20), 'Reset Parameter', border_radius=4)
submit_param_button.setHoverProperties(HOVER_PROPERTIES)

pause_button = rio.Button(ui, (10, 345, 220, 20), 'Pause', border_radius=4)
pause_button.setHoverProperties(HOVER_PROPERTIES)

global_best_button = rio.Button(ui, (10, 370, 220, 20), 'Show Global Best', border_radius=4)
global_best_button.setHoverProperties(HOVER_PROPERTIES)


font.set_bold(True)
current_solution_txt = font.render('Current Best Solution', True, BLACK)
font.set_bold(False)
solution_hoder_txt = []


rio.setBold(True)
# Create a random number generator with a fixed seed
rng = np.random.RandomState(335)


# ------------------- Simulation Entities Variable Section --------------------
total_cities = 30
cities = rng.randint(50, min(app.w, app.h)-50, (total_cities, 2))

total_ants = 35
population = ant.AntPopulation(total_ants, total_cities)
population.randomize(cities)

counter = 0
total_ant_cycle = 0



# ----------------  INITILIZATION  ----------------
rnd_state_input_box.setValue(335)
beta_input_box.setValue(population.beta)
alpha_input_box.setValue(population.alpha)
ant_input_box.setValue(population.total_ants)
city_input_box.setValue(total_cities)
evaporation_input_box.setValue(population.evaporation)
pheromone_input_box.setValue(1/5)
elitism_input_box.setValue(1)

distance_matrix = cdist(cities, cities, metric='euclidean')
ferromone_matrix = np.ones((total_cities, total_cities)) / 5




# tant = ant.Ant(15)
# go_to = int(np.random.randint(0, total_cities))
# tant.position = cities[go_to].astype(np.float64)
# tant.current_city = go_to
# tant.visited = [go_to]
# print('starting from', go_to)

best_path = None
best_dist = None
golbal_best_path = []
golbal_min_dist = inf
distance_result = np.zeros(total_ants)
best_ant_collection = []
temp_best_dist = inf


heatmap_surface = frame.Surface(30, 400, 180, 180, True)
heatmap_surface.hideBorder()
heatmap_surface.background(GRAY)

# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global counter, best_path, distance_result, best_dist, SHOW_BEST, DRAW_PATH, \
            PAUSE_SIMULATION, cities, total_cities, total_ants, HIDE_ANTS, \
            solution_hoder_txt, distance_matrix, ferromone_matrix, HIDE_CITIES, total_ant_cycle, \
            best_ant_collection, temp_best_dist, golbal_best_path, golbal_min_dist, \
            SHOW_GLOBAL_BEST
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background('#1c1c1c')
    ui.background(LIGHT_GRAY)
    # heatmap_surface.background(WHITE)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************


    # draw the cities
    if not HIDE_CITIES:
        for i, pt in enumerate(cities, 1):
            pygame.draw.circle(app(), TOMATO, pt, 10, 2)
            rio.fontColor(WHITE)
            # rio.println(app, chr(i), pt-6)
            rio.println(app, str(i), pt-8)



    # calculate next city to go
    # if  go_to == tant.current_city:
    #     go_to = tant.find_next_city(distance_matrix, ferromone_matrix)
    #     print('going to -', go_to)
    # if go_to is not None:
    #     tant.go(cities, go_to)
    # tant.drawPath(app)
    # tant.show(app)

    for i, ant_unit in enumerate(population):
        if not PAUSE_SIMULATION:
            if population.go_to[i] == ant_unit.current_city:
                # population.update_pheromone_local(ferromone_matrix, ant_unit.last_city(), ant_unit.current_city)
                population.go_to[i] = ant_unit.find_next_city(distance_matrix, ferromone_matrix, exploitation=False)

            if population.go_to[i] is not None:
                ant_unit.go(cities, population.go_to[i])

            ## when a ant complete its cycle
            elif not ant_unit.completed_tour:
                ant_unit.completed_tour = True
                dist = 0
                for a, b in ant.pairwise(ant_unit.visited):
                    # dist += abs(cities[a] - cities[b]).sum()
                    dist += np.linalg.norm(cities[a] - cities[b])
                
                distance_result[i] = dist
                total_ant_cycle += 1

                ant_unit.distance_visited = dist


                if dist <= temp_best_dist:
                    temp_best_dist = dist
                    best_ant_collection.append(i)



        if DRAW_PATH : ant_unit.drawPath(app, cities)
        if not HIDE_ANTS: ant_unit.show(app)


    if all(x is None for x in population.go_to) and not PAUSE_SIMULATION:
        idx = np.argmin(distance_result)
        best_path = population.ants[idx].visited[:]
        best_dist = float(distance_result[idx])
        
        # print(temp_best_dist)
        # print(best_ant_collection)
        # print(population.ants[best_ant_collection[-1]].visited[:])
        # if len(best_ant_collection) > 2 : print(population.ants[best_ant_collection[-2]].visited[:])

        if best_dist <= golbal_min_dist:
            golbal_min_dist = best_dist
            golbal_best_path = population.ants[idx].visited[:]



        # population.update_pheromone(distance_matrix, ferromone_matrix, best_ant_collection, temp_best_dist)
        population.update_pheromone2(distance_matrix, ferromone_matrix, golbal_best_path, golbal_min_dist)
        # population.update_pheromone3(ferromone_matrix, golbal_best_path, golbal_min_dist)
        # population.update_pheromone_global(ferromone_matrix, best_ant_collection, temp_best_dist)
        population.randomize(cities)

        ant.draw_heatmap(heatmap_surface, ferromone_matrix, vmin=0)


        counter += 1
        total_ant_cycle = 0
        best_ant_collection = []
        temp_best_dist = inf


    if SHOW_BEST:
        if best_path is not None:
            for a, b in ant.pairwise(best_path):
                pygame.draw.line(app(), '#FF8C00', cities[a], cities[b], 2)
                # pygame.draw.aaline(app(), '#FF8C00', cities[a]+1, cities[b]+1)

    if SHOW_GLOBAL_BEST:
        if golbal_best_path:
            for a, b in ant.pairwise(golbal_best_path):
                pygame.draw.line(app(), '#FF69B4', cities[a], cities[b], 2)
                # pygame.draw.aaline(app(), '#FF8C00', cities[a]+1, cities[b]+1)



    # ui.blit(current_solution_txt, (10, 350))
    # pygame.draw.line(ui(), BLACK, (10, 365), (230, 365))
    # for i, line in enumerate(solution_hoder_txt):
    #     ui.blit(line, (10, 370 + i * 15))


    rio.println(app, f'Iteration no - {counter}', (10, 10))
    if best_dist is not None:
        rio.println(app, f'Min Dist(C|G) - {best_dist:.2f} | {golbal_min_dist:.2f}', (320, 10))
    else:
        rio.println(app, f'Min Dist(C|G) - Inf | Inf', (320, 10))
    rio.println(app, f'Pheromone - {ferromone_matrix.min():.4f} | {ferromone_matrix.max():.4f}', (10, 25))
    rio.println(app, f'Completed - {total_ant_cycle} ', (180, 10))



    ##  ------------ slider -----------------
    if velocity_slider.focused():
        val = round(velocity_slider.getValue())
        population.set_velocity(val)

    velocity_slider.show()
    ui.blit(velocity_text, velocity_position)


    ## ------------- button -----------------

    best_path_button.show()
    if best_path_button.clicked():
        txt = "Hide Best" if best_path_button.getValue()[1] == 'h' else 'Show Best'
        best_path_button.setValue(txt)
        SHOW_BEST = utl.toggle(SHOW_BEST)

    draw_path_button.show()
    if draw_path_button.clicked():
        txt = "Hide Paths" if draw_path_button.getValue()[1] == 'h' else 'Show Paths'
        draw_path_button.setValue(txt)
        DRAW_PATH = utl.toggle(DRAW_PATH)

    hide_ant_button.show()
    if hide_ant_button.clicked():
        txt = "Hide Ants" if hide_ant_button.getValue()[1] == 'h' else 'Show Ants'
        hide_ant_button.setValue(txt)
        HIDE_ANTS = utl.toggle(HIDE_ANTS)

    hide_cities_button.show()
    if hide_cities_button.clicked():
        txt = "Hide Cities" if hide_cities_button.getValue()[1] == 'h' else 'Show Cities'
        hide_cities_button.setValue(txt)
        HIDE_CITIES = utl.toggle(HIDE_CITIES)

    pause_button.show()
    if pause_button.clicked():
        txt = "Pause" if pause_button.getValue()[0] == 'S' else 'Start'
        pause_button.setValue(txt)
        PAUSE_SIMULATION = utl.toggle(PAUSE_SIMULATION)

    
    global_best_button.show()
    if global_best_button.clicked():
        txt = "Hide Global Best" if global_best_button.getValue()[1] == 'h' else 'Show Global Best'
        global_best_button.setValue(txt)
        SHOW_GLOBAL_BEST = utl.toggle(SHOW_GLOBAL_BEST)



    ## ----------- params -------------
    if submit_param_button.clicked():
        total_ant_cycle = 0
        counter = 0

        best_path_button.setValue('Show Best')
        SHOW_BEST = False
        draw_path_button.setValue('Hide Paths')
        DRAW_PATH = True
        global_best_button.setValue('Show Global Best')
        SHOW_GLOBAL_BEST = False
        
        total_ants = int(ant_input_box.getValue())
        population.alpha = float(alpha_input_box.getValue())
        population.beta = float(beta_input_box.getValue())
        population.evaporation = float(evaporation_input_box.getValue())
        population.total_ants = total_ants
        population.elitism_factor = float(elitism_input_box.getValue())

        total_cities = int(city_input_box.getValue())
        population.total_cities = total_cities
        rnd_seed = int(rnd_state_input_box.getValue())
        if rnd_seed == -1:
            cities = np.random.randint(50, min(app.w, app.h)-50, (total_cities, 2))
        else:
            rnd_seed = abs(rnd_seed)
            rng = np.random.RandomState(rnd_seed)
            cities = rng.randint(50, min(app.w, app.h)-50, (total_cities, 2))

        population.randomize(cities)


        init_pheromon_level = float(pheromone_input_box.getValue())
        population.initial_pheromone = init_pheromon_level
        distance_matrix = cdist(cities, cities, metric='euclidean')
        ferromone_matrix = np.ones((total_cities, total_cities)) * init_pheromon_level

        distance_result = np.zeros(total_ants)
        best_dist = None
        best_path = None
        best_ant_collection = []
        temp_best_dist = inf
        golbal_best_path = []
        golbal_min_dist = inf


        pause_button.setValue('Start')
        PAUSE_SIMULATION = True




    rnd_state_input_box.show()
    ui.blit(rnd_state_text, rnd_state_pos)
    city_input_box.show()
    ui.blit(city_text, city_pos)
    ant_input_box.show()
    ui.blit(ant_text, ant_pos)
    alpha_input_box.show()
    ui.blit(alpha_text, alpha_pos)
    beta_input_box.show()
    ui.blit(beta_text, beta_pos)
    evaporation_input_box.show()
    ui.blit(evaporation_text, evaporation_pos)
    pheromone_input_box.show()
    ui.blit(pheromone_text, pheromone_pos)
    elitism_input_box.show()
    ui.blit(elitism_text, elitism_pos)
    submit_param_button.show()





    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blitSurfaces(ui, app, heatmap_surface)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    global SHOW_BEST, DRAW_PATH

    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
            return


        velocity_slider.update(event)
        best_path_button.update(event)
        draw_path_button.update(event)
        pause_button.update(event)
        hide_ant_button.update(event)
        hide_cities_button.update(event)
        global_best_button.update(event)

        rnd_state_input_box.update(event)
        city_input_box.update(event)
        ant_input_box.update(event)
        alpha_input_box.update(event)
        beta_input_box.update(event)
        evaporation_input_box.update(event)
        submit_param_button.update(event)
        pheromone_input_box.update(event)
        elitism_input_box.update(event)


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
            elif key == frame.KEYS['h']:
                DRAW_PATH = utl.toggle(DRAW_PATH)
            elif key == frame.KEYS['p']:
                SHOW_BEST = utl.toggle(SHOW_BEST)




if __name__ == "__main__":
    win.setEventsHandler(event_handler)
    main_loop()

