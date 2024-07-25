import numpy as np
import pygame
import classes
import classes.obstracle
from classes.veichle import VeichleA
from lib import rmath
from lib.templates import dnalib
from lib import color
# from lib import utils as utl


class Rocket:
    def __init__(self, texture, x=150, y=150):
        self.image :pygame.Surface = texture
        self.counter = 0
        self.paths = []
        self.collapsed = False
        self.dna = RocketDNA()
        self.dna.neucleotide = 'lpuqrts'

        self.position = np.array([x, y], dtype=np.float64)
        self.velocity = np.array([0., 0.])
        self.acc = np.zeros(2)
        self.angle = 0
        self.maxV = 6
        self.maxF = 0.4
        
        
    def update(self):
        self.velocity += self.acc
        self.velocity = rmath.limit(self.velocity, self.maxV)
        self.position += self.velocity
        self.acc *= 0
        self.paths.append(self.position.copy()) 

        self.angle = rmath.heading(self.velocity)
        
        
    def update2(self, direction):
        a = np.deg2rad(-self.angle)
        
        self.position[0] += direction * self.maxV * np.sin(a)
        self.position[1] -= direction * self.maxV * np.cos(a)

        # self.paths.append(self.position.copy())
        
        
        

    def brake(self):
        if np.any(np.abs(self.velocity) > 0.01) :
            self.velocity *= 0.01

    def damp(self):
        if ( self.counter == 0 and 
            np.any(np.abs(self.velocity) > 0.01) ):
            self.velocity *= .8

        self.counter += 1
        if self.counter == 5:
            self.counter = 0
        
        

    def apply_force(self, force):
        self.acc += force

    def seek(self, target, damping=1):
        desired = target - self.position
        desired = rmath.set_mag(desired, self.maxV)

        steer = desired - self.velocity
        steer = rmath.limit(steer, self.maxF) * damping
        return steer
    
    def steer_at(self, desired):
        desired = rmath.set_mag(desired, self.maxV)

        steer = desired - self.velocity
        steer = rmath.limit(steer, self.maxF)
        return steer


    def boundary2(self, w, h, d=20, damping=1):
        x, y = self.position
        # target = np.array([w/2, h/2])  

        if x < d:
            desired = np.array([self.maxV, self.velocity[1]])
        elif x > w-d:
            desired = np.array([-self.maxV, self.velocity[1]])
        elif y < d:
            desired = np.array([self.velocity[0], self.maxV])
        elif y > h-d:
            desired = np.array([self.velocity[1], -self.maxV])
        else:
            return np.zeros(2)

        desired = rmath.set_mag(desired, self.maxV)
        steer = desired - self.velocity
        steer = rmath.limit(steer, self.maxF)
        steer *= damping

        return steer
    
    def read_at(self, index):
        force = self.dna.phenotype_mapper(index)
        force = rmath.set_mag(force, self.maxV)

        force = force - self.velocity
        force = rmath.limit(force, self.maxF) * 0.5

        return force

    def calculate_fitness(self, target):
        dist = np.linalg.norm(self.position - target)
        fitness = rmath.linear_map(dist, 0, 1000, 50, 0)
        if not self.collapsed:
            fitness *= 2
        else:
            fitness *= 0.5
        
        self.dna.fitness = fitness 
        

    def check_obstracle(self, obstracle : classes.obstracle.SolidBody):
        x, y = self.position
        x0, y0 = obstracle.position
        x1, y1 = obstracle.w+x0, obstracle.h+y0

        if x > x0 and x < x1 and y > y0 and y < y1:
            self.collapsed = True


    def summary(self):
        print('---------------------')
        print(f'{self.collapsed=}')
        print(f'{self.position=}')
        print(f'{self.velocity=}')
        print(f'{self.acc=}')
        print(f'{self.angle=}')
        print('------ Coordinate -------')
        print(self.image.get_bounding_rect())
        print(self.image.get_rect())

        # r = 50
        # n = 10
        # for i, angle in enumerate(np.linspace(-45, 45, n)):
        #     x2 = r * np.sin(angle) + self.position[0]
        #     y2 = r * np.cos(angle) + self.position[1]
        #     print(angle, '->', *self.position, x2, y2)

        
    def draw_ray(self, pen, objs):
        r = 100
        n = 25
        colided = False

        points = rmath.circle_approximation(self.position, self.angle, r, -45, 45, 5)
        

        for obj in objs:
            colided = rmath.polygon_colision(obj.boundary(), points)
            if colided:
                break
        
        self.collapsed = colided

        pen.no_fill()
        if colided : pen.stroke(color.RED)
        else : pen.stroke(color.GREEN_YELLOW)
        pen.polygon(points)

        
        

    def show(self, pen):
        if len(self.paths) > 50:
            del self.paths[0:2]
        if self.collapsed:
            i = 0
            while self.paths and i < 5:
                self.paths.pop(0)
                i += 1
        

        pen.stroke((255, 0, 70, 100))
        # for i in range(0, len(self.paths)-1):
        #     x1, y1 = self.paths[i]
        #     x2, y2 = self.paths[i+1]
        #     # pen.line(x1, y1, x2, y2)

        temp_image = pygame.transform.rotate(self.image, self.angle)
        rect = temp_image.get_rect(center=self.position)

        pen.no_fill()
        pen.rect(*rect)

        pen.screen.render(self.image, self.angle, self.position[0], self.position[1])



