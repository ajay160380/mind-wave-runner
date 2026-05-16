import pygame
from settings import *

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    print("Game window initialized successfully!")
    
    # Note: Core game loop will be implemented next.
    pygame.quit()

if __name__ == "__main__":
    main()
