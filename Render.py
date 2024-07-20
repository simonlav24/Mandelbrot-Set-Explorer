
import multiprocessing.process
import os
from shutil import rmtree
import numpy as np
import multiprocessing
from Calculations import *
from typing import Tuple, List
import pygame

def render_mandelbrot_process(tl, br, method: DrawingMethod, size: Tuple[int, int], max_iterations: int=100):
    subs = 9
    world_length = br - tl
    sub_size = (int(size[0] * 1.0 / subs), int(size[1] * 1.0 / subs))

    if os.path.isdir('Temp'):
        rmtree('Temp')
    os.mkdir('Temp')
        
    processes: List[multiprocessing.Process] = []

    for y in range(subs):
        for x in range(subs):
            index = x + subs * y
            current_tl = (
                tl[0] + (x / subs) * world_length[0],
                tl[1] + (y / subs) * world_length[1]
            )
            current_br = (
                tl[0] + ((x + 1) / subs) * world_length[0],
                tl[1] + ((y + 1) / subs) * world_length[1]
            )
            p = multiprocessing.Process(target=render_mandelbrot, args=(index, current_tl, current_br, method, sub_size, max_iterations))
            processes.append(p)

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    surf = pygame.Surface(size)
    for file in os.listdir('Temp'):
        index = int(file.replace('.png', ''))
        x = (index % subs) * sub_size[0]
        y = (index // subs) * sub_size[1]

        image = pygame.image.load(fr'Temp/{file}')
        surf.blit(image, (x, y))

    return surf
    

def render_mandelbrot(index, tl, br, method: DrawingMethod, size: Tuple[int, int], max_iterations: int):
    surf = pygame.Surface(size)

    x_start = tl[0]
    x_step = (br[0] - tl[0]) / size[0]
    pos_x = x_start

    y_start = tl[1]
    y_step = (br[1] - tl[1]) / size[1]
    pos_y = y_start

    for s_y in range(size[1]):
        for s_x in range(size[0]):

            color = method.draw(np.array((pos_x, pos_y)), max_iterations)
            surf.set_at((s_x, s_y), color)

            pos_x += x_step
        pos_x = x_start
        pos_y += y_step

    pygame.image.save(surf, rf'Temp/{index}.png')



