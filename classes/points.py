import numpy as np
from lib import color
from lib import rmath


class T:
    def __init__(self, w, h) -> None:
        self.width = w
        self.height = h

    def x(self, x):
        return rmath.linear_map(x, 0, 1, 0, self.width)

    def y(self, y):
        return rmath.linear_map(y, 0, 1, self.height, 0)


class Point:
    def __init__(self, tr:T, x=0, y=0) -> None:
        self.x = x
        self.y = y
        self.r = 10
        self.label = 1 # 1 or -1
        self.tr = tr
        self.sh = False

    def randomize(self, func):
        self.x = np.random.rand()
        self.y = np.random.rand()
        if self.y > func(self.x):
            self.label = 1 ## above the line
        else:
            self.label = 0

    def show(self, pen):
        pen.no_fill()
        if self.label == 0:
            pen.stroke(color.HOT_PINK)
        elif self.label == 1:
            pen.stroke(color.LIME_GREEN)
        pen.circle(self.tr.x(self.x), self.tr.y(self.y), self.r)

    def show_prediction(self, pen, new_label):
        if self.sh : print(f'{self.x=:.4f}, {self.y=:.4f}| {self.label=} |{new_label=}', end=' ')
        pen.no_stroke()
        if self.label == new_label:
            if self.sh : print('true')
            pen.fill(color.GREEN)
        
        else:
            if self.sh : print('false')
            pen.fill(color.RED)
        pen.circle(self.tr.x(self.x), self.tr.y(self.y), self.r//2)



