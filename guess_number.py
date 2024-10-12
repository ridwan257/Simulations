import os
from math import ceil, floor
import pygame
import numpy as np
from lib import color as clr
from lib import frame
from lib import shape
from lib import rmath
from lib import utils as utl
from lib import rio
from templates.neuralnet import NeuralNetwork, to_string, toBinary

# from os import environ
# environ['SDL_VIDEO_WINDOW_POS'] = f"100,100"


# typedef to create vector in easy way
# c = rmath.c

WIDTH, HEIGHT=400, 500
# main window created
win = frame.Window(WIDTH, HEIGHT, title="Hello World")
win.set_esc_to_quit()
win.background_color(clr.WHITE)
win.framerate = 30

# not here we are spliting the window into 2 section
# one is for simulation for e.g. 400x400
# another one for some text or other
# Sruface for main simulation for e.g. 400x400
app = frame.Surface(60, 25, 100, 100)
app.background(clr.WHITE_SMOKE)


# Sruface for other text, button : 400*200
ui = frame.Surface(WIDTH - 160, 25, 100, 100)
ui.background(clr.WHITE_SMOKE)
# hiding borer of ui surface
# ui.hideBorder()

# -------------- Simulation Controling Variable Section ---------------
temp_surface = frame.createSurface(25, 25)

# ------------------ Preload Images and Others Section ----------------------
HOVER_PROPERTIES = {
    'bg_color' : (0, 200, 0, 100),
    'font_color' : clr.RED,
    # 'size' : 16,
    'bold' : True
}
# ------------------- Simulation Entities Variable Section --------------------
input_box = rio.InputBox(win, (10, 150, WIDTH-20, 30), bg_color=utl.toRGB(0xffd7e3))
train_btn = rio.Button(win, (10, 190, 80, 25), "Train")
train_btn.setHoverProperties(HOVER_PROPERTIES)
toogle_btn1 = False

think_btn = rio.Button(win, (100, 190, 80, 25), "Load")
think_btn.setHoverProperties(HOVER_PROPERTIES)

btn1 = rio.Button(win, (190, 190, 80, 25), "Save")
btn1.setHoverProperties(HOVER_PROPERTIES)

# ----------------  INITILIZATION  ----------------
drawing = False
prev_position = None
stroke_weight = 2

img_num = 1

# ------------- Load Neural Network -----------------
input_no = 25 * 25
brain = NeuralNetwork(input_no, 32, 10)
# brain.randomize()
# brain = NeuralNetwork.laodFromFile('./assets/guess_num/first_net.nn')
# brain.summary()

