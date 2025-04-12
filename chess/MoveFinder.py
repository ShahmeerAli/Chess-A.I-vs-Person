import random
from pkgutil import get_loader

pieceScore={"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE=1000
STALEMATE=0
DEPTH=2

def FindRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

#this function just finds the best moves through iterative methods
# def FindBestMove(gamestate,validMoves):
#     turnMultiplier = 1 if gamestate.whitetomove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestplayermove=None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gamestate.makeMove(playerMove)
#         oppentMoves=gamestate.getValidMoves()
#
#         opponentMaxScore=-CHECKMATE
#         for oppentMove in oppentMoves :
#            gamestate.makeMove(oppentMove)
#            if gamestate.checkMate:
#               score = -turnMultiplier * CHECKMATE
#            elif gamestate.staleMate:
#                score = STALEMATE
#            else:
#                score = -turnMultiplier * scoreMaterial(gamestate.board)
#            if (score > opponentMaxScore):
#                opponentMaxScore = score
#            gamestate.undoLastMove()
#         if opponentMaxScore <opponentMinMaxScore:
#             opponentMinMaxScore=opponentMaxScore
#             bestplayermove=playerMove
#         gamestate.undoLastMove()
#     return bestplayermove


# this function finds best move through recursion
def findBestMove(gamestate,validMoves):
    global nextMove
    nextMove=None
    findAlphaBeta(gamestate,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gamestate.whitetomove else -1)
    return nextMove


#made this function to compare negative min max with ALPHA BETA PRUNING
#ALPHA BETA PRUNNING WINS
# def findNegMinMax(gamestate, validMoves, depth, turnmultiplier):
#     global nextMove
#     print(f"Depth: {depth}, Turn: {'White' if turnmultiplier == 1 else 'Black'}")
#     if depth == 0:
#         score = turnmultiplier * scoreBoard(gamestate)
#         print(f"Returning score at depth 0: {score}")
#         return score
#
#     maxScore = -CHECKMATE
#     for move in validMoves:
#         gamestate.makeMove(move)
#         nextMoves = gamestate.getValidMoves()
#         score = -findNegMinMax(gamestate, nextMoves, depth - 1, -turnmultiplier)
#         gamestate.undoLastMove()
#
#         if score > maxScore:
#             maxScore = score
#             if depth == DEPTH:
#                 nextMove = move
#
#     return maxScore
#





def findAlphaBeta(gamestate, validMoves, depth,alpha,beta, turnmultiplier):
    global nextMove
    print(f"Depth: {depth}, Turn: {'White' if turnmultiplier == 1 else 'Black'}")
    if depth == 0:
        score = turnmultiplier * scoreBoard(gamestate)
        print(f"Returning score at depth 0: {score}")
        return score

    #move ordering -
    maxScore = -CHECKMATE
    for move in validMoves:
        gamestate.makeMove(move)
        nextMoves = gamestate.getValidMoves()
        score = -findAlphaBeta(gamestate, nextMoves, depth - 1,-beta,-alpha, -turnmultiplier)


        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gamestate.undoLastMove()
        if maxScore > alpha:
            alpha=maxScore
        if alpha>=beta:
            break

    return maxScore



def scoreBoard(gamestate):
    if gamestate.checkMate:
        if gamestate.whitetomove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gamestate.staleMate:
        return STALEMATE

    score=0
    for row in gamestate.board:
        for sqaure in row:
            if sqaure[0] == "w":
                score += pieceScore[sqaure[1]]
            elif sqaure[0] == 'b':
                score -= pieceScore[sqaure[1]]
    return score

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