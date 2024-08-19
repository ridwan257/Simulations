import pygame
import numpy as np
from classes.ping import Ball, Bat
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio
from lib.templates.neuralnet import NeuralNetwork

# from os import environ
# for key in environ.keys() : print(key, '->', environ[key])
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


# typedef to create vector in easy way
# c = rmath.c

WIDTH, HEIGHT=800, 400
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color((32, 32, 32))
win.framerate = 30

# -------------- Simulation Controling Variable Section ---------------

class BotPlayer(Bat):
    def __init__(self, x, y=0) -> None:
        super().__init__(x, y)
        self.brain = None




# --------------------------- Preload -------------------------------
pen = shape.AShape(win)
# ------------------- Simulation Entities Variable Section --------------------
ball = Ball(WIDTH//2, HEIGHT//2)
playerL = Bat(0, 100)
playerL.color = clr.GREEN
playerR = Bat(WIDTH - 50, 120)


# ------------ main game logic ------------
@win.game_loop
def main_loop(): 
    global counter

    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************
    
    ball.show(pen)


    playerR.update()
    playerR.show(win)



# -------------- handling keyboard/mouse event -----------
def event_handler():
    global counter

    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
            return

        key = pygame.key.get_pressed()
        if key[frame.KEYS['w']]:
            playerL.move(-1)
        elif key[frame.KEYS['s']]:
            playerL.move(1)
        
        if key[frame.KEYS['o']]:
            playerR.move(-1)
        elif key[frame.KEYS['k']]:
            playerR.move(1)
        elif key[frame.KEYS['j']]:
            playerR.moveX(-1)
        elif key[frame.KEYS['l']]:
            playerR.moveX(1)
        
        if event.type == pygame.KEYUP:
            playerR.move(0)

        key = win.key_pressed(event)
        if key:
            if key == frame.KEYS['space']:
                brain.summary()
            elif key == frame.KEYS['m']:
                brain.save('hello.nn')
            elif key == frame.KEYS['r']:
                brain.randomize()
                counter = 0
        

        
    




if __name__ == "__main__":
    win.setEventsHandler(event_handler)
    main_loop()

