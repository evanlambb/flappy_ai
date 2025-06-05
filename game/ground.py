# this is a class for the ground and then the collisons... 

import pygame 
from .config import * # i dont think that i need this...



class Ground():
    def __init__(self, ceiling=False, sprite=None):
        if sprite:
            self.sprite = sprite
            # Calculate how many times we need to tile the sprite
            self.tile_count = (WINDOW_WIDTH // sprite.get_width()) + 2  # +2 for smooth scrolling
        else:
            self.sprite = None
            
        if ceiling:
            self.x, self.y = 0, -200
        else:
            self.x, self.y = 0, WINDOW_HEIGHT - GROUND_HEIGHT
            
        self.rect = pygame.Rect(self.x, self.y, WINDOW_WIDTH, GROUND_HEIGHT)

    def draw(self, screen):
        if self.sprite:
            # Draw sprite repeatedly to fill ground width
            sprite_width = self.sprite.get_width()
            for i in range(self.tile_count):
                x_pos = self.x + (i * sprite_width)
                screen.blit(self.sprite, (x_pos, self.y))
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
