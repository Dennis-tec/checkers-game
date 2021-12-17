'''<DENNIS YIAILE'''

import pygame

from .constants import*

# this class designs the size and shapes of the pieces
class Piece:
    PADDING = 10  # padding of a piece
    OUTLINE = 2   # piece outline

    # this method draws matches the color with specific rows and columns during movements
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = True
        self.x = 0        # setting the x value to equal 0
        self.y = 0        # setting the y value to equal 0
        self.calc_pos()   # calculating position of a piece

    # this method calculates the position of a piece in rows and columns
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE //2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # this method creates the piece that can pass over the opponent backward as king
    def make_king(self):
        self.king = True

    # this method draws the piece as circles with a grey outline
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius+self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    # this method takes in rows to enhance movement of pieces throughout the board
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    # method returns a string representation of the game pieces as color
    def __repr__(self): # representation
        return str(self.color)
