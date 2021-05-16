import pygame
import os
import settings
import copy
import tetromino
from tetromino import SquareTet, LTet


def print2d(board):
    for row in board:
        print(row)


def removeLine(board, line):
    for i in range(line, 0, -1):
        board[i] = board[i - 1]
    board[0] = [0 for i in range(len(board[0]))]
    return board


def checkLines(board):
    for i, row in enumerate(board):
        if sum(row) == len(row):
            # a full line has been completed and should be removed
            board = removeLine(board, i)
            settings.POINTS += 1
    if sum(board[0]) > 0:
        board = [[1 for i in range(settings.WIDTH)]
                 for j in range(settings.HEIGHT + 1)]
    return board


def addBlocktoBoard(board, block):
    temp_board = copy.deepcopy(board)
    for x, y in block.get_spaces():
        print(x, y)
        print(len(temp_board), len(temp_board[y]))
        temp_board[y][x] = 1
    return temp_board


def drawdisplay(board, window, controlled_block):
    # makes a default rectangle based on the size of the window
    square = pygame.Rect(0, 0, settings.WIN_WIDTH // len(board[0]),
                         settings.WIN_HEIGHT // (len(board) - 1))
    for row in addBlocktoBoard(board, controlled_block)[1:]:
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
    board = [[0 for i in range(settings.WIDTH)]
             for j in range(settings.HEIGHT + 1)]

    clock = pygame.time.Clock()
    running = True
    frame = 0
    controledBlock = tetromino.randomTet(5, 0)
    while running:
        clock.tick(settings.FPS)
        frame = (frame + 1) % 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROLS["down"]:
                    frame = 0
                    # if the down button is held the tetromino will move down one until it hits the bottom
                    if controledBlock.movedown(board):
                        board = addBlocktoBoard(board, controledBlock)
                        controledBlock = tetromino.randomTet(
                            settings.START_X, 0)

                if event.key == settings.CONTROLS["slam"]:
                    while True:
                        if controledBlock.movedown(board):
                            board = checkLines(
                                addBlocktoBoard(board, controledBlock))
                            controledBlock = tetromino.randomTet(
                                settings.START_X, 0)
                            break

                if event.key == settings.CONTROLS["right"]:
                    controledBlock.movesideways(board, 1)

                if event.key == settings.CONTROLS["left"]:
                    controledBlock.movesideways(board, -1)

                if event.key == settings.CONTROLS["rotate"]:
                    controledBlock.rotate(board)

        print(controledBlock.get_spaces())

        if frame >= 30:
            frame = 0
            if controledBlock.movedown(board):
                board = checkLines(addBlocktoBoard(board, controledBlock))
                controledBlock = tetromino.randomTet(settings.START_X, 0)
        # print(controledBlock.get_spaces())

        """
        if frame % 30 == 0:
            print2d(board)
            for row in board:
                for i, item in enumerate(row):
                    row[i] = (item + 1) % 2
        """

        drawdisplay(board, WIN, controledBlock)


if __name__ == "__main__":
    main()
