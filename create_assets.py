import os
from PIL import Image, ImageDraw

def create_assets():
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # ------------------ CLASSIC DINO PALETTE ------------------
    CHARCOAL = (83, 83, 83)        # Classic Dino/Cactus Dark Grey
    LIGHT_GREY = (247, 247, 247)  # Classic Dino Light Grey Background
    WHITE = (255, 255, 255)        # Cloud White
    GOLD = (245, 166, 35)          # Retro Gold Star
    GOLD_LIGHT = (254, 215, 96)
    TRANSPARENT = (0, 0, 0, 0)
    
    # =========================================================================
    # 1. PIXEL-ART T-REX GENERATOR (64x96, 4-Frame walking loop)
    # =========================================================================
    def draw_pixel_rex(leg_pose="run1"):
        im = Image.new("RGBA", (64, 96), TRANSPARENT)
        draw = ImageDraw.Draw(im)
        
        # Draw T-Rex Body Silhouette block-by-block (Classic 8-bit Pixel look)
        # 1. Snout & Head (Top)
        draw.rectangle([24, 8, 56, 32], fill=CHARCOAL)
        # Eye (White pixel cutout)
        draw.rectangle([44, 12, 48, 16], fill=LIGHT_GREY)
        # Lower Jaw
        draw.rectangle([24, 28, 48, 36], fill=CHARCOAL)
        
        # 2. Neck
        draw.rectangle([20, 32, 36, 44], fill=CHARCOAL)
        
        # 3. Body
        draw.rectangle([16, 40, 40, 68], fill=CHARCOAL)
        
        # 4. Cute Tiny T-Rex Arms
        draw.rectangle([40, 44, 48, 48], fill=CHARCOAL)
        draw.rectangle([44, 48, 48, 52], fill=CHARCOAL)
        
        # 5. Long Tail
        draw.rectangle([0, 48, 16, 60], fill=CHARCOAL)
        draw.rectangle([4, 44, 12, 48], fill=CHARCOAL)
        draw.rectangle([0, 56, 8, 64], fill=CHARCOAL)
        
        # 6. Leg Animation Cycles
        if leg_pose == "run1":
            # Left leg down, right leg up
            draw.rectangle([20, 68, 28, 88], fill=CHARCOAL)
            draw.rectangle([28, 84, 36, 88], fill=CHARCOAL) # Foot
            
            draw.rectangle([32, 68, 40, 76], fill=CHARCOAL)
        elif leg_pose == "run2":
            # Left leg up, right leg down
            draw.rectangle([20, 68, 28, 76], fill=CHARCOAL)
            
            draw.rectangle([32, 68, 40, 88], fill=CHARCOAL)
            draw.rectangle([40, 84, 48, 88], fill=CHARCOAL) # Foot
        elif leg_pose == "run3":
            # Both legs down (Passing pose)
            draw.rectangle([20, 68, 28, 88], fill=CHARCOAL)
            draw.rectangle([28, 84, 36, 88], fill=CHARCOAL)
            
            draw.rectangle([32, 68, 40, 88], fill=CHARCOAL)
            draw.rectangle([40, 84, 48, 88], fill=CHARCOAL)
        elif leg_pose == "run4":
            # Running step 2
            draw.rectangle([18, 68, 26, 88], fill=CHARCOAL)
            draw.rectangle([26, 84, 34, 88], fill=CHARCOAL)
            
            draw.rectangle([34, 68, 42, 80], fill=CHARCOAL)
        elif leg_pose == "jump":
            # Tucked up legs
            draw.rectangle([20, 68, 28, 80], fill=CHARCOAL)
            draw.rectangle([32, 68, 40, 80], fill=CHARCOAL)
            
        return im
        
    for frame_idx, p in enumerate(["run1", "run2", "run3", "run4"]):
        im_run = draw_pixel_rex(p)
        im_run.save(f"assets/player_run{frame_idx+1}.png")
        
    im_jump = draw_pixel_rex("jump")
    im_jump.save("assets/player_jump.png")
    
    # =========================================================================
    # 2. PIXEL-ART DUCKING T-REX GENERATOR (64x48, 2-Frame sliding loop)
    # =========================================================================
    def draw_pixel_duck(pose="duck1"):
        im = Image.new("RGBA", (64, 48), TRANSPARENT)
        draw = ImageDraw.Draw(im)
        
        # Lower T-Rex Bowed Head (Extended snout forward)
        draw.rectangle([32, 12, 64, 30], fill=CHARCOAL)
        draw.rectangle([52, 16, 56, 20], fill=LIGHT_GREY) # Eye
        draw.rectangle([32, 26, 56, 34], fill=CHARCOAL)
        
        # Horizontal low body
        draw.rectangle([12, 20, 36, 40], fill=CHARCOAL)
        
        # Tail
        draw.rectangle([0, 24, 12, 34], fill=CHARCOAL)
        draw.rectangle([0, 32, 8, 38], fill=CHARCOAL)
        
        # Moving running legs (crouched low)
        if pose == "duck1":
            draw.rectangle([16, 40, 24, 46], fill=CHARCOAL)
            draw.rectangle([24, 44, 28, 46], fill=CHARCOAL)
        else:
            draw.rectangle([26, 40, 34, 46], fill=CHARCOAL)
            draw.rectangle([34, 44, 38, 46], fill=CHARCOAL)
            
        return im
        
    im_d1 = draw_pixel_duck("duck1")
    im_d1.save("assets/player_duck1.png")
    
    im_d2 = draw_pixel_duck("duck2")
    im_d2.save("assets/player_duck2.png")
    
    # =========================================================================
    # 3. CLASSIC SINGLE CACTUS (40x60)
    # =========================================================================
    im_small = Image.new("RGBA", (40, 60), TRANSPARENT)
    draw_small = ImageDraw.Draw(im_small)
    
    # Center Stem
    draw_small.rectangle([16, 0, 24, 60], fill=CHARCOAL)
    # Left Arm
    draw_small.rectangle([6, 18, 16, 24], fill=CHARCOAL)
    draw_small.rectangle([6, 8, 12, 24], fill=CHARCOAL)
    # Right Arm
    draw_small.rectangle([24, 28, 34, 34], fill=CHARCOAL)
    draw_small.rectangle([28, 18, 34, 34], fill=CHARCOAL)
    
    im_small.save("assets/obstacle_small.png")
    
    # =========================================================================
    # 4. CLASSIC CACTI CLUSTER (45x100)
    # =========================================================================
    im_tall = Image.new("RGBA", (45, 100), TRANSPARENT)
    draw_tall = ImageDraw.Draw(im_tall)
    
    # 1. Tall Main Cactus
    draw_tall.rectangle([22, 0, 30, 100], fill=CHARCOAL)
    # Left Arm
    draw_tall.rectangle([12, 30, 22, 38], fill=CHARCOAL)
    draw_tall.rectangle([12, 16, 18, 38], fill=CHARCOAL)
    # Right Arm
    draw_tall.rectangle([30, 44, 40, 52], fill=CHARCOAL)
    draw_tall.rectangle([34, 30, 40, 52], fill=CHARCOAL)
    
    # 2. Smaller Cactus clustered beside it
    draw_tall.rectangle([4, 40, 12, 100], fill=CHARCOAL)
    # Right Arm of small cactus overlapping
    draw_tall.rectangle([12, 60, 18, 66], fill=CHARCOAL)
    draw_tall.rectangle([14, 52, 18, 66], fill=CHARCOAL)
    
    im_tall.save("assets/obstacle_tall.png")
    
    # =========================================================================
    # 5. FLAPPING PTERODACTYL DINOSAUR (60x60)
    # =========================================================================
    im_wide = Image.new("RGBA", (60, 60), TRANSPARENT)
    draw_wide = ImageDraw.Draw(im_wide)
    
    # Head & Beak pointing Left
    draw_wide.rectangle([12, 22, 28, 30], fill=CHARCOAL)
    draw_wide.rectangle([18, 20, 24, 24], fill=CHARCOAL) # Head bump
    draw_wide.polygon([(12, 24), (2, 26), (12, 28)], fill=CHARCOAL) # Beak
    
    # Body
    draw_wide.rectangle([28, 24, 46, 32], fill=CHARCOAL)
    
    # Pixel Tail
    draw_wide.polygon([(46, 26), (54, 28), (46, 30)], fill=CHARCOAL)
    
    # Retro Wings Spread
    draw_wide.polygon([(30, 24), (36, 4), (42, 24)], fill=CHARCOAL)   # Wing 1 (Up)
    draw_wide.polygon([(30, 32), (36, 52), (42, 32)], fill=CHARCOAL)  # Wing 2 (Down)
    
    im_wide.save("assets/obstacle_wide.png")
    
    # =========================================================================
    # 6. DINO SKY & PIXEL CLOUDS (800x400)
    # =========================================================================
    im_sky = Image.new("RGBA", (800, 400), TRANSPARENT)
    draw_sky = ImageDraw.Draw(im_sky)
    
    # Clean solid classic Dino light background
    draw_sky.rectangle([0, 0, 800, 400], fill=LIGHT_GREY)
    
    # Draw cute, clean, pixelated white clouds floating in the sky
    def draw_pixel_cloud(cx, cy):
        draw_sky.rectangle([cx, cy, cx + 70, cy + 20], fill=WHITE)
        draw_sky.rectangle([cx + 10, cy - 10, cx + 50, cy], fill=WHITE)
        draw_sky.rectangle([cx + 20, cy - 15, cx + 40, cy - 10], fill=WHITE)
        draw_sky.rectangle([cx - 5, cy + 5, cx + 75, cy + 20], fill=WHITE)
        
    draw_pixel_cloud(120, 70)
    draw_pixel_cloud(440, 45)
    draw_pixel_cloud(680, 85)
    
    im_sky.save("assets/bg_stars.png")
    
    # =========================================================================
    # 7. MINIMALIST DISTANT HILLS (800x400)
    # =========================================================================
    im_hills = Image.new("RGBA", (800, 400), TRANSPARENT)
    draw_hills = ImageDraw.Draw(im_hills)
    
    # Just draw extremely faint, clean classic grey lines in the far background
    # Small bushes/hills
    def draw_pixel_hill(hx, hy, hw, hh):
        draw_hills.ellipse([hx, hy - hh, hx + hw, hy + hh], fill=(235, 235, 235))
        draw_hills.arc([hx, hy - hh, hx + hw, hy + hh], start=180, end=360, fill=(210, 210, 210), width=1)
        
    draw_pixel_hill(80, 360, 160, 45)
    draw_pixel_hill(540, 360, 200, 60)
    
    im_hills.save("assets/bg_mountains.png")
    
    # =========================================================================
    # 8. CLASSIC DOTTED HORIZON ROAD GRID (800x100)
    # =========================================================================
    im_floor = Image.new("RGBA", (800, 100), TRANSPARENT)
    draw_floor = ImageDraw.Draw(im_floor)
    
    # A single solid horizontal line for the road
    draw_floor.line([0, 0, 800, 0], fill=CHARCOAL, width=2)
    
    # Scattered cute classic ground dots/bumps
    import random
    random.seed(42)
    for _ in range(35):
        gx = random.randint(0, 799)
        gy = random.randint(5, 45)
        length = random.choice([2, 4, 6])
        draw_floor.line([gx, gy, gx + length, gy], fill=CHARCOAL, width=1)
        
    im_floor.save("assets/bg_floor.png")
    
    # =========================================================================
    # 9. GOLD STAR COLLECTIBLE (25x25)
    # =========================================================================
    im_core = Image.new("RGBA", (25, 25), TRANSPARENT)
    draw_core = ImageDraw.Draw(im_core)
    
    # Golden star pixel-style shape
    draw_core.ellipse([2, 2, 23, 23], fill=GOLD)
    draw_core.ellipse([5, 5, 20, 20], fill=GOLD_LIGHT)
    draw_core.polygon([(12, 5), (15, 11), (21, 11), (16, 15), (18, 21), (12, 17), (6, 21), (8, 15), (3, 11), (9, 11)], fill=WHITE)
    
    im_core.save("assets/data_core.png")
    
    print("All Chrome Dino minimalist pixel-art assets successfully generated inside assets/ directory!")

if __name__ == "__main__":
    create_assets()
