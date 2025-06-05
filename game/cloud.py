import pygame
import random
from .config import *

class Cloud:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.x -= 0.8  # Move slower than background
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

class CloudManager:
    def __init__(self, asset_manager):
        self.clouds = []
        self.cloud_sprites = [
            asset_manager.sprites['cloud1'],
            asset_manager.sprites['cloud2'],
            asset_manager.sprites['cloud3']
        ]
        self.spawn_initial_clouds()

    def spawn_initial_clouds(self):
        # Start with 3 non-overlapping clouds
        used_positions = set()
        for i in range(3):
            self._spawn_cloud(used_positions, initial=True)

    def _spawn_cloud(self, used_positions, initial=False):
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            # If initial spawn, spread across screen width
            # If regular spawn, always spawn from right side
            if initial:
                x = random.randint(0, WINDOW_WIDTH)
            else:
                x = WINDOW_WIDTH

            y = random.randint(50, WINDOW_HEIGHT // 2)  # Clouds in upper half
            sprite = random.choice(self.cloud_sprites)
            rect = pygame.Rect(x, y, sprite.get_width(), sprite.get_height())

            # Check for overlap with existing clouds
            overlap = False
            for pos in used_positions:
                cloud_rect = pygame.Rect(pos[0], pos[1], 
                                       sprite.get_width() + 50,  # Add padding
                                       sprite.get_height() + 50)
                if cloud_rect.colliderect(rect):
                    overlap = True
                    break

            if not overlap:
                used_positions.add((x, y))
                self.clouds.append(Cloud(x, y, sprite))
                break

            attempts += 1

    def update(self):
        # Update existing clouds
        used_positions = set((cloud.x, cloud.y) for cloud in self.clouds)
        
        # Remove off-screen clouds
        self.clouds = [cloud for cloud in self.clouds if not cloud.is_off_screen()]
        
        # Spawn new clouds if needed
        if len(self.clouds) < 3:
            self._spawn_cloud(used_positions)

        # Update remaining clouds
        for cloud in self.clouds:
            cloud.update()

    def draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)