'''<DENNIS YIAILE'''

# importing the required files for this project
import pygame
from checkers.constants import*
from checkers.game import*
from checkers.board import*

FPS = 60    # creating a constant timer for opening and running the project for all devices

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # window display set up
pygame.display.set_caption('Dennis-Checkers ') # proect title

# this method gets the columns and rows while moving pieces across the board with a mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col
# this method ensures that the entire project works to get the winner
def main():
    run = True
    clock = pygame.time.Clock()  # setting up the time clock to run the game
    game = Game(WIN)             # calling the game method

    while run:
        clock.tick(FPS)          # method ensures that the game runs at a constant time for all devices

        if game.winner() !=None:
            print(game.winner()) # printing the match winner if one is identified

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False        # this code stops the game from running if a player quite
            if event.type == pygame.MOUSEBUTTONDOWN: # this code moves the players pieces to respective positions depending on
                pos = pygame.mouse.get_pos()        # the position that has been pressed
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()       # update the location of a piece after a movement
    pygame.quit()           # quit game if completed

main()

if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
