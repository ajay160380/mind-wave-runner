import os
from PIL import Image, ImageDraw

def create_assets():
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # ------------------ PALETTE ------------------
    CYAN = (0, 240, 255, 255)
    GLOW_CYAN = (0, 240, 255, 100)
    DARK_BLUE = (0, 30, 80, 255)
    LIGHT_BLUE = (0, 102, 255, 255)
    PINK = (255, 0, 127, 255)
    GLOW_PINK = (255, 0, 127, 100)
    NEON_RED = (255, 0, 85, 255)
    GLOW_RED = (255, 0, 85, 100)
    DARK_RED = (120, 0, 30, 255)
    TRANSPARENT = (0, 0, 0, 0)
    DEEP_PURPLE = (8, 0, 21, 255)
    GRID_PURPLE = (40, 0, 80, 255)
    
    # =========================================================================
    # 1. PLAYER RUN 1 (40x60) - Cyber Runner Leg Position 1
    # =========================================================================
    im = Image.new("RGBA", (40, 60), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Head & Helmet (visor)
    draw.ellipse([12, 4, 28, 20], fill=DARK_BLUE, outline=CYAN, width=2)
    draw.rectangle([18, 10, 28, 14], fill=CYAN) # Visor glow
    
    # Torso
    draw.rectangle([10, 21, 30, 40], fill=LIGHT_BLUE, outline=CYAN, width=2)
    # Neon core line
    draw.line([20, 24, 20, 37], fill=CYAN, width=2)
    
    # Legs (Left leg forward, right leg back)
    # Left Leg (Forward)
    draw.line([15, 41, 10, 50], fill=CYAN, width=3)
    draw.line([10, 50, 22, 58], fill=CYAN, width=3)
    # Right Leg (Back)
    draw.line([25, 41, 32, 48], fill=CYAN, width=3)
    draw.line([32, 48, 28, 58], fill=CYAN, width=3)
    
    # Arms (Running pose)
    draw.line([10, 24, 5, 32], fill=CYAN, width=2)
    draw.line([30, 24, 35, 30], fill=CYAN, width=2)
    
    im.save("assets/player_run1.png")
    
    # =========================================================================
    # 2. PLAYER RUN 2 (40x60) - Cyber Runner Leg Position 2
    # =========================================================================
    im = Image.new("RGBA", (40, 60), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Head & Helmet (visor)
    draw.ellipse([12, 4, 28, 20], fill=DARK_BLUE, outline=CYAN, width=2)
    draw.rectangle([18, 10, 28, 14], fill=CYAN)
    
    # Torso
    draw.rectangle([10, 21, 30, 40], fill=LIGHT_BLUE, outline=CYAN, width=2)
    draw.line([20, 24, 20, 37], fill=CYAN, width=2)
    
    # Legs (Right leg forward, left leg back)
    # Left Leg (Back)
    draw.line([15, 41, 8, 48], fill=CYAN, width=3)
    draw.line([8, 48, 12, 58], fill=CYAN, width=3)
    # Right Leg (Forward)
    draw.line([25, 41, 30, 50], fill=CYAN, width=3)
    draw.line([30, 50, 18, 58], fill=CYAN, width=3)
    
    # Arms (Running pose alternate)
    draw.line([10, 24, 4, 30], fill=CYAN, width=2)
    draw.line([30, 24, 36, 32], fill=CYAN, width=2)
    
    im.save("assets/player_run2.png")
    
    # =========================================================================
    # 3. PLAYER JUMP (40x60) - Dynamic Jump Pose
    # =========================================================================
    im = Image.new("RGBA", (40, 60), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Head tilted slightly back
    draw.ellipse([12, 2, 28, 18], fill=DARK_BLUE, outline=CYAN, width=2)
    draw.rectangle([18, 6, 28, 10], fill=CYAN)
    
    # Torso angled
    draw.polygon([(10, 19), (30, 19), (28, 38), (8, 38)], fill=LIGHT_BLUE, outline=CYAN)
    draw.line([19, 21, 18, 36], fill=CYAN, width=2)
    
    # Legs bent up
    draw.line([12, 39, 6, 45], fill=CYAN, width=3)
    draw.line([6, 45, 14, 52], fill=CYAN, width=3)
    
    draw.line([26, 39, 32, 45], fill=CYAN, width=3)
    draw.line([32, 45, 24, 52], fill=CYAN, width=3)
    
    # Arms up/back
    draw.line([10, 22, 2, 14], fill=CYAN, width=2)
    draw.line([30, 22, 38, 14], fill=CYAN, width=2)
    
    im.save("assets/player_jump.png")
    
    # =========================================================================
    # 4. PLAYER DUCK 1 (40x30) - Cyber Slide Pose 1
    # =========================================================================
    im = Image.new("RGBA", (40, 30), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Head & Helmet positioned low and forward
    draw.ellipse([20, 4, 36, 20], fill=DARK_BLUE, outline=CYAN, width=2)
    draw.rectangle([26, 10, 36, 14], fill=CYAN)
    
    # Torso horizontal
    draw.rectangle([6, 12, 22, 26], fill=LIGHT_BLUE, outline=CYAN, width=2)
    draw.line([10, 19, 18, 19], fill=CYAN, width=2)
    
    # Legs tucked behind
    draw.line([6, 19, 1, 14], fill=CYAN, width=3)
    draw.line([1, 14, 4, 25], fill=CYAN, width=3)
    
    im.save("assets/player_duck1.png")
    
    # =========================================================================
    # 5. PLAYER DUCK 2 (40x30) - Cyber Slide Pose 2 (Leg flicker)
    # =========================================================================
    im = Image.new("RGBA", (40, 30), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Head & Helmet positioned low and forward
    draw.ellipse([20, 4, 36, 20], fill=DARK_BLUE, outline=CYAN, width=2)
    draw.rectangle([26, 10, 36, 14], fill=CYAN)
    
    # Torso horizontal
    draw.rectangle([6, 12, 22, 26], fill=LIGHT_BLUE, outline=CYAN, width=2)
    draw.line([10, 19, 18, 19], fill=CYAN, width=2)
    
    # Legs tucked behind (alternate frame)
    draw.line([6, 19, 2, 22], fill=CYAN, width=3)
    draw.line([2, 22, 0, 16], fill=CYAN, width=3)
    
    im.save("assets/player_duck2.png")
    
    # =========================================================================
    # 6. OBSTACLE TALL (30x70) - Laser Barrier
    # =========================================================================
    im = Image.new("RGBA", (30, 70), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Outer cage
    draw.rectangle([4, 4, 26, 66], outline=NEON_RED, fill=DARK_RED, width=2)
    # Glowing diagonal laser lines
    draw.line([4, 15, 26, 25], fill=PINK, width=2)
    draw.line([4, 35, 26, 45], fill=PINK, width=2)
    draw.line([4, 55, 26, 65], fill=PINK, width=2)
    # Center core glows neon red
    draw.rectangle([12, 10, 18, 60], fill=PINK)
    
    im.save("assets/obstacle_tall.png")
    
    # =========================================================================
    # 7. OBSTACLE WIDE (45x45) - Cyber Spiked Drone
    # =========================================================================
    im = Image.new("RGBA", (45, 45), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Center sphere
    draw.ellipse([10, 10, 35, 35], fill=DARK_RED, outline=NEON_RED, width=3)
    # Glowing core
    draw.ellipse([17, 17, 28, 28], fill=PINK)
    
    # Spikes (lines radiating outward)
    spikes = [
        ([22, 10], [22, 2]),    # Top
        ([22, 35], [22, 43]),   # Bottom
        ([10, 22], [2, 22]),    # Left
        ([35, 22], [43, 22]),   # Right
        ([13, 13], [6, 6]),     # Top-Left
        ([31, 13], [38, 6]),     # Top-Right
        ([13, 31], [6, 38]),     # Bottom-Left
        ([31, 31], [38, 38])     # Bottom-Right
    ]
    for start, end in spikes:
        draw.line(start + end, fill=NEON_RED, width=3)
        
    im.save("assets/obstacle_wide.png")
    
    # =========================================================================
    # 8. OBSTACLE SMALL (25x40) - Cyber Cactus / Neon Spike
    # =========================================================================
    im = Image.new("RGBA", (25, 40), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Base spike
    draw.polygon([(12, 2), (2, 38), (22, 38)], fill=DARK_RED, outline=NEON_RED)
    draw.line([12, 5, 12, 37], fill=PINK, width=2)
    
    # Mini side spikes
    draw.line([7, 20, 1, 15], fill=NEON_RED, width=2)
    draw.line([17, 25, 23, 20], fill=NEON_RED, width=2)
    
    im.save("assets/obstacle_small.png")
    
    # =========================================================================
    # 9. BACKGROUND STARS (800x400) - Starry Synthwave Space
    # =========================================================================
    im = Image.new("RGBA", (800, 400), DEEP_PURPLE)
    draw = ImageDraw.Draw(im)
    
    # Draw a soft radial sun gradient near the bottom center
    import math
    sun_x, sun_y = 400, 300
    for r in range(120, 0, -2):
        alpha = int((1.0 - (r / 120.0)) * 60)
        sun_color = (255, 0, 127, alpha)
        # Create a layered ellipse
        draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=sun_color)
        
    # Draw lines cut into the sun (classic synthwave retro sun)
    for y_cut in range(sun_y - 120, sun_y + 120, 15):
        thick = int((y_cut - (sun_y - 120)) / 15.0) + 1
        draw.line([sun_x - 130, y_cut, sun_x + 130, y_cut], fill=DEEP_PURPLE, width=thick)
        
    # Generate random starry pixels
    import random
    random.seed(42) # Deterministic stars
    for _ in range(80):
        sx = random.randint(0, 799)
        sy = random.randint(0, 260)
        s_size = random.choice([1, 2])
        color = random.choice([CYAN, PINK, (255, 255, 255, 255)])
        if s_size == 1:
            draw.point((sx, sy), fill=color)
        else:
            draw.ellipse([sx, sy, sx+1, sy+1], fill=color)
            
    im.save("assets/bg_stars.png")
    
    # =========================================================================
    # 10. BACKGROUND MOUNTAINS (800x400) - Synthwave Neon Mountain Grid
    # =========================================================================
    im = Image.new("RGBA", (800, 400), TRANSPARENT)
    draw = ImageDraw.Draw(im)
    
    # Vector digital mountains outlines
    # Mountain 1 (Left)
    draw.polygon([(0, 380), (150, 160), (300, 380)], fill=(20, 0, 40, 200), outline=PINK)
    draw.line([150, 160, 150, 380], fill=GLOW_PINK, width=2)
    # Mountain 2 (Right)
    draw.polygon([(500, 380), (680, 120), (800, 380)], fill=(20, 0, 40, 200), outline=PINK)
    draw.line([680, 120, 680, 380], fill=GLOW_PINK, width=2)
    # Mountain 3 (Center, slightly behind)
    draw.polygon([(200, 380), (420, 180), (600, 380)], fill=(10, 0, 30, 200), outline=CYAN)
    draw.line([420, 180, 420, 380], fill=GLOW_CYAN, width=2)
    
    im.save("assets/bg_mountains.png")
    
    # =========================================================================
    # 11. NEON FLOOR (800x100) - Retro Floor Grid
    # =========================================================================
    im = Image.new("RGBA", (800, 100), DEEP_PURPLE)
    draw = ImageDraw.Draw(im)
    
    # Top border line (glowing cyan floor line)
    draw.line([0, 2, 800, 2], fill=CYAN, width=4)
    draw.line([0, 4, 800, 4], fill=GLOW_CYAN, width=8)
    
    # Horizontal grid lines with perspective spacing
    grid_y_positions = [2, 10, 22, 38, 58, 82, 100]
    for gy in grid_y_positions:
        draw.line([0, gy, 800, gy], fill=GRID_PURPLE, width=2)
        
    # Perspective vanishing lines (vertical perspective)
    for offset in range(-400, 1200, 80):
        # Line from horizon point (vanishing point at screen width/2, height=0) to bottom edge
        # Horizon vanishing point is (400, 2)
        draw.line([400, 2, offset, 100], fill=GRID_PURPLE, width=2)
        
    im.save("assets/bg_floor.png")
    
    print("All custom assets successfully created inside assets/ directory!")

if __name__ == "__main__":
    create_assets()
