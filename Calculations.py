
import numpy as np
from cmath import sqrt
from math import sin, cos, pi

def mandel_color(pos: np.ndarray, color=1, max_iterations: int=100):
    a = pos[0]
    b = pos[1]
    
    ca = a
    cb = b
    
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
    
    if color == 0: # colorfull, olc
        f = 0.1
        red = (0.5 * sin(f * iteration) + 0.5) * 255
        green = (0.5 * sin(f * iteration + 2.094) + 0.5) * 255
        blue = (0.5 * sin(f * iteration + 4.188) + 0.5) * 255
        return (red, green, blue)    
    
    elif color == 1: # black&white
        if iteration == max_iterations:
            return (0,0,0)
        else:
            return (255,255,255)
    
    elif color == 2:
        return (255,255,255) if iteration % 2 == 0 else (0,0,0)


def mandel_normal(pos, color, max_iterations=100):
    radius = 100
    h2 = 1.5
    angle = 45+180
    v = cos((angle * 2 * pi)/360) + sin((angle * 2 * pi)/360) * 1j
    
    a = pos[0]
    b = pos[1]
    
    c: complex = a + b * 1j
    z: complex = a + b * 1j
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