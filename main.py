import pygame
import settings
import tetromino
from board import Board


def drawdisplay(board, window, controlled_block):
    window.blit(board.draw_board(settings.WIN_RES, controlled_block), (0, 0))
    pygame.display.update()


# this method will have the animation of the blocks filling up the screen
def gameOver(board, window):
    waitTime = 40
    count = 0
    for empty_i, empty_j in board.get_empties():
        count += 1
        if count % 20 == 0:
            waitTime -= 2
        board.board[empty_i][empty_j] = 1
        window.blit(board.draw_board(settings.WIN_RES), (0, 0))
        pygame.time.delay(waitTime)
        pygame.display.update()


def main():

    board = Board(settings.WIDTH, settings.HEIGHT)

    clock = pygame.time.Clock()
    running = True
    held = None
    frame = 0
    points = 0
    controledBlock = tetromino.randomTet(5, 0, board)
    while running:
        linescleared = False
        WIN = pygame.display.set_mode((settings.WIN_RES))
        clock.tick(settings.FPS)
        frame = (frame + 1) % 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == settings.GAME_OVER:
                running = False
                gameOver(board, WIN)
                break

            if event.type == settings.LINE_CLEARED:
                print("yay")
                linescleared = True
                points += 1

            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROLS["down"]:
                    frame = 0
                    # if the down button is held the tetromino will move down one until it hits the bottom
                    if controledBlock.movedown():
                        board.add_block(controledBlock)
                        controledBlock = tetromino.randomTet(
                            settings.START_X, 0, board)

                if event.key == settings.CONTROLS["slam"]:
                    while True:
                        if controledBlock.movedown():
                            board.add_block(controledBlock)
                            controledBlock = tetromino.randomTet(
                                settings.START_X, 0, board)
                            break

                if event.key == settings.CONTROLS["right"]:
                    controledBlock.movesideways(1)

                if event.key == settings.CONTROLS["left"]:
                    controledBlock.movesideways(-1)

                if event.key == settings.CONTROLS["rotate"]:
                    controledBlock.rotate()

        if linescleared:
            print("Line Cleared! Score: " + str(points))

        # print(controledBlock.get_spaces())

        if frame >= 30:
            frame = 0
            if controledBlock.movedown():
                board.add_block(controledBlock)
                controledBlock = tetromino.randomTet(
                    settings.START_X, 0, board)
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
