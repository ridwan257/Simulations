import pygame
import numpy as np
from lib import rmath
from lib import color as c
from lib import utils as utl

class VeichleA:
    def __init__(self, x, y, w=16, h=21, col=(128, 128, 128)):
        self.w = w
        self.h = h
        self.col = col
        # self.surface = pygame.surface.Surface((w, h), pygame.SRCALPHA)
        self.__vertices = [(self.w/2, 0), 
                    (self.w, self.h), 
                    (self.w/2, 2/3 * self.h), 
                    (0, self.h)]
        # pygame.draw.polygon(self.surface, self.col, self.__vertices,1)

        self.position = np.array([x, y], dtype=np.float64)
        self.velocity = np.array([0., 0.])
        self.acc = np.zeros(2)
        self.maxV = 5
        self.maxF = 0.6
        
        self.dead = False
        self.__health = 100
        self.__use_leap_color = True
        self.__boundary = True
        # here the info stored that how much 
        # self.dna = [0.5, -0.08, 90, 40]
        self.dna = np.array([
            0.5, # attraction factor for good food
            -0.08, # repaltion factor for bad food
            90, # perception radius for good food
            40, # perception radius for bad food
            5 # modulator of boundary activity

        ]) 

    @property
    def health(self):
        return self.__health
    @health.setter
    def health(self, nutrition):
        self.__health += nutrition
        if self.__health > 100:
            self.__health = 100
        elif self.__health < 0:
            self.__health = 0
            # self.dead = True
    

    def update(self):
        self.velocity += self.acc
        self.velocity = rmath.limit(self.velocity, self.maxV)
        self.position += self.velocity
        self.acc *= 0
        
    def apply_force(self, force):
        # print(force)
        self.acc += force
  
    def seek(self, target, damping = 1):
        desired = target - self.position
        desired = rmath.set_mag(desired, self.maxV)

        steer = desired - self.velocity
        steer = rmath.limit(steer, self.maxF) # this is most important
        steer *= damping
        return steer

    def boundary2(self, w, h, d=20, damping=1):
        x, y = self.position
        target = np.array([w/2, h/2])  

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

            
    def eat(self, bucket, w=400, h=400):
        # print(f'{len(bucket)=}')
        temp_dist = np.inf
        nearest_food = -1
        eated_food = []
        food_should_be_recalled = True
        report = {
            'food' : 0,
            'poison' : 0
        }

        for i, food in enumerate(bucket):
            if food.eaten:
                if food_should_be_recalled and \
                    np.random.rand() < 0.002:
                    food.eaten = False
                    food_should_be_recalled = False
                    # x = np.random.randint(0, w + 1)
                    # y = np.random.randint(0, h + 1)
                    # food.position = np.array([x, y])
                
                continue
            # food is not eaten. so calculate the distance
            dist = np.linalg.norm(self.position - food.position)

            if dist < self.w//2:
                self.health = food.nutrition
                eated_food.append(i)
                food.eaten = True
            # among ramaing foods we should find the nearest food
            elif dist < temp_dist:
                temp_dist = dist
                nearest_food = i
            
            # counting good and bad food
            if food.type == 'g':
                report['food'] += 1
            else:
                report['poison'] += 1

        # if eated_food:
        #     print(f'{eated_food=} | {nearest_food=} | {len(bucket)}')

        # now calculating force which should vehicle go
        # default is 0
        steer = np.zeros(2)
        # if any food available then we should check if 
        # it is inside the vehicle percetion
        if nearest_food > -1:
            damping = 0
            if bucket[nearest_food].type=='g' and temp_dist < self.dna[2]: 
                damping = self.dna[0]
            elif temp_dist < self.dna[3]: 
                damping = self.dna[1]

            steer = self.seek(bucket[nearest_food].position, damping)
            # here the damping factor may be greater than one
            # if that then force can be bigger than its maximum
            # we have rescale such phenomena
            if damping > 1:
                steer = rmath.limit(steer, self.maxF)
            
        return (steer, report)

    def show_leap_color(self) : self.__use_leap_color = True
    def hide_leap_color(self) : self.__use_leap_color = False
    
    def show_boundary(self) : self.__boundary = True
    def hide_boundary(self) : self.__boundary = False

    def fill(self, color):
        self.col = color
        # pygame.draw.polygon(self.surface, self.col, self.__vertices)

    def show(self, pen):
        if self.dead:
            return    
        if self.__use_leap_color:
            self.fill(utl.lerp_color(self.health/100, c.RED, c.BLUE))
        if self.__boundary and pen:
            pen.no_fill()
            pen.stroke(c.BLUE)
            pen.Acircle(self.position, self.dna[2])
            pen.stroke(c.RED)
            pen.Acircle(self.position, self.dna[3])

        angle = rmath.heading(self.velocity)
        pen.no_stroke()
        pen.fill(self.col)
        pen.Apolygon(*self.position, self.w, self.h, self.__vertices, angle)
    




class Food:
    def __init__(self, pos, type):
        self.position = pos
        self.type = type
        self.r = 3
        self.eaten = False
        
        if type == 'g':
            self.color = c.GREEN
            self.nutrition = 3
        else:
            self.color = c.RED
            self.nutrition = -6

    def show(self, pen):
        if self.eaten:
            return
        # we are gonna draw the food
        pen.no_stroke()
        pen.fill(self.color)
        pen.Acircle(self.position, self.r)

    


    @classmethod
    def show_all(cls, pen, bucket):
        for food in bucket:
            if food:
                food.show(pen)



def reproduce_vehicles(veichles, index, w, h, rate):
    print('-----------------')
    print(f'{index=}') 
    weights = np.arange(1, len(index)+1, dtype=np.float64)**2
    weights /= np.sum(weights)
    i = 0
    children = []
    mutaion_report = np.zeros(len(veichles))
    
    while i < len(veichles):
        partners = np.random.choice(index, 2, replace=False, p=weights)
        bf = veichles[partners[0]]
        gf = veichles[partners[1]]
        # making baby
        # if np.random.randint(0, 2) == 0:
        #     x, y = bf.position
        #     v = gf.velocity
        # else:
        #     x, y = gf.position
        #     v = bf.velocity
        x = np.random.randint(0, w + 1)
        y = np.random.randint(0, h + 1)
        child = VeichleA(x, y, bf.w, bf.h)
        child.velocity = np.random.uniform(-2, 2, 2)
        child.dna = (bf.dna + gf.dna) / 2
        for j, p in enumerate(np.random.rand(4)):
            sd = 0.3 if j < 2 else 12
            if p < rate / 100:
                child.dna[j] += np.random.normal(0, sd)
                mutaion_report[i] = 1
        
        children.append(child)
        i += 1


    
    return (children, np.sum(mutaion_report))






