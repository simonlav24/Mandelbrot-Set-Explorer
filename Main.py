

import os
from datetime import datetime
import numpy as np
import pygame

from Calculations import *

WIN_WIDTH = 1280
WIN_HEIGHT = 720
WIN_RATIO = WIN_HEIGHT / WIN_WIDTH

OUTPUT_PATH = 'Output'

render_size = (1920*2, 1080*2)

def save_image(surf: pygame.Surface):
    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    path = os.path.join(OUTPUT_PATH, f'{dt_string}.png')
    print(f'Image saved: {path}')
    pygame.image.save(surf, path)

class Grid:
    def __init__(self):
        self.cam: np.ndarray = np.array([-200,0])
        self.scale = 300.0
        self.center: np.ndarray = np.array([WIN_WIDTH / 2, WIN_HEIGHT / 2])
        
        self.drag_point = None
        self.cam_prev = None
        self.mouse_pressed: bool = False
        self.is_changed: bool = False

        self.selected_point: np.ndarray = None
        
    def transform(self, pos: np.ndarray) -> np.ndarray:
        return pos * self.scale + self.center - self.cam
    
    def invert(self, pos: np.ndarray) -> np.ndarray:
        return (pos - self.center + self.cam) / self.scale

    def zoom(self, sign: float):
        origin = self.transform(np.zeros(2))
        mouse = np.array(pygame.mouse.get_pos())
        adjust = mouse - origin
        self.cam = self.cam + sign * adjust * 0.2
        self.scale += sign * 0.2 * self.scale
        self.is_changed = True

    def home(self):
        self.cam: np.ndarray = np.array([-200,0])
        self.scale = 300.0
        self.center: np.ndarray = np.array([WIN_WIDTH / 2, WIN_HEIGHT / 2])
        self.drag_point = None
        self.cam_prev = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drag_point = np.array(pygame.mouse.get_pos()) / self.scale
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
            self.cam = self.cam_prev + (self.drag_point - current) * self.scale
            self.is_changed = True

    def draw(self, win):
        if self.selected_point is not None:
            pygame.draw.circle(win, (255,0,0), self.transform(self.selected_point), 5)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Simon\'s graph')
    
    font =  pygame.font.SysFont('Tahoma', 12, True)
    
    grid = Grid()
    drawing = DrawingMethod(1)

    initial_subdivisions = 20
    subdivisions_x = initial_subdivisions
    subdivisions_y = int(subdivisions_x * WIN_RATIO)
    mandel_surf = pygame.Surface((subdivisions_x, subdivisions_y))
    
    STATE_EXPLORE = 0
    STATE_RENDER = 1
    STATE_RENDER_FULL = 2
    state = STATE_EXPLORE

    render_finished: bool = False

    done = False
    while not done:
        for event in pygame.event.get():
            grid.handle_event(event)
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    win_point = grid.invert(np.array(pygame.mouse.get_pos()))
                    grid.selected_point = win_point
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    # render win
                    render_finished = False
                    if state == STATE_EXPLORE:
                        state = STATE_RENDER
                    else:
                        state = STATE_EXPLORE

                if event.key == pygame.K_j:
                    # switch julia set
                    if grid.selected_point is None:
                        continue
                    if drawing.center_pos is None:
                        drawing.set_center_pos(grid.selected_point)
                    else:
                        drawing.set_center_pos(None)

                if event.key == pygame.K_m:
                    # cycle methods
                    drawing.cycle_method()
                
                if event.key == pygame.K_p:
                    # render full
                    render_finished = False
                    state = STATE_RENDER_FULL
                
                if event.key == pygame.K_h:
                    # home button
                    grid.home()

                
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
                    color = drawing.draw(pos_in_world)
                    mandel_surf.set_at((x, y), color)
            subdivisions_x += 1
            subdivisions_y = int(subdivisions_x * WIN_RATIO)
            
            win.blit(pygame.transform.scale(mandel_surf, (WIN_WIDTH, WIN_HEIGHT)), (0,0))
            grid.draw(win)
        
        elif state == STATE_RENDER:
            if not render_finished:
                for y in range(0, WIN_HEIGHT):
                    for x in range(0, WIN_WIDTH):
                        pos_in_win = np.array((x, y))
                        pos_in_world = grid.invert(pos_in_win)
                        color = drawing.draw(pos_in_world)
                        win.set_at((x, y), color)
                    
                    pygame.draw.line(win, (255,255,0), (0, y + 1), (WIN_WIDTH, y + 1))
                    pygame.display.update()

                render_finished = True
        
        elif state == STATE_RENDER_FULL:
            surf = pygame.Surface(render_size)
            ratio_x = WIN_WIDTH / render_size[0]
            ratio_y = WIN_HEIGHT / render_size[1]
            if not render_finished:
                for y in range(0, render_size[1]):
                    for x in range(0, render_size[0]):

                        pos_in_win = np.array((x * ratio_x, y * ratio_y))
                        pos_in_world = grid.invert(pos_in_win)
                        color = drawing.draw(pos_in_world)
                        surf.set_at((x, y), color)
                    
                    pygame.draw.line(surf, (255,255,0), (0, y + 1), (render_size[0], y + 1))

                    win.blit(pygame.transform.smoothscale(surf, (WIN_WIDTH, WIN_HEIGHT)), (0,0))
                    pygame.display.update()

                save_image(surf)
                render_finished = True
            

        # win.blit(mandel_surf, (0,0))
        pygame.display.update()


        

if __name__ == '__main__':
    main()