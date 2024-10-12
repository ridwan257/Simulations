import numpy as np
from templates.matter import Agent2D
from lib import color


class Boid(Agent2D):
    def __init__(self, x, y, w=12, h=20) -> None:
        super().__init__()
        self.position[:] = (x, y)
        self.w = w
        self.h = h
        self.maxV = 5
        self.maxF = 0.6
        self.perception = 100
        self.__vertices = [
            (w/2, 0), (w, h), (0, h)
        ]
        self.paths = []     

    def boundary(self, w, h):
        is_boundary = False

        if self.position[0] < 0:
            self.position[0] = w
            is_boundary = True
        elif self.position[0] > w:
            self.position[0] = 0
            is_boundary = True
        
        if self.position[1] < 0:
            self.position[1] = h
            is_boundary = True
        elif self.position[1] > h:
            self.position[1] = 0
            is_boundary = True

        if is_boundary:
            self.paths = []
            return
        
        self.paths.append(self.position.copy())

        if len(self.paths) > 20:
            del self.paths[0:2]
    
    

    def flocking(self, others, factorA=1, factorC=1, factorS=1):
        pos = np.zeros(2)
        vel = np.zeros(2)
        direction = np.zeros(2)
        force = np.zeros(2)
        count = 0
        for other in others:
            dist = np.linalg.norm(self.position - other.position)

            if dist < self.perception and dist > 0:
                count += 1
                # aggeregation
                vel += other.velocity
                # cohesion
                pos += other.position
                # separetion
                d = self.position - other.position
                d /=  dist
                direction += d

        if count > 0:
            vel = vel / count
            force += self.steer(vel, factorA)

            pos = pos / count
            force += self.seek(pos, factorC)

            direction = direction / count
            force += self.steer(direction, factorS)

        return force

    def show(self, pen):
        pen.noFill()
        pen.stroke(color.HOT_PINK)
        # pen.circle(self.position, self.perception)

        # for i in range(len(self.paths)-1):
        #     x1, y1 = self.paths[i]
        #     x2, y2 = self.paths[i+1]

            # pen.line(x1, y1, x2, y2)

        pen.noStroke()
        pen.fill(color.CADET_BLUE)
        pen.Apolygon(*self.position, self.w, self.h, self.__vertices, self.angle)
        