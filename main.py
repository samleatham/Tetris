import pygame
import os
import settings


def print2d(board):
    for row in board:
        print(row)


def drawdisplay(board, window):
    # makes a default rectangle based on the size of the window
    square = pygame.Rect(0, 0, settings.WIN_WIDTH // len(board[0]),
                         settings.WIN_HEIGHT // len(board))
    for row in board:
        for block in row:
            if block:
                pygame.draw.rect(window, settings.WHITE, square)
            else:
                pygame.draw.rect(window, settings.BLACK, square)
            pygame.draw.rect(window, settings.BLACK, square, 5)
            square.x += square.width
        square.y += square.height
        square.x = 0
    pygame.display.update()


def main():
    WIN = pygame.display.set_mode((settings.WIN_RES))
    board = [[(i % 2 + j % 2) % 2 for i in range(settings.WIDTH)]
             for j in range(settings.HEIGHT)]

    clock = pygame.time.Clock()
    running = True
    frame = 0
    while running:
        clock.tick(settings.FPS)
        frame = (frame + 1) % 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        if frame % 30 == 0:
            print2d(board)
            for row in board:
                for i, item in enumerate(row):
                    row[i] = (item + 1) % 2

        drawdisplay(board, WIN)


if __name__ == "__main__":
    main()
