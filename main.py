import pygame
import pygame_gui
import json
import numpy as np

from settings import *
from screen import InputScreen
from algorithm import calculate_weight_matrix
from ui import UI

class HopfieldIllustrationApp:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode(size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("HopfieldNetworkIllustration")
        self.clock = pygame.Clock()
        self.running = True

        # Load the memory file
        with open("memory.json") as json_file:
            letter_memories = json.load(json_file)

        with open("photo_memory.json") as json_file:
            photo_memories = [next(iter(memory.values())) for memory in json.load(json_file)]
        
        # patterns = np.column_stack([next(iter(memory.values())) for memory in letter_memories])
        patterns = np.column_stack(photo_memories)

        print(patterns[:][:], patterns.shape)

        # weight_matrix = calculate_weight_matrix(memories=memories)

        # UI
        self.uiManager = pygame_gui.UIManager(window_resolution=(DISPLAY_WIDTH, DISPLAY_HEIGHT), theme_path="theme.json")
        self.ui = UI(rect=pygame.Rect(698, -2, 205, 705), manager=self.uiManager, memory_num=len(photo_memories))

        # Input Screen
        self.input_screen = InputScreen(screen_dimensions=(700, 700), top_left=(0, 0), grid_size=(64, 64), weight_matrix=patterns, ui=self.ui)

        # Start game loop
        self.run()
        
    def run(self) -> None:
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.uiManager.process_events(event)
                self.ui.process_event(event)
                self.input_screen.handle_event(event)
                

            # Update
            self.uiManager.update(dt)
            self.input_screen.update()
            
            # Draw
            self.display_surface.fill("white")
            self.input_screen.draw()
            self.uiManager.draw_ui(self.display_surface)


            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    HopfieldIllustrationApp()