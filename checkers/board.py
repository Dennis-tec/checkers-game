'''<DENNIS YIAILE'''

import pygame
from .constants import*
from checkers.piece import*

# this class creates the board to play the game
class Board:
    def __init__(self):
        self.board = [] # colors of the board
        self.red_left = self.white_left = 12   # number of white and red pieces is 12
        self.red_kings = self.white_kings = 0  # setting kings to be 0 when starting the game
        self.create_board()                    # calling the create method

    # this method draws squares on the board
    def draw_squares(self, win):
        win.fill(BLACK)           # filling the window with black color
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):    # drawing a checker board pattern
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE )) # drawing rectangles on the board

    # this method move pieces from one column or rows to another
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] # swapping pieces in different positions
        piece.move(row, col)    # calling move method in the piece file

        if row ==ROWS or row == 0:
            piece.make_king()        # make piece king if it reaches the opposite end
            if piece.color ==WHITE:
                self.white_kings+=1   # add 1 to the white kings if the piece is white
            else:
                self.red_kings+=1     # add 1 to the red kings if the piece is red

    # this method get a piece at specific position
    def get_piece(self, row, col):
        return self.board[row][col]

    # this method create the positions occupied by red pieces, white, pieces or empty positions
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ( (row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE)) # first 3 rows are occupied by white pieces
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED)) # last 3 rows are occupied by red pieces
                    else:
                        self.board[row].append(0)   # add 0 to empty pieces
                else:
                    self.board[row].append(0)

    # this method draws each piece by calling the draw_squares method
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    # this method removes a piece from a specific positions after being moved
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece !=0: # making sure that the piece move in the right step
                if piece.color ==RED:
                    self.red_left -=1
                else:
                    self.white_left -=1

    # this method determines and returns winner of the game
    def winner(self):
        if self.red_left <=0:
            return "WHITE WON"      # white wins if all red pieces are depleted
        elif self.white_left <=0:
            return "RED WON"        # red wins if all white pieces are depleted
        return None

    # this method ensures that the player is moving in the right direction
    def get_valid_moves(self, piece):
        moves = {}               # store moves as the keys
        left = piece.col-1
        right = piece.col+1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left)) # traverse left
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right)) # traverse right

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left))  # traverse left
            moves.update(self._traverse_right(row+1, min(row+3,ROWS), 1, piece.color, right))  # traverse right

        return moves

    # any time a player presses a piece, they can either move to the right or left

    # this method traverses left of rows and columns recursively if the player selects the left position
    def _traverse_left(self, start, stop, step, color, left, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:    # if next square is empty
                if skipped and not last:     # skipped but no other item to skip onto
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color,left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color,left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left-=1
        return moves

    # this method traverses right of rows and columns recursively if the player selects the right position
    def _traverse_right(self, start, stop, step, color, right, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:  # if next square is empty
                if skipped and not last:  # skipped but no other item to skip onto
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right +1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves