from abc import ABC, abstractmethod
import numpy as np
from lib import rmath


class Matter2D(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.position = np.zeros(2)
        self.velocity = np.zeros(2)
        self.acc = np.zeros(2)
        self.maxV = 5
        self.maxF = 0.5
        self.angle = 0

    def update(self):
        self.velocity += self.acc
        self.velocity = rmath.limit(self.velocity, self.maxV)
        self.position += self.velocity
        self.acc *= 0
    
    def apply_force(self, force):
        self.acc += force
    
    @abstractmethod
    def show(self):
        pass