
import numpy as np
import cmath
import math
from math import sin, cos, pi, atan2, log
from typing import Tuple
import pygame

image = pygame.image.load('Assets/image.png')

def smap(value, a, b, c, d):
	return (value - a) / (b - a) * (d - c) + c

class DrawingMethod:
    def __init__(self, method_index: int=0):
        self.functions = [
            (mandel_color, iteration_to_color_bw),
            (mandel_color, iteration_to_color_colorful),
            (mandel_color, iteration_to_color_alternating),
            (mandel_normal, None),
            (mandel_image, None),
        ]
        self.method_index = method_index
        self.func: callable = self.functions[self.method_index][0]
        self.coloring: callable = self.functions[self.method_index][1]
        self.center_pos: np.ndarray = None

    def set_center_pos(self, pos: np.ndarray) -> None:
        self.center_pos = pos

    def cycle_method(self):
        self.method_index = (self.method_index + 1) % len(self.functions)
        self.func: callable = self.functions[self.method_index][0]
        self.coloring: callable = self.functions[self.method_index][1]

    def draw(self, pos: np.ndarray, max_iteration: int=100) -> Tuple[int, int, int]:
        center: np.ndarray = pos
        if self.center_pos is not None:
            center = self.center_pos
        return self.func(pos, center, max_iteration, self.coloring)

def iteration_to_color_colorful(iteration: int, max_iterations: int) -> Tuple[int, int, int]:
    f = 0.1
    red = (0.5 * sin(f * iteration) + 0.5) * 255
    green = (0.5 * sin(f * iteration + 2.094) + 0.5) * 255
    blue = (0.5 * sin(f * iteration + 4.188) + 0.5) * 255
    return (red, green, blue)

def iteration_to_color_bw(iteration: int, max_iterations: int) -> Tuple[int, int, int]:
    if iteration == max_iterations:
        return (0,0,0)
    else:
        return (255,255,255)

def iteration_to_color_alternating(iteration: int, max_iterations: int) -> Tuple[int, int, int]:
    return (255,255,255) if iteration % 2 == 0 else (0,0,0)

def mandel_color(pos: np.ndarray, pos_center: np.ndarray, max_iterations: int=100, coloring: callable=iteration_to_color_bw) -> Tuple[int, int, int]:
    a = pos[0]
    b = pos[1]
    
    ca = pos_center[0]
    cb = pos_center[1]
    
    iteration = 0
    while iteration < max_iterations:
        aa = a*a - b*b
        bb = 2*a*b

        a = aa + ca
        b = bb + cb
        
        # if fabs(aa) + fabs(bb) > 4:# asteroids
        # if fabs(aa + bb) > 4:# droplets
        if a*a + b*b > 4:# circular
        # if sqrt(a*a + b*b) > out:# circular
            break
        
        iteration += 1
    
    return coloring(iteration, max_iterations)

def mandel_normal(pos: np.ndarray, pos_center: np.ndarray, max_iterations=100, coloring: callable=None) -> Tuple[int, int, int]:
    radius = 100
    h2 = 1.5
    angle = 45+180
    v = cos((angle * 2 * pi)/360) + sin((angle * 2 * pi)/360) * 1j
    
    c: complex = pos_center[0] + pos_center[1] * 1j
    z: complex = pos[0] + pos[1] * 1j
    dc = 1 + 0j
    der = 1 + 0j
    iteration = 0
    
    reason = 0#not enough
    
    while iteration < max_iterations:

        new_z = z * z + c
        new_der = (der * 2.0) * z + dc
        
        z = new_z
        der = new_der
        
        if abs(z) > radius*radius:
            reason = 1
            break
        
        iteration += 1
    
    if reason == 0:
        bright = 0
    else:
        u = z / der
        u = u * (1.0 / abs(u))
                  
        real_part = u.real * v.real
        imag_part = u.imag * v.imag

        t = real_part + imag_part + h2
        t = t / (1 + h2)
        if t < 0:
            t = 0
        bright = t * 255
    return (bright, bright, bright)

def mandel_image(pos: np.ndarray, pos_center: np.ndarray, max_iterations=100, coloring: callable=None) -> Tuple[int, int, int]:
    move = 0
    out = 4
    a = pos[0]
    b = pos[1]
    
    ca = pos_center[0]
    cb = pos_center[1]
    
    iteration = 0
    while iteration < max_iterations:
        #
        # za = a
        # zb = b
        #
    
        aa = a*a - b*b
        bb = 2*a*b

        a = aa + ca
        b = bb + cb
        
        # if fabs(aa) + fabs(bb) > 4:# asteroids
        # if fabs(aa + bb) > 4:# droplets
        # if a*a + b*b > 4:# circular
        if math.sqrt(a*a + b*b) > out:# circular
            break
        
        iteration += 1
        
    
    # a*=50
    # b*=50
    pos = (image.get_width()//2, image.get_height()//2)
    
    # col = ((pos[0] + int(za))% image.get_width(), (pos[1] + int(zb)) % image.get_height())
    
    x = (atan2(a, b) * (1/pi) + 1)/2
    x *= image.get_width()
    x = int((x + move) % image.get_width())

    
    mag = math.sqrt(a*a + b*b)
    if not out < mag < out*out:
        y = 1
    else:
        y = log(mag / out) / log(out)
    y = smap(y, 0, 1, 0, image.get_height() - 1)
    
    y = int(y)
    
    """ no log:
    mag = sqrt(a*a + b*b)
    if not out <= mag <= out*out:
        y = 0
    else:
        y = (mag - out)/(out*out - out)
    y *= image.get_height()
    y = int(y)
    if y > image.get_height():
        return image.get_height()
    """
    
    # x /= image.get_width()
    # x *= 255
    # x = int((x + move) % 255)
    # print(x)
    # return (x, x, x)
    return image.get_at((x,y))
