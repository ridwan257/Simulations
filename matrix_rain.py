import pygame
import numpy as np
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio
from classes.katakana import WaterStream

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


WIDTH, HEIGHT=1000, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Matrix Rain")
win.set_esc_to_quit()
win.background_color(clr.BLACK)
win.framerate = 30

# -------------- Simulation Controling Variable Section ---------------
PAUSE_SIMULATION = False
# ------------------ Preload Images and Others Section ----------------------
font_collection = []
min_font_size = 24
max_font_size = 28
# loading font of different size
for i in range(min_font_size, max_font_size+1):
    f = rio.load_font('./assets/fonts/MS Gothic.ttf', i, False)
    font_collection.append(f)

# ------------------- Simulation Entities Variable Section --------------------
rains = []

# ----------------  INITILIZATION  ----------------
xposition = np.arange(0, WIDTH - max_font_size, max_font_size) + max_font_size
np.random.shuffle(xposition)

N = len(xposition)

for i in range(N):
    r = WaterStream(xposition[i])
    y = np.random.randint(-1500, 0)
    r.init_position(font_collection, y)
    rains.append(r)

# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global rains

    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************
    for stream in rains:
        stream.render(win, PAUSE_SIMULATION)
        if stream.last_char_position() > HEIGHT:
            y = np.random.randint(-250, 0)
            stream.init_position(font_collection, y)



# -------------- handling keyboard/mouse event -----------
def event_handler():
    global rains, PAUSE_SIMULATION

    # Process events within the loop
    for event in win.events():
        if win.check_for_quit(event):
            return

        key = win.key_pressed(event)
        if key:
            if key == frame.KEYS['r']:
                rains = []
                np.random.shuffle(xposition)
                for i in range(N):
                    r = WaterStream(xposition[i])
                    y = np.random.randint(-1500, 0)
                    r.init_position(font_collection, y)
                    rains.append(r)
            elif key == frame.KEYS['p']:
                PAUSE_SIMULATION = utl.toggle(PAUSE_SIMULATION)




if __name__ == "__main__":
    win.set_events_handlers(event_handler)
    main_loop()

