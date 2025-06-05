import pygame 
from .config import *

class BasePipe:
    def __init__(self, y, sprite=None):
        self.x = PIPE_SPAWN_X
        self.y = y
        self.height = WINDOW_HEIGHT - y  # Default height
        
        if sprite:
            # Scale width while preserving aspect ratio
            orig_width, orig_height = sprite.get_size()
            scale_factor = PIPE_WIDTH / orig_width
            self.sprite_segment = pygame.transform.scale(
                sprite,
                (PIPE_WIDTH, int(orig_height * scale_factor))
            )
        else:
            self.sprite_segment = None
            
        self.rect = pygame.Rect(self.x, y, PIPE_WIDTH, self.height)
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED  # Update the x position first
        self.rect.x = self.x  # Then update the rect position

    def draw(self, screen):
        if self.sprite_segment:
            # Tile the sprite vertically
            segment_height = self.sprite_segment.get_height()
            remaining_height = self.height
            current_y = self.y
            
            while remaining_height > 0:
                draw_height = min(segment_height, remaining_height)
                screen.blit(self.sprite_segment, 
                           (self.x, current_y),
                           (0, 0, PIPE_WIDTH, draw_height))
                current_y += draw_height
                remaining_height -= draw_height
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Draw green rectangle

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0


class TopPipe(BasePipe):
    def __init__(self, y, sprite=None):
        super().__init__(y, sprite)
        # Top pipe extends from top (y=0) down to gap position
        self.y = 0  # Start at top of screen
        self.height = y  # Height is the distance to the gap
        self.rect = pygame.Rect(self.x, self.y, PIPE_WIDTH, self.height)

class BottomPipe(BasePipe):
    def __init__(self, y, sprite=None):
        super().__init__(y, sprite)
        # Bottom pipe extends from gap position to bottom of screen
        self.height = WINDOW_HEIGHT - y
        self.rect = pygame.Rect(self.x, y, PIPE_WIDTH, self.height)