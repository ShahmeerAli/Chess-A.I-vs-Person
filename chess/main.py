"""This class is for the driver main class. It will be responsible
for handling our user input and displaying the current game state."""

import pygame as p
# Remove this import unless you're using it; pygame.examples is not standard for production
# from pygame.examples.go_over_there import screen, clock

from chess import engine

# Global Constants
width = height = 512
dimensions = 8
square_size = height // dimensions
max_fps = 15
Images = {}

"""
Initializing images exactly once to load later
"""
def LoadImages():
    pieces = ["wp", "wR", "wB", "wN", "wQ", "wK",
              "bp", "bR", "bB", "bN", "bQ", "bK"]
    for piece in pieces:
        Images[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (square_size, square_size)
        )

"""
Main function to handle user input
"""
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gamestate = engine.Gamestate()
    validMoves=gamestate.getValidMoves()
    moveMade=False

    LoadImages()
    running = True
    sqSelcted=()
    playerclicks=[]


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//square_size
                row=location[1]//square_size
                if sqSelcted==(row,col):
                    sqSelcted=()
                    playerclicks=[]
                else:
                    sqSelcted=(row,col)
                    playerclicks.append(sqSelcted)
                if len(playerclicks)==2:
                   move=engine.Moves(playerclicks[0],playerclicks[1],gamestate.board)

                   print(move.getChessNotation())
                   for i in range(len(validMoves)):
                     if move ==validMoves[i]:
                      gamestate.makeMove(validMoves[i])
                      moveMade=True
                      sqSelcted=()
                      playerclicks = []
                   if not moveMade:
                       playerclicks=[sqSelcted ]
            elif    e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gamestate.undoLastMove()
                    moveMade=True


        if moveMade:
           validMoves=gamestate.getValidMoves()
           moveMade=False

        drawGameState(screen, gamestate)
        clock.tick(max_fps)
        p.display.flip()

"""
Responsible for all graphics
"""
def drawGameState(screen, gamestate):
    drawBoardSquares(screen)
    drawPieces(screen, gamestate.board)

def drawBoardSquares(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * square_size, r * square_size, square_size, square_size))


def drawPieces(screen, board):
   for row in range(dimensions):
       for c in range(dimensions):
           piece=board[row][c]
           if piece!="_":
               screen.blit(Images[piece],p.Rect(c*square_size,row*square_size,square_size,square_size))





if __name__ == "__main__":
    main()
