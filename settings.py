import pygame
import os

# game dimensions

WIDTH, HEIGHT = 10, 20
WIN_WIDTH, WIN_HEIGHT = 400, 800
WIN_RES = (WIN_WIDTH, WIN_HEIGHT)


# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game settings

FPS = 60

# controls

CONTROLS = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "down": pygame.K_DOWN,
            "rotate": pygame.K_UP, "slam": pygame.K_SPACE, "hold": pygame.K_RSHIFT}
