from typing import Tuple
import numpy as np
import json
import pygame

from settings import *
from algorithm import converge_network, converge_network_modern

class GridSquare:
    def __init__(self, pos, dimensions) -> None:
        self.display_surface = pygame.display.get_surface()
        
        self.surf = pygame.Surface(dimensions, pygame.SRCALPHA)
        self.rect = self.surf.get_frect(topleft=pos)

        self.toggled = True

    def draw(self) -> None:
        self.display_surface.blit(self.surf, self.rect)
        pygame.draw.rect(self.surf, "black", self.surf.get_frect(topleft=(0,0)), 1)

    def toggle(self) -> None:
        self.surf.fill("black" if self.toggled else "white")
        self.toggled = not self.toggled


class InputScreen:
    def __init__(self, screen_dimensions: Tuple[int, int], top_left: Tuple[int, int], grid_size: Tuple[int, int], weight_matrix = np.ndarray) -> None:
        self.screen_width, self.screen_height = screen_dimensions
        self.top_left = pygame.Vector2(top_left)
        self.grid_width, self.grid_height = grid_size

        grid_square_width, grid_square_height = self.screen_width / self.grid_width, self.screen_height / self.grid_height
        self.grid_squares = [[GridSquare(self.top_left + pygame.Vector2(grid_square_width * i, grid_square_height * j), (grid_square_width, grid_square_height)) for i in range(self.grid_width)] for j in range(self.grid_height)]

        self.weight_matrix = weight_matrix


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
        mouse_just_pressed = pygame.mouse.get_just_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        key_just_pressed = pygame.key.get_just_pressed()
        self._handle_mouse_left_click_just_pressed(mouse_just_pressed)
        self._handle_key_just_pressed(key_just_pressed)
        self._handle_mouse_left_click_pressed(mouse_pressed)

    def _handle_mouse_left_click_just_pressed(self, mouse_just_pressed: tuple[bool, bool, bool]) -> None:
        if mouse_just_pressed[0]: # If left clicked
            mouse_pos = pygame.mouse.get_pos()
            for row in self.grid_squares:
                for grid_square in row:
                    if grid_square.rect.collidepoint(mouse_pos):
                        grid_square.toggle()

    def _handle_mouse_left_click_pressed(self, mouse_pressed: tuple[bool, bool, bool]) -> None:
        if mouse_pressed[0]: # If left clicked
            mouse_pos = pygame.mouse.get_pos()
            for row in self.grid_squares:
                for grid_square in row:
                    if grid_square.rect.collidepoint(mouse_pos):
                        grid_square.surf.fill("black")
                        grid_square.toggled = False

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