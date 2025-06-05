import pygame
import sys
import math
import random
from game.bird import Bird
from game.ground import Ground
from game.pipe import BasePipe, TopPipe, BottomPipe 
from game.cloud import Cloud, CloudManager  # Add this line
from game.config import *

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.asset_manager = AssetManager()  # Removed pipe_length parameter
        self.bird = Bird(WINDOW_WIDTH  // 3, WINDOW_HEIGHT // 2, self.asset_manager.sprites["bird"])
        self.ground = Ground(False, self.asset_manager.sprites["ground"])
        self.ceiling = Ground(True)
        self.running = True
        self.game_started = False  
        self.pipes = []
        self.score = 0

        bg = pygame.image.load("assets/bg.png").convert()
        self.bg = pygame.transform.scale(bg, (480, 590))
        self.bg_width = self.bg.get_width()
        self.scroll = 0
        self.tiles = math.ceil(WINDOW_WIDTH / self.bg_width) + 1

        
        self.ground_width = self.ground.sprite.get_width()
        self.ground_scroll = 0
        self.ground_tiles = math.ceil(WINDOW_WIDTH / self.ground_width) + 1


        # Cloud manager
        self.cloud_manager = CloudManager(self.asset_manager)

    def handle_events(self):

        for pipe in self.pipes:
            if self.isColliding(self.bird.rect, pipe.rect):
                self.game_over()

            elif pipe.is_off_screen():
                self.pipes.remove(pipe)
            elif isinstance(pipe, BottomPipe) and not pipe.scored and self.bird.x > pipe.x:
                self.score += 1
                pipe.scored = True

        if self.isColliding(self.bird.rect, self.ground.rect) or self.isColliding(self.bird.rect, self.ceiling.rect):
            self.game_over()
            
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Add this to handle window close
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:  # Changed from SPACEBAR to KEYDOWN
                if event.key == pygame.K_SPACE:  # Check for spacebar key specifically
                    self.bird.jump()

    def run(self):
        count = 0
        while self.running:
            # Draw everything starting with background
            for i in range(0, self.tiles):
                self.screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))
            self.scroll -= 1

            if abs(self.scroll) > self.bg_width:
                self.scroll = 0
                
            # Draw clouds right after background
            self.cloud_manager.draw(self.screen)

            # Draw rest of game elements
            for i in range(0, self.ground_tiles):
                self.screen.blit(self.ground.sprite, (i * self.ground_width + self.ground_scroll, WINDOW_HEIGHT - GROUND_HEIGHT))
            self.ground_scroll -= 3

            for pipe in self.pipes:
                pipe.draw(self.screen)

            if abs(self.ground_scroll) > self.ground_width:
                self.ground_scroll = 0

            self.bird.draw(self.screen)
            
            # Draw score (moved here so it's always visible)
            if self.game_started:
                font = pygame.font.Font(None, 36)
                text = font.render(f"{self.score}", True, (0, 0, 0))
                text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))
                self.screen.blit(text, text_rect)

            if self.game_started:
                self.handle_events()


                # Update game state
                self.bird.update()
                for pipe in self.pipes:
                    pipe.update()

                # Update clouds
                self.cloud_manager.update()

                if count >= PIPE_SPAWN_INTERVAL:
                    count = 0
                    
                    # Calculate gap position with proper constraints
                    min_height = PIPE_GAP + 75  # Minimum height from top
                    max_height = WINDOW_HEIGHT - 50 - 75  # Leave space at bottom
                    gap_y = random.randint(min_height, max_height)
    
                    # Create pipes
                    pipe_bottom = BottomPipe(gap_y, self.asset_manager.sprites['pipe'])
                    pipe_top = TopPipe(gap_y - PIPE_GAP, self.asset_manager.sprites['pipe'])
                    
                    self.pipes.append(pipe_bottom)
                    self.pipes.append(pipe_top)

                

                count += 1
                
                pygame.display.update()


            else: # game is not started

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_started = True

                font = pygame.font.Font(None, 36)
                text = font.render("Press SPACE to start", True, (0, 0, 0))
                text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def isColliding(self, rect1, rect2):
        if (rect1.y + rect1.height < rect2.y or 
            rect1.y > rect2.y + rect2.height or 
            rect1.x + rect1.width < rect2.x or 
            rect1.x > rect2.x + rect2.width):
            return False
        return True

    def game_over(self):
        self.__init__()



class AssetManager:
    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self._load_assets()

    def _load_assets(self):
        try:
            # Load bird with preserved aspect ratio
            bird_sprite = pygame.image.load('assets/bird.png')
            orig_bird_width, orig_bird_height = bird_sprite.get_size()
            bird_scale_factor = min(BIRD_WIDTH / orig_bird_width, BIRD_HEIGHT / orig_bird_height)
            new_bird_width = int(orig_bird_width * bird_scale_factor)
            new_bird_height = int(orig_bird_height * bird_scale_factor)
            
            self.sprites['bird'] = pygame.transform.scale(
                bird_sprite, 
                (new_bird_width, new_bird_height)
            )
            # Load ground with preserved aspect ratio
            ground_sprite = pygame.image.load('assets/ground.png')
            orig_ground_width, orig_ground_height = ground_sprite.get_size()
            # Scale height to match GROUND_HEIGHT, maintain width aspect ratio
            scale_factor = GROUND_HEIGHT / orig_ground_height
            new_ground_width = int(orig_ground_width * scale_factor)
            new_ground_height = GROUND_HEIGHT

            self.sprites['ground'] = pygame.transform.scale(
                ground_sprite, 
                (new_ground_width, new_ground_height)
            )
            
            
            
            # Just load the pipe sprite without scaling
            self.sprites['pipe'] = pygame.image.load('assets/pipe_v2.png')

            # Load cloud sprites
            for i in range(1, 4):
                cloud_sprite = pygame.image.load(f'assets/cloud_{i}.png')
                # Scale clouds to reasonable size (adjust scale factor as needed)
                scale_factor = 0.15
                new_width = int(cloud_sprite.get_width() * scale_factor)
                new_height = int(cloud_sprite.get_height() * scale_factor)
                self.sprites[f'cloud{i}'] = pygame.transform.scale(
                    cloud_sprite, 
                    (new_width, new_height)
                )

        except pygame.error as e:
            print(f"Error loading sprites: {e}")
            self.sprites['bird'] = None
            self.sprites['pipe'] = None

class Cloud:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.x -= 0.5  # Move slower than background
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0



if __name__ == "__main__":
    game = FlappyBird()

    game.run()