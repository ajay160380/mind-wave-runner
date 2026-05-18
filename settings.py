# settings.py
from PIL import Image
import pygame

# Screen Dimensions
WIDTH = 800
HEIGHT = 400

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game Configuration
FPS = 60
TITLE = "Mind-Wave Gesture Runner"

def load_png(filepath, has_alpha=True):
    """Load a PNG image using PIL and return it as a Pygame Surface,
    bypassing SDL_image compilation dependencies on macOS/Unix.
    """
    mode = "RGBA" if has_alpha else "RGB"
    try:
        pil_image = Image.open(filepath).convert(mode)
        raw_data = pil_image.tobytes()
        size = pil_image.size
        # Create Pygame surface directly from the pixel buffer
        surface = pygame.image.frombuffer(raw_data, size, mode)
        if has_alpha:
            return surface.convert_alpha()
        return surface.convert()
    except Exception as e:
        print(f"Error loading image {filepath}: {e}")
        # Return a fallback colored block surface
        fallback = pygame.Surface((40, 60))
        fallback.fill(RED if "obstacle" in filepath else BLUE)
        return fallback

