import os
import pygame
pygame.font.init()

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
FPS = 60

# Bird Settings

BIRD_HEIGHT = 40
BIRD_WIDTH = 50
GRAVITY = 0.5
JUMP_SPEED = 10.5

PIPE_WIDTH = 100
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_SPAWN_X = WINDOW_WIDTH
PIPE_SPAWN_INTERVAL = 100

GROUND_HEIGHT = 50



BIRD_IMGS = [
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))
            ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 30)