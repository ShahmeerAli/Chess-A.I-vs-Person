import random

pieceScore={"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE=1000
STALEMATE=0

def FindRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


def FindBestMove(gamestate,validMoves):
    turnMultiplier = 1 if gamestate.whitetomove else -1
    opponentMinMaxScore = CHECKMATE
    bestplayermove=None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gamestate.makeMove(playerMove)
        oppentMoves=gamestate.getValidMoves()

        opponentMaxScore=-CHECKMATE
        for oppentMove in oppentMoves :
           gamestate.makeMove(oppentMove)
           if gamestate.checkMate:
              score = -turnMultiplier * CHECKMATE
           elif gamestate.staleMate:
               score = STALEMATE
           else:
               score = -turnMultiplier * scoreMaterial(gamestate.board)
           if (score > opponentMaxScore):
               opponentMaxScore = score
           gamestate.undoLastMove()
        if opponentMaxScore <opponentMinMaxScore:
            opponentMinMaxScore=opponentMaxScore
            bestplayermove=playerMove
        gamestate.undoLastMove()
    return bestplayermove





"""
score based on material
"""

def scoreMaterial(board):
    score=0
    for row in board:
        for sqaure in row:
            if sqaure[0] == "w":
                score+=pieceScore[sqaure[1]]
            elif sqaure[0]=='b':
                score-=pieceScore[sqaure[1]]

    return score