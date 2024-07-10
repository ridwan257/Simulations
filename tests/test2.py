import os
import pygame
import numpy as np
from lib import frame
from lib import utils as utl
import classes.veichle as veichle
from lib import rmath
import numpy as np
from lib import shape

# Set the position of the Pygame window on the screen
x_position = 80  # X position on the screen
y_position = 180  # Y position on the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = f"80,180"

win = frame.Window(400, 400)
win.background_color((255, 255, 255))
pen = shape.Shape(win.surface)

v = veichle.VeichleA(200, 200, 15, 30, (255, 0, 0))
v.maxF = 0.5
v.maxV = 8
v.fill((0, 0, 255))
v.hide_boundary()
v.hide_leap_color()
v.velocity = np.array([2.3, 3.8])


v2 = veichle.VeichleA(200, 200, 15, 30, (255, 0, 0))
v2.maxF = v.maxF
v2.fill((255, 0, 0))
v2.hide_boundary()
v2.hide_leap_color()
v2.velocity = v.velocity.copy()

d = 20
# Main function
@win.game_loop
def main():
    
    pen.no_fill()
    pen.rect(d, d, win.w - 2*d, win.h-2*d)

    # f = v2.seek(utl.mouse())
    f = v2.boundary2(win.w, win.h, d)
    v2.apply_force(f)
    v2.update()
    v2.show(win)
    
    # f = v.seek(utl.mouse())
    f = v.boundary(win.w, win.h, d, 0.1)
    v.apply_force(f)
    v.update()
    v.show(win)

    


# def event_handler():
#     # Process events within the loop
#     for event in win.events():
#         if win.check_for_quit(event):
#             return

if __name__ == "__main__":
    # win.set_events_handlers(event_handler)
    main()
    # x = np.array([0.000, 0.000000])
    # print(v.normalizeto(x, 6))
    # print(rmath.limit(x, 6))
    # print(rmath.set_mag(x, 6))
