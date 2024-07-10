import pygame
import numpy as np
from lib import frame
from lib import utils as utl
import classes.veichle as veichle
from lib import rmath


win = frame.Window()
win.background_color((255, 255, 255))

#v = veichle.VeichleA(100, 100, 15, 30, (255, 0, 0))
#v.maxF = 0.5
#v.maxV = 8
#v.fill((0, 0, 255))


v2 = veichle.VeichleA(100, 100, 15, 30, (255, 0, 0))
v2.maxF = 0.1
v2.fill((255, 0, 0))
v2.hide_boundary()

# Main function
@win.game_loop
def main():
    
    f = v2.seek(utl.mouse())
    v2.apply_force(f)
    v2.update()
    v2.show(win)
    
    # this is 
    #f = v.seek(utl.mouse(), 0.1)
    #v.apply_force(f)
    #v.update()
    # v.show(win)


    


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
