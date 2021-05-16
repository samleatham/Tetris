import copy
import settings
import pygame


class Board:
    def __init__(self, x, y):
        self.board = [[0 for i in range(x)]
                      for j in range(y + 1)]

    def get_board_length(self):
        return len(self.board[0])

    def get_board_height(self):
        return len(self.board)

    def clear_line(self, line):
        for i in range(line, 0, -1):
            self.board[i] = self.board[i - 1]
            # increment the point total by sending a message to the main loop
        self.board[0] = [0 for i in range(self.get_board_length())]

    def check_lines(self):
        for i, row in enumerate(self.board):
            if sum(row) == self.get_board_length():
                self.clear_line(i)

    def add_block(self, block):
        for x, y in block.get_spaces():
            self.board[y][x] = 1
        self.check_lines()
        if sum(self.board[0]) > 0:
            pygame.event.post(pygame.event.Event(settings.GAME_OVER))
            # send a message to tell the main loop the game is over

            # given a block's location it projects where it will land

    def project_block(self, block):
        temp_block = copy.deepcopy(block)
        while True:
            if temp_block.movedown():
                return temp_block

    def check_collisions(self, x, y):
        return x < 0 or y < 0 or y >= self.get_board_height() or x >= self.get_board_length() or self.board[y][x]

    def draw_block(self, surface, block, outline=False):
        square = pygame.Rect(0, 0, surface.get_width() // self.get_board_length(),
                             surface.get_height() // (self.get_board_height() - 1))
        for x, y in [(x, y) for (x, y) in block.get_spaces() if y > 0]:
            square.x = square.width * x
            square.y = square.width * (y - 1)
            if outline:
                pygame.draw.rect(surface, settings.WHITE, square, 10)
            else:
                pygame.draw.rect(surface, settings.WHITE, square)
        return surface

    # returns a surface with all the blocks drawn on it
    def draw_board(self, res, block=0):

        square = pygame.Rect(0, 0, res[0] // self.get_board_length(),
                             res[1] // (self.get_board_height() - 1))
        surface = pygame.Surface((settings.WIN_WIDTH, settings.WIN_HEIGHT))
        surface.fill(settings.BLACK)

        if block:
            surface = self.draw_block(surface, block)
            surface = self.draw_block(surface, self.project_block(block), True)

        for row in self.board[1:]:
            for block in row:
                if block:
                    pygame.draw.rect(surface, settings.WHITE, square)
                pygame.draw.rect(surface, settings.BLACK, square, 5)
                square.x += square.width
            square.y += square.height
            square.x = 0

        return surface