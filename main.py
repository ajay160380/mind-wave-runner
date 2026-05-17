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
    
    # Main game loop
    running = True
    game_active = True
    
    while running:
        # Get gestures from webcam
        is_jumping, is_ducking = hand_tracker.process_frame()
        
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
        screen.fill(WHITE)
        
        # Draw ground line
        pygame.draw.line(screen, GRAY, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 2)
        
        # Draw obstacles
        for obs in obstacles:
            obs.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw Score
        score_text = font.render(f"Score: {score // 10}", True, BLACK)
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
