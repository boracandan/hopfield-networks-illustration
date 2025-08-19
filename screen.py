from typing import Tuple
import pygame

from settings import *

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
    def __init__(self, screen_dimensions: Tuple[int, int], top_left: Tuple[int, int], grid_size: Tuple[int, int]) -> None:
        self.screen_width, self.screen_height = screen_dimensions
        self.top_left = pygame.Vector2(top_left)
        self.grid_width, self.grid_height = grid_size

        grid_square_width, grid_square_height = self.screen_width / self.grid_width, self.screen_height / self.grid_height
        
        self.grid_squares = [[GridSquare(self.top_left + pygame.Vector2(grid_square_width * i, grid_square_height * j), (grid_square_width, grid_square_height)) for i in range(self.grid_width)] for j in range(self.grid_height)]

    def draw(self) -> None:
        for row in self.grid_squares:
            for square in row:
                square.draw()

    def update(self) -> None:
        mouse_pressed = pygame.mouse.get_just_pressed()
        self._handle_mouse_left_click_just_pressed(mouse_pressed)

    def _handle_mouse_left_click_just_pressed(self, mouse_pressed: tuple[bool, bool, bool]) -> None:
        if mouse_pressed[0]: # If left clicked
            mouse_pos = pygame.mouse.get_pos()
            for row in self.grid_squares:
                for grid_square in row:
                    if grid_square.rect.collidepoint(mouse_pos):
                        grid_square.toggle()
    

