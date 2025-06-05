import pygame 
from .config import *

class Bird:
    def __init__(self, x, y, sprite=None):
        self.x = x
        self.y = y
        self.velocity = 0
        self.sprite = sprite
        self.rotated_sprite = sprite
        self.angle = 0  # 0 degrees is horizontal
        if sprite:
            self.rect = sprite.get_rect(center=(x, y))
        else:
            self.rect = pygame.Rect(x, y, BIRD_WIDTH, BIRD_HEIGHT)

    def jump(self):
        self.velocity = -JUMP_SPEED
        self.angle = 45  # Point upward when jumping

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        
        # Update position
        self.y += self.velocity
        
        # Update rotation based on velocity
        if self.velocity < 0:  # Moving upward
            self.angle = 30
        else:  # Falling
            # Gradually rotate downward
            self.angle = max(-90, 30 - self.velocity * 4)
        
        # Update collision rect
        self.rect.y = self.y

    def draw(self, screen):
        if self.sprite:
            # Store center position before rotation
            center = self.rect.center
            
            # Rotate sprite
            self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
            
            # Get new rect and maintain center position
            self.rect = self.rotated_sprite.get_rect(center=center)
            
            # Draw rotated sprite
            screen.blit(self.rotated_sprite, self.rect)
        else:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)