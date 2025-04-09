"""this is for data storage
  about the current state of the game
  also for determining the valid moves
  keep move log/track
"""
from time import sleep


class Gamestate():
    def __init__(self):
        self.board=[[
            "bR","bN","bB","bQ","bK","bB","bN","bR"
        ],
            [
              "bp","bp","bp","bp","bp","bp","bp","bp"
            ],
            [
                "_","_","_","_","_","_","_","_"
            ],
            [
                "_", "_", "_", "_", "_", "_", "_", "_"
            ],
            [
                "_", "_", "_", "_", "_", "_", "_", "_"
            ],
            [
                "_", "_", "_", "_", "_", "_", "_", "_"
            ],
            [
                "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"
            ],
            [
                "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"
            ],

        ]
        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,"Q":self.getQueenMoves,
                            'K': self.getKingMoves}


        self.whitetomove=True
        self.trackmovoes=[]


    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="_"
        self.board[move.endRow][move.endCol]=move.piecemoved
        self.trackmovoes.append(move)
        self.whitetomove=not self.whitetomove #switch turns


    def undoLastMove(self):
        if len(self.trackmovoes)!=0:
            move=self.trackmovoes.pop()
            self.board[move.startRow][move.startCol]=move.piecemoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whitetomove=not self.whitetomove




    def getValidMoves(self):
      # generating valid moves when the king is
      # checked
        return self.possibleMoves()


#All Moves Without checks
    def possibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=="w" and self.whitetomove) or (turn=="b" and not self.whitetomove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #move function
        return moves


    def getPawnMoves(self ,r,c,moves):
        if self.whitetomove:
            if self.board[r-1][c]=="_": #one square pawn advance
                moves.append(Moves((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="_":
                    moves.append(Moves((r,c),(r-2,c),self.board))
            if c-1>=0:#left capture
                if self.board[r-1][c-1][0]=="b":
                    moves.append(Moves((r, c), (r - 1, c-1), self.board))
            if c+1 <= 7:#right capture
                if self.board[r-1][c+1]=="b":
                    moves.append(Moves((r, c), (r - 1, c+1), self.board))
        else:#black pawn moves
            if self.board[r+1][c]=="_":
                moves.append(Moves((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="_":
                    moves.append(Moves((r,c),(r+2,c),self.board))
            if c - 1 >=0 and self.board[r+1][c-1][0]=="w":
                moves.append(Moves((r, c),(r+1,c-1),self.board))
            if c+1 <=7 and self.board[r+1][c+1][0] =="w":
                moves.append(Moves((r, c), (r + 1, c + 1), self.board))






    def getRookMoves(self, r, c, moves):
        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyCol="b" if self.whitetomove else "w"
        for dir in directions:
            for i in range(1,8):
                endRow=r+dir[0] * i
                endCol=c+dir[1] * i
                if 0<=endRow < 8 and 0<=endCol < 8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="_":
                        moves.append(Moves((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyCol:
                        moves.append(Moves((r,c),(endRow,endCol),self.board))
                        break
                    else:
                     break
                else:
                    break



    def getKnightMoves(self, r, c, moves):
        knightmoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor="w" if self.whitetomove else "b"
        for knight in knightmoves:
            endRow=r + knight[0]
            endCol=c + knight[1]
            if 0<=endRow <8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0] !=allyColor:
                    moves.append(Moves((r,c),(endRow,endCol),self.board))




    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyCol = "b" if self.whitetomove else "w"
        for dir in directions:
            for i in range(1, 8):
                endRow = r + dir[0] * i
                endCol = c + dir[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "_":
                        moves.append(Moves((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyCol:
                        moves.append(Moves((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
      self.getRookMoves(r,c,moves)
      self.getBishopMoves(r,c,moves)



    def getKingMoves(self, r, c, moves):
        kingMoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whitetomove else "b"
        for i in  range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
             endPiece = self.board[endRow][endCol]
             if endPiece[0] != allyColor:
                moves.append(Moves((r, c), (endRow, endCol), self.board))



class Moves():
    rankToRows={"1":7,"2":6,"3":5,"4":4,
                "5":3,"6":2,"7":1,"8":0
                }
    rowsToRanks={v:k for k,v in rankToRows.items()}

    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}


    def __init__(self,startSq,endSq,board):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.piecemoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow * 10 +self.endCol
        print(self.moveID)

    def __eq__(self, other):
        if isinstance(other,Moves):
            return self.moveID==other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)



    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
