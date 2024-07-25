if [ -z "$1" ]; then
	echo "no file name mentioned..."
	exit
fi

file_name="$1"

if [ -f "$file_name" ]; then
    echo "file exists..."
    exit
fi

if [ -z "$2" ]; then
	echo "no alias mentioned!"
    alias_name="${file_name%.*}"
else
    alias_name="$2"
fi

echo "setting $alias_name as alias....."



echo "creating pygame template..."
echo "File Name - $file_name"


echo "import pygame
import numpy as np
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f\"100,100\"


# typedef to create vector in easy way
c = rmath.c

WIDTH, HEIGHT=500, 600
# main window created
win = frame.Window(WIDTH, HEIGHT, title=\"Hello World\")
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




# ----------------  INITILIZATION  ----------------



# ------------ main game logic ------------
@win.game_loop
def main_loop():
    # global
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background(clr.WHITE_SMOKE)
    # ui.background(clr.LIGHT_GRAY)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************







    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blit_surface(app)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    # global

    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
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




if __name__ == \"__main__\":
    win.setEventsHandler(event_handler)
    main_loop()
" > $file_name



printf "\n\n.PHONY : %s\n%s:\n\tpython3 %s" \
"$alias_name" "$alias_name" "$file_name" >> Makefile
