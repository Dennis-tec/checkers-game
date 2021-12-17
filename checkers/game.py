import pygame

from .constants import*
from checkers.board import*

# this class designs how the game is played
class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    # method update and display rows and columns after valid movements
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # method construct attributes used by other methods in the class
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    # method returns the winner
    def winner(self):
        return self.board.winner()

    # methods reset the game after play and win
    def reset(self):
        self._init()

    # method allows player to select specific and only valid rows and cols positions
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    # method allows play to skipped the opponent pieces while moving if there's an open space ahead of the opponent
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]   # player skipped the opponent
            if skipped:
                self.board.remove(skipped)          # opponent remove after being skipped
            self.change_turn()                      # turns to play given to another player
        else:
            return False

        return True

    # method paint a blue color for any valid positions and moves possible
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE +SQUARE_SIZE//2), 15)

    # method allow players to play in turns. That's, one after the other
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:     # red plays first
            self.turn = WHITE    # white plays next and so on until one wins
        else:
            self.turn = RED