class RocketDNA(dnalib.DNA):
    force_mapper = {
        b'l' : rmath.c(-1., 0.),
        b'p' : rmath.c(-1., -1.),
        b'u' : rmath.c(0., -1.),
        b'q' : rmath.c(1., -1.),
        b'r' : rmath.c(1., 0.),
        b't' : rmath.c(1., 1.),
        b's' : rmath.c(-1., 1.),
        b'b' : rmath.c(0., 1.)
    }

    def __init__(self):
        super().__init__()
        self.neucleotide = 'slpuqrtb'
    
    @staticmethod
    def cross(dna1, dna2, mutation_rate):
        middle = dna1.length // 2
        new_seq = np.concatenate((
            dna1.seq[:middle], dna2.seq[middle:]
        ))
        if mutation_rate == 0: return new_seq

        total_points = round((mutation_rate * dna1.length)/100)
        indices = np.random.choice(np.arange(0, dna1.length), total_points, replace=False)
        nts = np.random.choice(dna1.neucleotide, total_points)
        new_seq[indices] = nts
        return new_seq

    
    def phenotype_mapper(self, ind):
        key = self.seq[ind]
        return RocketDNA.force_mapper.get(key)
        


def reproduce(population, initial_position, rate):
    sorted_population = sorted(population,
        key = lambda rocket : rocket.dna.fitness
    )

    x0, y0 = initial_position
    total_candidate = len(population) // 2 + 1
    mates = dnalib.random_mates(total_candidate, len(population), True) + len(population) - total_candidate
    texture = population[0].image
    children = []
    for i, j in mates:
        # print()
        # print(i, j)
        # print(sorted_population[i].dna.get(), '|', sorted_population[j].dna.get())
        x0 += np.random.normal(0, 3)
        child = Rocket(texture, x0, y0)
        child.dna.load(RocketDNA.cross(
            sorted_population[i].dna, 
            sorted_population[j].dna, 
            rate
        ))
        child.velocity = np.zeros(2)
        children.append(child)
        # print(child.dna.get())
    
    return children








if __name__ == "__main__":
    dna = RocketDNA()
    np.random.seed(1)
    dna.random(10)
    print(dna.get())
    print(dna.seq[1] == b'u')
    RocketDNA.counter += 1
    print(RocketDNA.counter)

    print(dnalib.random_mates(3, 8, True)+4)
    RocketDNA.cross(4, 5)
