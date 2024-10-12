import pygame
import numpy as np
from lib import color as c
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio

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
app = frame.Surface(0, 0, WIDTH, HEIGHT)
# using this pen we can draw some figure on main screen
pen = shape.AShape(app)

font = pygame.font.SysFont('CodeNewRoman Nerd Font', 14)
input_box = rio.InputBox(app, (0, HEIGHT-30, WIDTH, 30))
# -------------- Global Variable section ---------------

X = np.zeros(0)
Y = np.zeros(0)
a = 0
b = 0
dJa = 0
dJb = 0
learning_rateA = 0.05
learning_rateB = 0.000001
iteration = 0


# ----------------  INITILIZATION  ----------------



# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global a, b, dJa, dJb, learning_rateA, learning_rateB, X, Y, iteration
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    app.background(c.POWDER_BLUE)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ main function ----------------------------
    # *******************************************************************
    N = X.size

    try:
        dJa = (-2/N) * np.sum((Y - a - b*X))

    except ZeroDivisionError:
        dJa = 0
    
    try:
        dJb = (-2/N) * np.sum(X * (Y - a - b*X))
    except ZeroDivisionError:
        dJb = 0
    

    a = a - learning_rateA * dJa
    b = b - learning_rateB * dJb


    iteration += 1
    # *******************************************************************
    # ----------------------- drawing on canvus --------------------------
    # *******************************************************************
    pen.stroke(c.BLACK)
    x1, x2 = 0, WIDTH
    y1 = b * x1 + a
    y2 = b * x2 + a
    pen.Aline(x1, y1, x2, y2)

    pen.fill(c.RED)
    pen.noStroke()
    for x, y in zip(X, Y):
        pen.Acircle(x, y, 5)
    

    rio.println(app, f'Iteration no : {iteration}', (10, 10))
    rio.println(app, f'learning rateA = {learning_rateA}', (10, 25))
    rio.println(app, f'learning rateB = {learning_rateB}', (10, 40))
    sign = '+' if b >=0 else '-'
    rio.println(app, f'Equation, y = {a:.3f} {sign} {abs(b):.3f}x', (10, 55))

    # *******************************************************************
    # ----------------------- input processing --------------------------
    # *******************************************************************
    if text := input_box.getInput():
        text = list(map(lambda t : t.strip(), text.split('=')))
        if text[0] == 'rateA':
            learning_rateA = float(text[1])
        if text[0] == 'rateB':
            learning_rateB = float(text[1])
        elif text[0] == 'reset':
            X = np.zeros(0)
            Y = np.zeros(0)
            a, b = 0, 0
            learning_rateA = 0.01
            learning_rateB = 0.000001
            iteration = 0
        elif text[0] == 'clear':
            X = np.zeros(0)
            Y = np.zeros(0)
            a, b = 0, 0
            iteration = 0


    input_box.show()
    # update window or chaging the current frame by next one
    # this is the end step of this function
    win.blitSurfaces(app)




# -------------- handling keyboard/mouse event -----------
def event_handler():
    global X, Y, a, b, learning_rateA, learning_rateB, iteration
    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
            return

        input_box.update(event)

        if event.type == pygame.MOUSEBUTTONDOWN and not input_box.focused:
            mx, my = utl.mouse()
            X = np.append(X, mx)
            Y = np.append(Y, my)
            # a, b = 0, 0
            iteration = 0

        key = win.key_pressed(event)
        if key and not input_box.focused:
            if key == frame.KEYS['c']:
                X = np.zeros(0)
                Y = np.zeros(0)
                a, b = 0, 0
                iteration = 0
            elif key == frame.KEYS['s']:
                # for x, y in zip(X, Y):
                #     print(f'({x}, {y})', end=',')
                # print()
                print([int(x) for x in X])
                print([int(y) for y in Y])
                
            elif key == frame.KEYS['p']:
                pass




if __name__ == "__main__":
    win.setEventsHandler(event_handler)
    main_loop()

