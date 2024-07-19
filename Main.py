from math import fabs, sqrt, cos, sin, pi, floor, ceil, e, atan2, log
from random import uniform, randint, choice
from datetime import datetime
import numpy as np
import pygame

from Calculations import *

WIN_WIDTH = 1280
WIN_HEIGHT = 720
WIN_RATIO = WIN_HEIGHT / WIN_WIDTH

render_size = (1920, 1080)

class Grid:
    def __init__(self):
        self.cam: np.ndarray = np.array([0,0])
        self.scale = 200.0
        self.center: np.ndarray = np.array([WIN_WIDTH / 2, WIN_HEIGHT / 2])
        
        self.point = None
        self.cam_prev = None
        self.mouse_pressed: bool = False
        self.is_changed: bool = False
        
    def transform(self, pos: np.ndarray) -> np.ndarray:
        return pos * self.scale + self.center - self.cam
    
    def invert(self, pos: np.ndarray) -> np.ndarray:
        return (pos - self.center + self.cam) / self.scale

    def zoom(self, sign):
        origin = self.transform(np.zeros(2))
        mouse = np.array(pygame.mouse.get_pos())
        adjust = mouse - origin
        self.cam = self.cam + sign * adjust * 0.2
        self.scale += sign * 0.2 * self.scale
        self.is_changed = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.point = np.array(pygame.mouse.get_pos()) / self.scale
            self.mouse_pressed = True
            self.cam_prev = self.cam.copy()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse_pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.zoom(1.0)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.zoom(-1.0)
    
    def step(self):
        self.is_changed = False
        if self.mouse_pressed:
            current = np.array(pygame.mouse.get_pos()) / self.scale
            self.cam = self.cam_prev + (self.point - current) * self.scale
            self.is_changed = True

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Simon\'s graph')
    
    font =  pygame.font.SysFont('Tahoma', 12, True)
    
    grid = Grid()

    initial_subdivisions = 20
    subdivisions_x = initial_subdivisions
    subdivisions_y = int(subdivisions_x * WIN_RATIO)
    mandel_surf = pygame.Surface((subdivisions_x, subdivisions_y))
    
    STATE_EXPLORE = 0
    STATE_RENDER = 1
    state = STATE_EXPLORE

    render_finished: bool = False

    done = False
    while not done:
        for event in pygame.event.get():
            grid.handle_event(event)
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    render_finished = False
                    if state == STATE_EXPLORE:
                        state = STATE_RENDER
                    else:
                        state = STATE_EXPLORE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            done = True
        
        # step
        grid.step()

        if grid.is_changed:
            state = STATE_EXPLORE

        # draw
        if state == STATE_EXPLORE:
            win.fill((0,0,0))
            if grid.is_changed:
                subdivisions_x = initial_subdivisions
                subdivisions_y = int(initial_subdivisions * WIN_RATIO)

            mandel_surf = pygame.Surface((subdivisions_x, subdivisions_y))
            for y in range(0, subdivisions_y):
                y_win = (WIN_HEIGHT / subdivisions_y) * y
                for x in range(0, subdivisions_x):
                    x_win = (WIN_WIDTH / subdivisions_x) * x
                    
                    pos_in_win = np.array([x_win + (WIN_WIDTH / subdivisions_x) / 2, y_win + (WIN_HEIGHT / subdivisions_y) / 2])
                    # win.set_at((int(pos_in_win[0]), int(pos_in_win[1])), (255,0,0))
                    pos_in_world = grid.invert(pos_in_win)
                    color = mandel_normal(pos_in_world, 2)
                    mandel_surf.set_at((x, y), color)
            subdivisions_x += 1
            subdivisions_y = int(subdivisions_x * WIN_RATIO)
            
            win.blit(pygame.transform.scale(mandel_surf, (WIN_WIDTH, WIN_HEIGHT)), (0,0))
        
        if state == STATE_RENDER:
            if not render_finished:
                for y in range(0, WIN_HEIGHT):
                    for x in range(0, WIN_WIDTH):
                        pos_in_win = np.array((x, y))
                        pos_in_world = grid.invert(pos_in_win)
                        color = mandel_normal(pos_in_world, 2)
                        win.set_at((x, y), color)
                    
                    pygame.draw.line(win, (255,255,0), (0, y + 1), (WIN_WIDTH, y + 1))
                    pygame.display.update()

            render_finished = True

        # win.blit(mandel_surf, (0,0))
        pygame.display.update()


        

if __name__ == '__main__':
    main()