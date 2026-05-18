import pygame
import sys
import random
from settings import *
from player import Player
from obstacle import Obstacle
from hand_tracker import HandTracker

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Set up the clock
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 32, bold=True)
    
    # Initialize game objects
    player = Player()
    obstacles = []
    spawn_timer = 0
    SPAWN_INTERVAL = random.randint(60, 120)  # Frames between spawns
    score = 0
    
    # Initialize Hand Tracker
    hand_tracker = HandTracker()
    
    # Load background images
    bg_stars = pygame.image.load("assets/bg_stars.png").convert()
    bg_mountains = pygame.image.load("assets/bg_mountains.png").convert_alpha()
    bg_floor = pygame.image.load("assets/bg_floor.png").convert_alpha()
    
    # Parallax scrolling coordinates
    stars_x = 0.0
    mountains_x = 0.0
    floor_x = 0.0
    
    # Main game loop
    running = True
    game_active = True
    
    while running:
        # Get gestures from webcam
        is_jumping, is_ducking, cam_surface = hand_tracker.process_frame()
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    player.jump()
                if event.key == pygame.K_DOWN and game_active:
                    player.duck()
                if event.key == pygame.K_UP and game_active:
                    player.unduck()
                if event.key == pygame.K_r and not game_active:
                    # Restart the game
                    game_active = True
                    obstacles.clear()
                    score = 0
                    spawn_timer = 0
                    player.y = player.ground_y
                    player.vel_y = 0
                    player.unduck()
        
        if game_active:
            # Apply gestures
            if is_jumping:
                player.jump()
            elif is_ducking:
                player.duck()
            else:
                player.unduck()
                
            # 2. Update Game State
            player.update()
            score += 1
            
            # Scroll backgrounds at different speeds (Parallax)
            stars_x -= 0.2
            if stars_x <= -WIDTH:
                stars_x = 0.0
                
            mountains_x -= 1.0
            if mountains_x <= -WIDTH:
                mountains_x = 0.0
                
            floor_x -= 5.0
            if floor_x <= -WIDTH:
                floor_x = 0.0
            
            # Spawn obstacles at random intervals
            spawn_timer += 1
            if spawn_timer >= SPAWN_INTERVAL:
                obstacles.append(Obstacle())
                spawn_timer = 0
                SPAWN_INTERVAL = random.randint(60, 120)
            
            # Update all obstacles, check collision, and remove off-screen ones
            for obs in obstacles[:]:
                obs.update()
                
                # AABB Collision Detection
                if player.rect.colliderect(obs.rect):
                    game_active = False
                    break
                
                if obs.is_off_screen():
                    obstacles.remove(obs)
        
        # 3. Render
        # Draw background layers (Parallax)
        screen.blit(bg_stars, (stars_x, 0))
        screen.blit(bg_stars, (stars_x + WIDTH, 0))
        
        screen.blit(bg_mountains, (mountains_x, 0))
        screen.blit(bg_mountains, (mountains_x + WIDTH, 0))
        
        screen.blit(bg_floor, (floor_x, HEIGHT - 100))
        screen.blit(bg_floor, (floor_x + WIDTH, HEIGHT - 100))
        
        # Draw obstacles
        for obs in obstacles:
            obs.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw the PiP webcam feed in the top right corner
        if cam_surface:
            # Draw a glowing cyber cyan border around the PiP
            pygame.draw.rect(screen, (0, 240, 255), (WIDTH - 182, 18, 164, 124), 2)
            screen.blit(cam_surface, (WIDTH - 180, 20))
        
        # Draw Score
        score_text = font.render(f"Score: {score // 10}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Draw Game Over Text
        if not game_active:
            go_text = font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(go_text, go_rect)
        
        pygame.display.flip()
        
        # 4. Cap the frame rate
        clock.tick(FPS)
    
    hand_tracker.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
