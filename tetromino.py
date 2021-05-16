import random


def boardSpotTaken(x, y, board):
    return x < 0 or y < 0 or y >= len(board) or x >= len(board[0]) or board[y][x]

class Tetromino():

    def __init__(self, x, y, board, block1, block2, block3):
        self.x = x
        self.y = y
        self.blocks = [block1, block2, block3]
        self.board = board

    # returns a list of spaces that the tetremino occupies
    # optional parameters allow to check
    def get_spaces(self, x_add=0, y_add=0):
        return [(self.x + x_add, self.y + y_add)] + [(x + self.x + x_add, y + self.y + y_add) for x, y in self.blocks]

        # attempts to move the piece down a space
        # returns true if the piece has hit the floor

    def get_rotated_spaces(self, x_add=0):
        return [(self.x + x_add, self.y)] + [(y + self.x + x_add, -x + self.y) for x, y in self.blocks]

    def movedown(self):
        # checks all the coordinates of the blocks if they were moved 1 space down
        for coordinate in self.get_spaces(0, 1):
            if self.board.check_collisions(coordinate[0], coordinate[1]):
                return True
        self.y += 1
        return False

    # attempts to move the piece in the direction
    def movesideways(self, dir):
        canMove = True
        for coordinate in self.get_spaces(dir):
            if self.board.check_collisions(coordinate[0], coordinate[1]):
                canMove = False
                break
        self.x += dir * canMove

    def rotate(self):
        for x_delta in [0, -1, 1]:
            # tries to find a way to rotate the block
            canRotate = True
            for coordinate in self.get_rotated_spaces(x_delta):
                if self.board.check_collisions(coordinate[0], coordinate[1]):
                    canRotate = False
                    break
            if canRotate:
                self.x += x_delta
                for i, block in enumerate(self.blocks):
                    self.blocks[i] = (block[1], -block[0])
                return


def randomTet(x, y, board):
    tets = [SquareTet, LTet, LFlipTet, STet, SFlipTet, LongTet, TTet]
    return random.choice(tets)(x, y, board)


class SquareTet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (1, 0), (0, 1), (1, 1))

    def rotate(self):
        # rotating a square block doesnt change anything so the method is overwritten
        return True


class LTet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (-1, 1), (-1, 0), (1, 0))


class LFlipTet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (1, 1), (1, 0), (-1, 0))


class STet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (0, 1), (-1, 1), (1, 0))


class SFlipTet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (0, 1), (1, 1), (-1, 0))


class LongTet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (-1, 0), (1, 0), (2, 0))


class TTet(Tetromino):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, (-1, 0), (1, 0), (0, 1))
