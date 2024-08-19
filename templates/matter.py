from abc import ABC, abstractmethod
import numpy as np
from lib import rmath


class Agent2D(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.position = np.zeros(2)
        self.velocity = np.zeros(2)
        self.acc = np.zeros(2)
        self.maxV = 5
        self.maxF = 0.2
        self.angle = 0

    def update(self):
        self.velocity += self.acc
        self.velocity = rmath.limit(self.velocity, self.maxV)
        self.angle = rmath.heading(self.velocity)
        self.position += self.velocity
        self.acc *= 0

    def steer(self, desired, damping=1):
        """
        Return the force vector for given direction vector.
        """
        desired = rmath.set_mag(desired, self.maxV)

        steer =  desired - self.velocity
        steer = rmath.limit(steer, self.maxF) # this is most important
        steer *= damping
        return steer
    
    def seek(self, target, dir=1, damping=1):
        desired = target - self.position
        desired *= dir
        force = self.steer(desired, damping)
        return force
    
    def apply_force(self, force):
        self.acc += force
    
    @abstractmethod
    def show(self):
        pass


def boundary2(obj : Agent2D, w, h, d=20, damping=1):
    x, y = obj.position
    target = np.array([w/2, h/2])  

    if x < d:
        desired = np.array([obj.maxV, obj.velocity[1]])
    elif x > w-d:
        desired = np.array([-obj.maxV, obj.velocity[1]])
    elif y < d:
        desired = np.array([obj.velocity[0], obj.maxV])
    elif y > h-d:
        desired = np.array([obj.velocity[1], -obj.maxV])
    else:
        return np.zeros(2)

    desired = rmath.set_mag(desired, obj.maxV)
    steer = desired - obj.velocity
    steer = rmath.limit(steer, obj.maxF)
    steer *= damping

    return steer