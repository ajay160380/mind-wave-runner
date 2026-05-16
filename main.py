import pygame
import sys
from settings import *

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Set up the clock
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 2. Update Game State
        
        # 3. Render
        screen.fill(WHITE)
        pygame.display.flip()
        
        # 4. Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
