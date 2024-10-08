from typing import List, Union
import numpy as np



class Vec2d(np.ndarray):
    def __new__(cls, x=0, y=0):
        obj = np.asarray([x, y], dtype=np.float64).view(cls)
        obj._x = x
        obj._y = y
        return obj
    
    def __init__(self, x=0, y=0): ...
    
    def __array_finalize__(self, obj):
        # This method is called to finalize the creation of the array
        if obj is None: return
        # Copy over attributes from the original array if necessary
        self._x = getattr(obj, '_x', 0)
        self._y = getattr(obj, '_y', 0)

    @property
    def x(self): return self._x
    @x.setter 
    def x(self, value): 
        self._x = value
        self[0] = value

    @property
    def y(self): return self._y
    @y.setter 
    def y(self, value): 
        self._y = value
        self[1] = value

    def heading(self):
        return np.arctan2(self._y, self._x)
    
    



def c(*args, **keys):
    return np.array(args, **keys)

def distance(point1, point2):
    p1 = np.array(point1)
    p2 = np.array(point2)
    distance = np.linalg.norm(p2 - p1)
    return distance

def rotation_angle(position, target)->np.float64:
    dx = position[0] - target[0]
    dy = position[1] - target[1]

    angle_radians = np.arctan2(dy, dx)
    angle_degrees = 90 - np.degrees(angle_radians)

    return angle_degrees

def R2d(angle):
    cos_value = np.cos(np.radians(angle))
    sin_value = np.sin(np.radians(angle))
    return np.array([
            [cos_value, -sin_value],
            [sin_value, cos_value]
        ])

def heading(vector:np.ndarray)->np.float64:
    if np.all(vector == 0): 
        return 0
    angle_rad = np.arctan2(vector[1], -1*vector[0])
    angle_deg = 90 + np.degrees(angle_rad)
    return angle_deg


def limit(vector, maxlength)->np.ndarray:
    if type(vector) == list:
        vector = np.array(vector)
    
    l = np.linalg.norm(vector)
    
    if l > maxlength:
        vector = ( vector / l ) * maxlength
    
    return vector

def set_mag(vector, value)->np.ndarray:
    if type(vector) == list:
        vector = np.array(vector)
        
    l = np.linalg.norm(vector)
    if l > 0:
        vector = ( vector / l ) * value
    return vector

def linear_map(value : float, amin, amax, bmin, bmax):
    k = (bmax - bmin) / (amax - amin)
    x = bmax + value * k - k * amax
    return x

def inf_map(value : float, bmin : float, bmax : float):
    k = value / (value + 1)
    x = bmin + k * (bmax - bmin)
    return x


def polygon_colision(polygon1 : Union[List, np.ndarray], polygon2 : Union[List[float], np.ndarray]):
    """
    detect collision between to convex polygon.

    parametes:
    polygon1 : [(a1, b1), (a2, b2), ..., (an, bn)] or numpy array
        all points of polygon in counter-clockwise or clockwisw manner
    polygon2 : [(a1, b1), (a2, b2), ..., (an, bn)] or numpy array
        all points of polygon in counter-clockwise or clockwisw manner
    """
    # calculating the vertices from the polygon
    if type(polygon1) != np.ndarray:
        polygon1 = np.array(polygon1)
    if type(polygon1) != np.ndarray:
        polygon2 = np.array(polygon2)

    # calculating all vertices
    vertices1 = np.roll(polygon1, -1, 0) - polygon1
    vertices2 = np.roll(polygon2, -1, 0) - polygon2


    # calculating all orthogonals of vertices
    orthogonal_v1 = np.empty_like(vertices1)
    orthogonal_v1[:, 0] = vertices1[:, 1]
    orthogonal_v1[:, 1] = -1 * vertices1[:, 0]

    orthogonal_v2 = np.empty_like(vertices2)
    orthogonal_v2[:, 0] = vertices2[:, 1]
    orthogonal_v2[:, 1] = -1 * vertices2[:, 0]

    # concatenating all orthogonal in a single array
    orthogonals = np.concatenate([orthogonal_v1, orthogonal_v2])
    orthogonals = np.unique(orthogonals, axis=0)


    # making all othogonals unit vector
    # this may not be important
    # norm_values = np.linalg.norm(orthogonals, axis=1)
    # norm_values = norm_values[:, np.newaxis]
    # orthogonals /= norm_values
    
    # print('**********************************')
    for vec in orthogonals:
        # print('---------------------------')
        # print(vec)
        # calculating each pojection point on norm vactors
        polygon1_projection = np.dot(polygon1, vec)
        polygon2_projection = np.dot(polygon2, vec)

        min_p1 = np.min(polygon1_projection)
        max_p1 = np.max(polygon1_projection)

        min_p2 = np.min(polygon2_projection)
        max_p2 = np.max(polygon2_projection)

        # print(min_p1, max_p1, '|', min_p2, max_p2)

        if (min_p1 - max_p2 > 0) or (max_p1 - min_p2 < 0):
            return False
    
    return True

def circle_approximation(origin, direction, radii, angR, angL, n=3):
    angL, angR = np.deg2rad((angL, angR)) - np.deg2rad(direction)
    x1, y1 = origin
    
    points = np.empty((n + 1, 2))
    points[0] = (x1, y1)

    for i, angle in enumerate(np.linspace(angL, angR, n), 1):
        x = radii * np.sin(angle) + x1
        y =  y1 - radii * np.cos(angle)
        points[i] = (x, y)

    return points