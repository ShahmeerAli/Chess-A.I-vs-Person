"""This class is for the driver main class. It will be responsible
for handling our user input and displaying the current game state."""

import pygame as p
# Remove this import unless you're using it; pygame.examples is not standard for production
# from pygame.examples.go_over_there import screen, clock

from chess import engine
from chess import MoveFinder

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

    gameFinished=False
    playerOne=True #if made false both players work as AI
    playerTwo=False
    while running:
        humanTurn=(gamestate.whitetomove and playerOne) or (not gamestate.whitetomove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type==p.MOUSEBUTTONDOWN:
              if not gameFinished and humanTurn:
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
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gamestate.undoLastMove()
                    moveMade=True
                if e.key==p.K_r:
                    gamestate=engine.Gamestate()
                    validMoves=gamestate.getValidMoves()
                    sqSelcted=()
                    playerclicks=[]
                    moveMade=False


        #A.I MOVE FINDER
        if not gameFinished and not humanTurn:
            AIMove=MoveFinder.FindBestMove(gamestate, validMoves)
            if AIMove is None:
               AIMove=MoveFinder.FindRandomMove(validMoves)
            gamestate.makeMove(AIMove)
            moveMade=True



        if moveMade:
           validMoves=gamestate.getValidMoves()
           moveMade=False

        drawGameState(screen, gamestate,validMoves,sqSelcted)
        if gamestate.checkMate:
            gameFinished=True
            if gamestate.whitetomove:
                drawText(screen,"Black Wins")
            else:
                drawText(screen,"White Wins")
        elif gamestate.staleMate:
            gameFinished=True
            drawText(screen,"Stale Mate")


        clock.tick(max_fps)
        p.display.flip()

"""
Responsible for all graphics
"""
def drawGameState(screen, gamestate,validMoves,sqSelected):
    drawBoardSquares(screen)
    highlightsquares(screen,gamestate,validMoves,sqSelected)
    drawPieces(screen, gamestate.board)



def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, True, p.Color("Red"))
    textLocation = p.Rect(0, 0, width, height).move(
        width // 2 - textObject.get_width() // 2,
        height // 2 - textObject.get_height() // 2
    )
    screen.blit(textObject, textLocation)




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



"""
Highligthing the squares
"""
def highlightsquares(screen,gamestate,validMoves,sqSelected):
    if sqSelected!=():
        r, c = sqSelected
        if gamestate.board[r][c][0]==('w' if gamestate.whitetomove else 'b'):
               surface=p.Surface((square_size, square_size))
               surface.set_alpha(120)
               surface.fill('green')
               screen.blit(surface,(c * square_size, r * square_size))
               surface.fill('violet')
               for move in validMoves:
                   if move.startRow==r and move.startCol == c:
                       screen.blit(surface,(move.endCol*square_size, move.endRow*square_size))






if __name__ == "__main__":
    #calling main
    main()
