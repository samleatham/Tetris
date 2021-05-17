import pygame
import settings
import tetromino
from board import Board

board = Board(settings.WIDTH, settings.HEIGHT)
WIN = pygame.display.set_mode((settings.WIN_RES))


def drawdisplay(board, controlled_block):
    # draw the main game
    WIN.blit(board.draw_board(settings.WIN_RES, controlled_block), (0, 0))
    # draw the score
    # draw the list of upcomming blocks
    # draw the held block
    pygame.display.update()


# this method will have the animation of the blocks filling up the screen
def gameOver():
    waitTime = 40
    count = 0
    for empty_i, empty_j in board.get_empties():
        count += 1
        if count % 20 == 0:
            waitTime -= 2
        board.board[empty_i][empty_j] = 1
        WIN.blit(board.draw_board(settings.WIN_RES), (0, 0))
        pygame.time.delay(waitTime)
        pygame.display.update()


def hold_block(block, held, board):
    if held > 0:
        newblock = held
        held = block.index
        block = tetromino.createTet(
            settings.START_X, 0, board, newblock)
    else:
        held = block.index
        block = tetromino.randomTet(
            settings.START_X, 0, board, newblock)
    return block, held


def handle_movment(block, moves):
    print(moves)
    if moves["sideways"]:
        block.movesideways(moves["sideways"])
    if moves["rotate"]:
        block.rotate()

    if moves["slam"]:
        block.slam()
    elif moves["down"]:
        block.movedown()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    canHold = True
    frame = 0
    held = -1
    SCORE = 0
    pygame.time.set_timer(settings.MOVE_DOWN, 500)
    controledBlock = tetromino.randomTet(5, 0, board)
    while running:
        clock.tick(settings.FPS)
        linescleared = 0
        move = {"sideways": 0, "down": 0, "slam": 0, "rotate": 0}
        frame = (frame + 1) % 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == settings.GAME_OVER:
                running = False
                gameOver()
                break

            if event.type == settings.LINE_CLEARED:
                print("yay")
                linescleared += 1

            if event.type == settings.BLOCK_PLACED:
                board.add_block(controledBlock)
                controledBlock = tetromino.randomTet(
                    settings.START_X, 0, board)
                canHold = True

            if event.type == settings.MOVE_DOWN:
                move["down"] = 1

            # read control inputs
            if event.type == pygame.KEYDOWN:

                if event.key == settings.CONTROLS["down"]:
                    move["down"] = 1

                if event.key == settings.CONTROLS["slam"]:
                    move["slam"] = 1

                if event.key == settings.CONTROLS["right"]:
                    move["sideways"] += 1

                if event.key == settings.CONTROLS["left"]:
                    move["sideways"] -= 1

                if event.key == settings.CONTROLS["rotate"]:
                    controledBlock.rotate()

                if event.key == settings.CONTROLS["hold"] and canHold:
                    controledBlock, held = hold_block(
                        controledBlock, held, board)

        print(controledBlock.get_spaces())
        handle_movment(controledBlock, move)

        # update the score
        if linescleared:
            SCORE += linescleared
            print("Line Cleared! Score: " + str(SCORE))

        drawdisplay(board, controledBlock)


if __name__ == "__main__":
    main()
