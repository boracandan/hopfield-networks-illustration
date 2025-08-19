import pygame
import pygame_gui

from settings import *
from screen import InputScreen

class HopfieldIllustrationApp:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("HopfieldNetworkIllustration")
        self.clock = pygame.Clock()
        self.running = True

        self.input_screen = InputScreen(screen_dimensions=(700, 700), top_left=(0, 0), grid_size=(28, 28))

        # Start game loop
        self.run()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                

            # Update
            self.input_screen.update()
            
            # Draw
            self.display_surface.fill("white")
            self.input_screen.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    HopfieldIllustrationApp()