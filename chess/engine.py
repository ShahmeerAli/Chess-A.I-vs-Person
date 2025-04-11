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
        self.whitekingLocation=(7,4)
        self.blackkingLocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        self.enPassanPossible=()
        self.currentCastleRigths=CastleRights(True,True,True,True)
        self.castleLog=[CastleRights(self.currentCastleRigths.wks,
                                     self.currentCastleRigths.bks,
                                     self.currentCastleRigths.wqs,
                                     self.currentCastleRigths.bqs)]




    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="_"
        self.board[move.endRow][move.endCol]=move.piecemoved
        self.trackmovoes.append(move)
        self.whitetomove=not self.whitetomove #switch turns
        #update kings location
        if move.piecemoved=="wK":
            self.whitekingLocation=(move.endRow,move.endCol)
        elif move.piecemoved=="bK":
            self.blackkingLocation=(move.endRow,move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.piecemoved[0] + 'Q'

       #en passant move
        if move.IsenPassanPossible:
            if self.whitetomove:
                self.board[move.startRow][move.endCol] = "_"  # White captured black pawn
            else:
                self.board[move.startRow][move.endCol] = "_"  # Black captured white pawn

        #update enPassantPossible Variable
        if move.piecemoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassanPossible=((move.startRow+move.endRow)//2,move.endCol)
        else:
            self.enPassanPossible = ()


        #castle moves
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][7]
                self.board[move.endRow][7]="_"
            else:
                self.board[move.endRow][move.endCol+1]=self.board[move.endRow][0]
                self.board[move.endRow][0]="_"

        #update castling rights -rook or a king


        self.updateCastleRights(move)
        self.castleLog.append(CastleRights(self.currentCastleRigths.wks,self.currentCastleRigths.bks,
                                       self.currentCastleRigths.wqs,
                                       self.currentCastleRigths.bqs))



    def undoLastMove(self):
        if len(self.trackmovoes)!=0:
            move=self.trackmovoes.pop()
            self.board[move.startRow][move.startCol]=move.piecemoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whitetomove=not self.whitetomove
            # update kings location
            if move.piecemoved == "wK":
                self.whitekingLocation = (move.startRow, move.startCol)
            elif move.piecemoved == "bK":
                self.blackkingLocation = (move.startRow, move.startCol)

           #undo enpassant move
            if move.IsenPassanPossible:
                self.board[move.endRow][move.endCol]="_"
                self.board[move.startRow][move.endCol]=move.pieceCaptured
                self.enPassanPossible=(move.endRow,move.endCol)
            #undo 2 square pawn advance
            if move.piecemoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassanPossible=()

            #undo the castling rights
            self.castleLog.pop()
            castleRightss=self.castleLog[-1]
            #undo castle move

            if move.isCastleMove:
                if move.endCol == 6:  # Kingside
                    self.board[move.endRow][5] = "_"
                    self.board[move.endRow][7] = "wR" if move.piecemoved == "wK" else "bR"
                elif move.endCol == 2:  # Queenside
                    self.board[move.endRow][3] = "_"
                    self.board[move.endRow][0] = "wR" if move.piecemoved == "wK" else "bR"




    def updateCastleRights(self, move):
        if move.piecemoved == "wK":
            self.currentCastleRigths.wks = False
            self.currentCastleRigths.wqs = False
        elif move.piecemoved == "bK":
            self.currentCastleRigths.bks = False
            self.currentCastleRigths.bqs = False
        elif move.piecemoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastleRigths.wqs = False
                elif move.startCol == 7:
                    self.currentCastleRigths.wks = False
        elif move.piecemoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastleRigths.bqs = False
                elif move.startCol == 7:
                    self.currentCastleRigths.bks = False




    def getValidMoves(self):
      tempEnPossible=self.enPassanPossible
      tempCastleRights=CastleRights(self.currentCastleRigths.wks,
                                    self.currentCastleRigths.bks,
                                    self.currentCastleRigths.wqs,
                                    self.currentCastleRigths.bqs)
      # generating valid moves when the king is
      # checked
      moves=self.possibleMoves()
      if self.whitetomove:
          self.getCastleMoves(self.whitekingLocation[0],self.whitekingLocation[1],moves)
      else:
          self.getCastleMoves(self.blackkingLocation[0],self.blackkingLocation[1],moves)
      for i in range(len(moves)-1,-1,-1):
          self.makeMove(moves[i])
          self.whitetomove= not self.whitetomove
          if self.inCheck():
              moves.remove(moves[i])
          self.whitetomove=not self.whitetomove
          self.undoLastMove()
      if len(moves) == 0:
          if self.inCheck():
              self.checkMate=True
          else:
              self.staleMate=True
      else:
          self.checkMate=False
          self.staleMate=False



      self.enPassanPossible=tempEnPossible
      self.currentCastleRigths=tempCastleRights
      return moves



    def inCheck(self):
        if self.whitetomove:
            return self.squareunderAttack(self.whitekingLocation[0],self.whitekingLocation[1])
        else:
            return self.squareunderAttack(self.blackkingLocation[0],self.blackkingLocation[1])




    def squareunderAttack(self,r,c):
        self.whitetomove = not self.whitetomove
        oppMoves = self.possibleMoves()
        self.whitetomove = not self.whitetomove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False





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
                elif (r-1,c-1) == self.enPassanPossible:
                    moves.append(Moves((r, c), (r - 1, c - 1), self.board,enPassanPossible=True))
            if c+1 <= 7:#right capture
                if self.board[r-1][c+1][0]=="b":
                    moves.append(Moves((r, c), (r - 1, c+1), self.board))
                elif (r - 1, c + 1) == self.enPassanPossible:
                    moves.append(Moves((r, c), (r - 1, c + 1), self.board, enPassanPossible=True))


        else:#black pawn moves
            if self.board[r+1][c]=="_":
                moves.append(Moves((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="_":
                    moves.append(Moves((r,c),(r+2,c),self.board))
            if c - 1 >=0 and self.board[r+1][c-1][0]=="w":
                moves.append(Moves((r, c),(r+1,c-1),self.board))
            elif (r + 1, c - 1) == self.enPassanPossible:
                 moves.append(Moves((r, c), (r + 1, c - 1), self.board, enPassanPossible=True))
            if c+1 <=7 and self.board[r+1][c+1][0] =="w":
                moves.append(Moves((r, c), (r + 1, c + 1), self.board))
            elif (r + 1, c + 1) == self.enPassanPossible:
                moves.append(Moves((r, c), (r + 1, c +1 ), self.board, enPassanPossible=True))






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





    def getCastleMoves(self, r, c, moves):
        if self.squareunderAttack(r,c):
            return
        if (self.whitetomove and self.currentCastleRigths.wks )or (not self.whitetomove and self.currentCastleRigths.bks ) :
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whitetomove and self.currentCastleRigths.wqs )or (not self.whitetomove and self.currentCastleRigths.bqs ) :
            self.getQueensideCastleMoves(r,c,moves)





    def getKingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == "_" and self.board[r][c+2] == "_":
            if not self.squareunderAttack(r,c+1) and not self.squareunderAttack(r,c+2):
                moves.append(Moves((r,c),(r,c+2),self.board,iscastleMove=True))




    def getQueensideCastleMoves(self, r, c, moves):
       if self.board[r][c-1] == "_" and self.board[r][c-2] == "_" and self.board[r][c-3] == "_":
           if not self.squareunderAttack(r, c - 1) and not self.squareunderAttack(r, c - 2):
               moves.append(Moves((r, c), (r, c - 2), self.board, iscastleMove=True))




class CastleRights:
    def __init__(self,wks,bks,wqs,bqs):
       self.bks=bks
       self.wks=wks
       self.wqs=wqs
       self.bqs=bqs









class Moves():
    rankToRows={"1":7,"2":6,"3":5,"4":4,
                "5":3,"6":2,"7":1,"8":0
                }
    rowsToRanks={v:k for k,v in rankToRows.items()}

    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}


    def __init__(self,startSq,endSq,board,enPassanPossible = False,pawnPromotion=False,iscastleMove=False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.piecemoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.piecemoved == "wp" and self.endRow ==0) or (self.piecemoved=="bp" and self.endRow==0):
            self.isPawnPromotion=True
        #en passant
        self.IsenPassanPossible = enPassanPossible
        if len(self.piecemoved) >=2  and self.piecemoved[1] == 'p' and (self.endRow,self.endCol) ==enPassanPossible:

            self.IsenPassanPossible = True

        self.isCastleMove=iscastleMove





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
