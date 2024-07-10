


import lib
import lib.shape


class SolidBody:
    def __init__(self, pos, w, h, color=(255, 99, 71)) -> None:
        self.position = pos
        self.w = w
        self.h = h
        self.color = color

    def show(self, pen:lib.shape.AShape) -> None:
        pen.fill(self.color)
        pen.no_stroke()
        pen.rect(*self.position, self.w, self.h)
    

        