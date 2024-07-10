import numpy as np


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

def linear_map(value, amin, amax, bmin, bmax):
    k = (bmax - bmin) / (amax - amin)
    x = bmax + value * k - k * amax
    return x

def inf_map(value, bmin, bmax):
    k = value / (value + 1)
    x = bmin + k * (bmax - bmin)
    return x