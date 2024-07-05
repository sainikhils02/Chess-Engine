class GameState():
    def __init__(self):
        self.board=[
            #board is 8x8, each elemnt is two characters: colour and name of piece
            #blank space is "--"
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove=True
        self.moveLog=[]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = True
        self.enpassantPossible = ()
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        #Update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow-move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible=()

        if move.isCastleMove:
            if move.endCol-move.startCol==2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    def undoMove(self):
        if len(self.moveLog)!=0:
            move = self.moveLog.pop()
            #print(move.getChessNotation()[2:]+move.getChessNotation()[:2])
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] =  '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1] == 'p' and abs(move.startRow-move.endRow) == 2:
                self.enpassantPossible = ()
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs , newRights.bqs )
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False


    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCatleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        moves = self.getAllMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if(len(moves)==0):
            if(self.inCheck()):
                self.checkMate = True
            else:
                self.staleMate = True
        else:   
            self.checkMate = False
            self.staleMate = False
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCatleRights
        return moves
    

    def inCheck(self):
        if self.whiteToMove and self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1]):
            return True
        elif not self.whiteToMove and self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1]):
            return True
        return False


    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        oppositemoves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppositemoves:
            if(move.endRow == row and move.endCol == col):
                return True
        return False
    

    def getAllMoves(self):
        #moves = [Move((6, 4), (4, 4), self.board)]
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves


    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove:
            if self.board[row-1][col] == '--':
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '--':
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
                elif(row-1, col-1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row-1, col-1), self.board, isEnpassantMove=True))
            if col+1 < len(self.board[0]):
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
                elif(row-1, col+1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row-1, col+1), self.board, isEnpassantMove=True))
        else:#black moves
            if self.board[row+1][col] == '--':
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == '--':
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
                elif (row+1, col-1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row+1, col-1), self.board, isEnpassantMove = True))
            if col+1 < len(self.board[0]):
                if self.board[row+1][col+1][0] == 'w    ':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
                elif(row+1, col+1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row+1, col+1), self.board, isEnpassantMove=True))
        

    def getRookMoves(self, row, col, moves):
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        startcolor = self.board[row][col][0]
        for direc in directions:
            for i in range(1, len(self.board[0])):
                erow = row + direc[0]*i
                ecol = col + direc[1]*i
                if erow >=0 and erow < len(self.board[0]) and ecol >= 0 and ecol < len(self.board[0]):
                    endcolor = self.board[erow][ecol][0]
                    if self.board[erow][ecol]=='--':
                        moves.append(Move((row, col), (erow, ecol), self.board))
                    elif startcolor!=endcolor:
                        moves.append(Move((row, col), (erow, ecol), self.board))
                        break
                    else:
                        break
                else: 
                    break
         

    def getKnightMoves(self, row, col, moves):
        directions = ((1, 2), (2, 1), (-1, -2), (1, -2), (-1, 2), (2, -1), (-2, -1), (-2, 1))
        startcolor = self.board[row][col][0]
        for direc in directions:
            erow = row + direc[0]
            ecol = col + direc[1]
            if erow >=0 and erow < len(self.board[0]) and ecol >= 0 and ecol < len(self.board[0]):
                endcolor = self.board[erow][ecol][0]
                if self.board[erow][ecol]=='--':
                    moves.append(Move((row, col), (erow, ecol), self.board))
                elif startcolor!=endcolor:
                    moves.append(Move((row, col), (erow, ecol), self.board))

    def getBishopMoves(self, row, col, moves):
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        startcolor = self.board[row][col][0]
        for direc in directions:
            for i in range(1, len(self.board[0])):
                erow = row + direc[0]*i
                ecol = col + direc[1]*i
                if erow >=0 and erow < len(self.board[0]) and ecol >= 0 and ecol < len(self.board[0]):
                    endcolor = self.board[erow][ecol][0]
                    if self.board[erow][ecol]=='--':
                        moves.append(Move((row, col), (erow, ecol), self.board))
                    elif startcolor!=endcolor:
                        moves.append(Move((row, col), (erow, ecol), self.board))
                        break
                    else:
                        break
                else: 
                    break  

    def getQueenMoves(self, row, col, moves):
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))
        startcolor = self.board[row][col][0]
        for direc in directions:
            for i in range(1, len(self.board[0])):
                erow = row + direc[0]*i
                ecol = col + direc[1]*i
                if erow >=0 and erow < len(self.board[0]) and ecol >= 0 and ecol < len(self.board[0]):
                    endcolor = self.board[erow][ecol][0]
                    if self.board[erow][ecol]=='--':
                        moves.append(Move((row, col), (erow, ecol), self.board))
                    elif startcolor!=endcolor:
                        moves.append(Move((row, col), (erow, ecol), self.board))
                        break
                    else:
                        break
                else: 
                    break  

    def getKingMoves(self, row, col, moves):
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))
        startcolor = self.board[row][col][0]
        for direc in directions:
            erow = row + direc[0]
            ecol = col + direc[1]
            if erow >=0 and erow < len(self.board[0]) and ecol >= 0 and ecol < len(self.board[0]):
                endcolor = self.board[erow][ecol][0]
                if self.board[erow][ecol]=='--':
                    moves.append(Move((row, col), (erow, ecol), self.board))
                elif startcolor!=endcolor:
                    moves.append(Move((row, col), (erow, ecol), self.board))
        #self.getCastleMoves(row, col, moves, startcolor)


    def getCastleMoves(self, row, col, moves):
        if self.squareUnderAttack(row, col):
            return 
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(row, col, moves)


    def getKingsideCastleMoves(self, row, col, moves):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.squareUnderAttack(row, col+1) and not self.squareUnderAttack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, isCastleMove=True))



    def getQueensideCastleMoves(self, row, col, moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] == '--':
            if not self.squareUnderAttack(row, col-1) and not self.squareUnderAttack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, isCastleMove=True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    #rowsToRanks = {"7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 5, "1": 7, "0": 8}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    #colsToFiles = {"0": 'a', "1": 'b', "2": 'c', "3": 'd', "4": 'e', "5": 'f', "6": 'g', "7": 'h'}
    def __init__(self, startsq, endsq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        # if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
        #     self.isPawnPromotion = True
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp' 
        # if self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == enpassantPossible:
        #     self.isEnpassantMove = True
        self.isCastleMove = isCastleMove
        self.moveId = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        #print(self.moveId)

    def __eq__(self, other):
        if(isinstance(other, Move)):
            return self.moveId == other.moveId
        return False

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol)+self.getRankFile(self.endRow, self.endCol)  
