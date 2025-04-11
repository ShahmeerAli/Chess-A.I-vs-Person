import random


def FindRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


def FindBestMove():
    return