train_dict = {
    '0' : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    '1' : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    '2' : [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    '3' : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    '4' : [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    '5' : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    '6' : [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    '7' : [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    '8' : [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    '9' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
}

# ------------ main game logic ------------
@win.game_loop
def main_loop():
    global prev_position, toogle_btn1, img_num, temp_surface
    
    # reset the bacground color so that 
    # previous frame drawing don't pressent
    # app.background(clr.WHITE_SMOKE)
    # ui.background(clr.LIGHT_GRAY)
    # completed backgound fill


    # *******************************************************************
    # ------------------------ drawing on board  --------------------------
    # *******************************************************************
    if drawing:
        x1, y1 = utl.mouse() - app.pos
        if prev_position is None:
            prev_position = (x1, y1)
        # pygame.draw.aaline(app(), clr.BLACK, prev_position, (x1, y1))
        dist = np.linalg.norm(np.subtract( prev_position, (x1, y1)))
        if dist <= stroke_weight :
            pygame.draw.circle(app.surface, clr.BLACK, (x1, y1) , stroke_weight)
        else:
            x0, y0 = prev_position
            n = ceil(dist / stroke_weight)
            for p in range(n + 1):
                q = n - p
                x = ( p * x1 + q * x0 ) / n
                y = ( p * y1 + q * y0 ) / n
                pygame.draw.circle(app.surface, clr.BLACK, (x, y) , stroke_weight)
        prev_position = (x1, y1)

    # grayscale_array = utl.getGrayScaleValue(app.surface)
    # utl.grayScaleToSurface(ui(), grayscale_array)
    # grayscale_array = grayscale_array.flatten()
    # grayscale_array = 1#grayscale_array / 255
    


    # *******************************************************************
    # ------------------------ input-io handle  --------------------------
    # *******************************************************************
    if txt := input_box.getInput():
        txt = rio.InputBox.process_cmd(txt)
        print(txt)
        if txt[0] == 'v':
            train_btn.setValue(txt[1])
        if txt[0] == 'b':
            train_btn.setBoldText(bool(txt[1]))
    

    # if btn1.clicked():
    #     file_path = './assets/guess_num/' + input_box.getValue()
    #     print(file_path)
    #     if os.path.exists(file_path):
    #         print('exists, change name..!')
    #     else:
    #         arr = pygame.surfarray.array2d(app.surface)
    #         grayscale_array = RGBtoGrayscale(arr)
    #         np.save(file_path, grayscale_array)
    #         print('saved!')

    if train_btn.clicked():
        num = input_box.getValue()
        actual_output = train_dict.get(num, None)
        print(num, actual_output)
        if actual_output:
            for _ in range(10000):
                brain.train(grayscale_array, actual_output)
            print('training done...')
            res = brain.think(grayscale_array)
            print(to_string(res, 4))



    # if think_btn.clicked():
    #     print('hi')
    #     # print(grayscale_array.shape)
    #     res = brain.think(grayscale_array)
    #     print(to_string(res, 4))
    #     res = toBinary(res)
    #     print(res)

    if think_btn.clicked():
        name = input_box.getValue() # demo1
        file_name = f"./assets/guess_num/{name}_25x25.np"
        if os.path.exists(file_name):
            arr = np.loadtxt(file_name)
            # arr = converTo25x25(arr)
            arr *= 255
            utl.grayScaleToSurface(temp_surface, arr)
            new_surf = pygame.transform.scale(temp_surface, (100, 100))
            ui.blit(new_surf, (0, 0))
            print(f"{name} loaded succesfully!")
        else:
            print(f"{name} not exist!")


    if btn1.clicked():
        grayscale_array = utl.getGrayScaleValue(app.surface)
        grayscale_array /= 255
        grayscale_array = converTo25x25(grayscale_array)
        num = input_box.getValue()
        if num:
            file_name = f"./assets/guess_num/extra_data/demo{img_num}_{num}_25x25.np"
            np.savetxt(file_name, grayscale_array)
            print(f"demo{img_num}_{num}_25x25.np saved!")
            img_num += 1
        else:
            print('error: enter number')


    
    # update window or chaging the current frame by next one
    # this is the end step of this function
    train_btn.show()
    think_btn.show()
    btn1.show()
    input_box.show()
    win.blitSurfaces(app, ui)



count = 1
# -------------- handling keyboard/mouse event -----------
def event_handler():
    global drawing, prev_position, count

    # Process events within the loop
    for event in win.events():
        if win.checkForQuit(event):
            return


        input_box.update(event)
        train_btn.update(event)
        think_btn.update(event)
        btn1.update(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            prev_position = None

        

        key = win.key_pressed(event)
        if key:
            if key == frame.KEYS['c']:
                app.background(clr.WHITE_SMOKE)
            
            elif key == frame.KEYS['up']:
                folder_name = input_box.getValue()
                file_name = f"./assets/guess_num/{folder_name}/demo{count}_25x25.np"
                if os.path.exists(file_name):
                    arr = np.loadtxt(file_name)
                    arr *= 255
                    utl.grayScaleToSurface(temp_surface, arr)
                    new_surf = pygame.transform.scale(temp_surface, (100, 100))
                    ui.blit(new_surf, (0, 0))
                    print(f"{folder_name}/demo{count} loaded succesfully!")
                else:
                    print(f"{folder_name}/demo{count} not exist!")
                
                count += -1

            elif key == frame.KEYS['down']:
                folder_name = input_box.getValue()
                file_name = f"./assets/guess_num/{folder_name}/demo{count}_25x25.np"
                if os.path.exists(file_name):
                    arr = np.loadtxt(file_name)
                    arr *= 255
                    utl.grayScaleToSurface(temp_surface, arr)
                    new_surf = pygame.transform.scale(temp_surface, (100, 100))
                    ui.blit(new_surf, (0, 0))
                    print(f"{folder_name}/demo{count} loaded succesfully!")
                else:
                    print(f"{folder_name}/demo{count} not exist!")
                    
                count += 1
            
            

            elif key == frame.KEYS['left']:
                pass
            elif key == frame.KEYS['right']:
                pass
            elif key == frame.KEYS['s']:
                arr = pygame.surfarray.array2d(app.surface)
                grayscale_array = utl.RGBtoGrayscale(arr)
                # np.save("./assets/guess_num/number1_200x200.npy", grayscale_array)
            elif key == frame.KEYS['j']:
                arr = np.load("./assets/guess_num/num2_200x200.npy")
                utl.grayScaleToSurface(ui.surface, arr)
            elif key == frame.KEYS['p']:
                brain.save("./assets/guess_num/first_net.nn")
                print('Saved!')



def converTo25x25(arr):
    reshaped_arr = arr.reshape(25, 4, 25, 4)
    new_arr =  reshaped_arr.sum(axis=(1, 3))
    new_arr /= 16
    return new_arr



if __name__ == "__main__":
    win.setEventsHandler(event_handler)
    main_loop()

