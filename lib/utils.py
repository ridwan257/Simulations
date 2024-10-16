import pygame
import numpy as np


def to_string(vector, digit=3, sep=' '):
    text = np.array2string(vector, precision=digit, 
                           suppress_small=True, separator=sep)
    # return text[1:-1].strip()
    return text

def print_array2d(arr, end=' '):
    for row in arr: 
        for v in row: 
            print(v, end=end)
        print()

def image(filepath, size=None):
    img = pygame.image.load(filepath).convert_alpha()   
    if size is not None:
        img = pygame.transform.smoothscale(img, size)
    return img


def mouse() : 
    return np.array(pygame.mouse.get_pos(), dtype=np.float64)

def lerp_color(t, color1, color2):
    """
    Linearly interpolate between two colors.
    
    Parameters:
    color1 (tuple): The first color (r1, g1, b1).
    color2 (tuple): The second color (r2, g2, b2).
    t (float): The interpolation parameter, where 0 <= t <= 1.
    
    Returns:
    tuple: The interpolated color (r, g, b).
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)

    return (r, g, b)

def topleft(surface, center):
    rect = surface.get_rect(center=center)
    return rect.topleft

def get_elapsed_time(start_time):
    if start_time == 0:
        return 0
    else:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        return elapsed_time

def toggle(value : bool)->bool:
    if value:
        return False
    return True

def RGBtoGrayscale(value):
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = (value >> 0) & 0xFF

    return 0.299 * r + 0.587 * g + 0.114 * b

RGBtoGrayscale = np.vectorize(RGBtoGrayscale)

def toRGB(value):
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = (value >> 0) & 0xFF

    return (r, g, b)

def getGrayScaleValue(surface):
    """
    Convert a surface into array containing grayscale value
    """
    arr = pygame.surfarray.array2d(surface)
    return RGBtoGrayscale(arr)

def grayScaleToSurface(surface : pygame.Surface, array : np.ndarray):
    """
    Copy a grascale color value array to a surface
    """
    rgb_array = np.stack((array, array, array), axis=-1)
    pygame.surfarray.blit_array(surface, rgb_array)

