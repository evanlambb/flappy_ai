import pygame 
from .config import *

class BasePipe:
    def __init__(self, y, sprite=None):
        self.x = PIPE_SPAWN_X
        self.y = y
        self.height = WINDOW_HEIGHT - y  # Default height
        
        if sprite:
            # Scale width only, keeping aspect ratio
            orig_width, orig_height = sprite.get_size()
            scale_factor = PIPE_WIDTH / orig_width
            scaled_height = int(orig_height * scale_factor)
            
            # Scale sprite to match pipe width
            self.sprite_segment = pygame.transform.scale(
                sprite,
                (PIPE_WIDTH, scaled_height)
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
            # Calculate area to clip from sprite
            clip_rect = pygame.Rect(
                0,                          # x start of clip
                0,                          # y start of clip
                PIPE_WIDTH,                 # width of clip
                min(self.height,           # Take whichever is smaller:
                    self.sprite_segment.get_height())  # sprite height or pipe height
            )
            
            # Draw only the clipped portion
            screen.blit(
                self.sprite_segment,        # source surface
                (self.x, self.y),          # destination position
                clip_rect                   # area to clip from source
            )
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
        
        # Flip sprite after base initialization is complete
        if self.sprite_segment:
            self.sprite_segment = pygame.transform.flip(self.sprite_segment, False, True)
            
    def draw(self, screen):
        if self.sprite_segment:
            # For top pipe, we draw from top down
            clip_height = min(self.height, self.sprite_segment.get_height())
            clip_rect = pygame.Rect(
            0,
            self.sprite_segment.get_height() - clip_height,  # Clip from bottom of flipped sprite
            PIPE_WIDTH,
            clip_height
            )

            
            # Draw the flipped sprite starting from the top (y=0)
            screen.blit(
                self.sprite_segment,
                (self.x, 0),  # Always start at top of screen
                clip_rect
            )
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)


class BottomPipe(BasePipe):
    def __init__(self, y, sprite=None):
        super().__init__(y, sprite)
        # Bottom pipe extends from gap position to bottom of screen
        self.height = WINDOW_HEIGHT - y
        self.rect = pygame.Rect(self.x, y, PIPE_WIDTH, self.height)