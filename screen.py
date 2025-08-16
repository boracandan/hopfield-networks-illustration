from typing import Tuple
import pygame

from settings import *

class GridSquare:
    def __init__(self, pos, dimensions) -> None:
        self.display_surface = pygame.display.get_surface()
        
        self.surf = pygame.Surface(dimensions, pygame.SRCALPHA)
        self.rect = self.surf.get_frect(topleft=pos)

    def draw(self) -> None:
        self.display_surface.blit(self.surf, self.rect)
        pygame.draw.rect(self.surf, "black", self.surf.get_frect(topleft=(0,0)), 1)
        

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
    

