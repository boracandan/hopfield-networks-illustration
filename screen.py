from typing import Tuple
import numpy as np
import json
import pygame
import pygame_gui as pg

from settings import *
from ui import UI
from algorithm import converge_network, converge_network_modern

class GridSquare:
    def __init__(self, pos, dimensions) -> None:
        self.display_surface = pygame.display.get_surface()
        
        self.surf = pygame.Surface(dimensions, pygame.SRCALPHA)
        self.rect = self.surf.get_frect(topleft=pos)

        self.toggled = True

    def draw(self) -> None:
        pygame.draw.rect(surface=self.surf, color="black", rect=self.surf.get_frect(topleft=(0,0)), width=1)
        self.display_surface.blit(self.surf, self.rect)
        

    def toggle(self) -> None:
        self.surf.fill("black" if self.toggled else "white")
        self.toggled = not self.toggled


class InputScreen:
    def __init__(self, screen_dimensions: Tuple[int, int], top_left: Tuple[int, int], grid_size: Tuple[int, int], weight_matrix: np.ndarray, ui: UI) -> None:
        self.screen_width, self.screen_height = screen_dimensions
        self.top_left = pygame.Vector2(top_left)
        self.grid_width, self.grid_height = grid_size

        self.grid_square_width, self.grid_square_height = self.screen_width / self.grid_width, self.screen_height / self.grid_height
        self.grid_squares = [[GridSquare(self.top_left + pygame.Vector2(self.grid_square_width * i, self.grid_square_height * j), (self.grid_square_width, self.grid_square_height)) for i in range(self.grid_width)] for j in range(self.grid_height)]

        self.weight_matrix = weight_matrix

        self.ui = ui

        self.brush_color = "black"
        self._brush_collision_rect = pygame.FRect((0, 0), (self.grid_square_width / 10, self.grid_square_height / 10))


    @property
    def current_state(self) -> list:
        return [1 if grid_square.toggled else -1 for row in self.grid_squares for grid_square in row]    
    
    @current_state.setter
    def current_state(self, state: np.ndarray) -> None:
        i = 0
        for row in self.grid_squares:
            for grid_square in row:
                desired_state = True if state[i] == 1 else False
                if grid_square.toggled != desired_state:
                    grid_square.toggle()
                i += 1

    @property
    def brush_size(self) -> int:
        return self._brush_collision_rect.width / self.grid_square_width
    
    @brush_size.setter
    def brush_size(self, size: int) -> None:
        self._brush_collision_rect.size = (self.grid_square_width * size, self.grid_square_height * size)

    def reset(self) -> None:
        for row in self.grid_squares:
            for grid_square in row:
                if not grid_square.toggled:
                    grid_square.toggle()

    def draw(self) -> None:
        for row in self.grid_squares:
            for square in row:
                square.draw()

    def update(self) -> None:
        mouse_pressed = pygame.mouse.get_pressed()
        key_just_pressed = pygame.key.get_just_pressed()
        self._handle_key_just_pressed(key_just_pressed)
        self._handle_mouse_left_click_pressed(mouse_pressed)

    def handle_event(self, event: pygame.Event):
        if event.type == pg.UI_BUTTON_PRESSED:
            if event.ui_element in self.ui.memory_buttons:
                idx = self.ui.memory_buttons.index(event.ui_element)
                self.current_state = self.weight_matrix[:, idx].reshape(-1)

            elif event.ui_element is self.ui.black_button:
                self.brush_color = "black"

            elif event.ui_element is self.ui.white_button:
                self.brush_color = "white"

        elif event.type == pg.UI_HORIZONTAL_SLIDER_MOVED:
            print(event.ui_element.get_current_value())

    def _handle_mouse_left_click_pressed(self, mouse_pressed: tuple[bool, bool, bool]) -> None:
        if mouse_pressed[0]: # If left clicked
            mouse_pos = pygame.mouse.get_pos()
            self._brush_collision_rect.center = mouse_pos
            for row in self.grid_squares:
                for grid_square in row:
                    if grid_square.rect.colliderect(self._brush_collision_rect):
                        grid_square.surf.fill(self.brush_color)
                        grid_square.toggled = self.brush_color == "white"

    def _handle_key_just_pressed(self, key_just_pressed: pygame.key.ScancodeWrapper) -> None:
        if key_just_pressed[pygame.K_r]: # if "r" key is pressed 
            self.reset()

        if key_just_pressed[pygame.K_t]:
            # self.reset()

            outputs = np.array(self.current_state)
            print(outputs, "aaaa")
            converged_state = converge_network_modern(patterns=self.weight_matrix, state=outputs)
            print(converged_state)
            self.current_state = converged_state