import pygame
import lib.frame
import lib.rio


WIDTH=600
HEIGHT=400

win = lib.frame.Window(WIDTH, HEIGHT)
win.background_color((32, 32, 32))


lib.rio.fontSize(28)
lib.rio.fontColor((255, 255, 255))

font_obj = lib.rio.load_font()

slider = lib.rio.Slider(win, 0.1, 5, 1, 100, 200, 200)
input_box = lib.rio.InputBox(win, (0, HEIGHT-30, WIDTH, 30))


@win.game_loop
def main():
    


    lib.rio.println(win, f'{slider.value:.4f}', (100, 100))

    if text := input_box.getInput():
        text = eval(text)
        print(text)
        slider.setValue(text)

    slider.show()
    input_box.show()


def handleEvents():

    for event in win.events():
        if win.checkForQuit(event):
            return

        slider.update(event)
        input_box.update(event)

if __name__ == "__main__":
    win.setEventsHandler(handleEvents)
    main()
