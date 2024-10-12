import lib.shape


class SolidBody:
    def __init__(self, pos, w, h, color=(255, 99, 71)) -> None:
        self.position = pos
        self.w = w
        self.h = h
        self.color = color

    def boundary(self):
        x1, y1 = self.position
        return [
            (x1, y1),
            (x1+self.w, y1),
            (x1 + self.w, y1 + self.h),
            (x1, y1 + self.h),  
        ]

    def show(self, pen:lib.shape.AShape) -> None:
        pen.fill(self.color)
        pen.noStroke()
        pen.rect(*self.position, self.w, self.h)
    

        