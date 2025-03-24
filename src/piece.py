class Piece:
    def __init__(self, square: int, board: 'Board'):
        self.square = square
        self.board = board

        self.isWhite = False
        piece = board.bitboard.GetPieceAtSquare(square)
        if piece and piece.isupper():
            self.isWhite  = True;
    

    def GetPossibleMoves(self) -> list:
        """
        Base method for getting possible moves
        """
        square = self.square
        board = self.board

        piece = board.bitboard.GetPieceAtSquare(square)
        if not piece:
            return ['no piece found']
        
        pieceMethodMap = {
            'P': Pawn(square, board),
            'N': Knight(square, board),
            'B': Bishop(square, board),
            'R': Rook(square, board),
            'Q': Queen(square, board),
            'K': King(square, board)
        }
        pieceType = pieceMethodMap.get(piece.upper())
        if pieceType:
            return pieceType.GetPossibleMoves()
        
        return ['invalid piece type']



    def GetPossibleTakes(self) -> list:
        """
        Base method for getting possible captures
        """
        square = self.square
        board = self.board

        piece = board.bitboard.GetPieceAtSquare(square)
        if not piece:
            return []

        pieceMethodMap = {
            'P': Pawn(square, board).GetPossibleTakes(), # possible takes funciton for pawn only
            'N': Knight(square, board).GetPossibleMoves(),
            'B': Bishop(square, board).GetPossibleMoves(),
            'R': Rook(square, board).GetPossibleMoves(),
            'Q': Queen(square, board).GetPossibleMoves(),
            'K': King(square, board).GetPossibleMoves()
        }
        pieceType = pieceMethodMap.get(piece.upper())
        if pieceType:
            return pieceType
        
        return []


class Pawn(Piece):
    def GetPossibleMoves(self) -> list:
        square = self.square
        board = self.board

        moves = []
        direction = -8 if self.isWhite else 8  # Up for white, down for black

        target = square + direction
        # 1 square forward
        if not board.bitboard.GetPieceAtSquare(target):
            moves.append(target)
            
            target = square + 2*direction
            # 2 squares on first move
            # hasnt moved check
            if self.isWhite:
                if square in range(49,57): # 49 to 56
                    if not board.bitboard.GetPieceAtSquare(target):
                        moves.append(target)
            else:
                if square in range(9,17): # 9 to 16
                    if not board.bitboard.GetPieceAtSquare(target):
                        moves.append(target)
        
        #diagonal captures
        takes = self.GetPossibleTakes()
        if takes:
            moves.append(takes)
        
        #en passant
        if False == True:
        # if board.movementHistory:
            lastMove = board.movementHistory[-1]
            if lastMove['piece'].upper() == 'P':
                #default row to two rows ahead
                #then check if beside
                #then append lastmove and one direction forward fo the side
                if self.isWhite and lastMove['piece'].isupper() != self.isWhite:
                    if lastMove['from'] in range(9, 17) and lastMove['to'] in range(25, 33): #9-16 to 25-32
                        if square in [lastMove['to'] - 1, lastMove['to'] + 1]:
                            moves.append(lastMove['to'] + direction)
                elif not self.isWhite and lastMove['piece'].isupper() != self.isWhite:
                    if lastMove['from'] in range(49,57) and lastMove['to'] in range(33, 41): #49-56 to 33-40
                        if square in [lastMove['to'] - 1, lastMove['to'] + 1]:
                            moves.append(lastMove['to'] + direction)
                #take logic
        return moves


    # enpassant can only take pawns, do something about it later but not included here
    def GetPossibleTakes(self) -> list:
        square = self.square
        board = self.board

        captures = []
        direction = -8 if self.isWhite else 8  # Up for white, down for black
        # diagonal captures
        column = square%8
        column = 8 if column == 0 else column
        #diagonals cannot go across the sides of the boar
        if column == 8:
            diagonals = [direction - 1] if self.isWhite else [direction + 1]
        elif column == 1:
            diagonals = [direction + 1] if self.isWhite else [direction - 1]
        else:
            diagonals = [direction + 1, direction - 1] # 9 and 7
        
        for diagonal in diagonals:
            target = square + diagonal
            if 1 <= target <= 64:  # Check if target is on board
                piece = board.bitboard.GetPieceAtSquare(target)
                if piece and piece.isupper() != self.isWhite:
                    captures.append(target)
                    #take logic
        return captures
        

class Knight(Piece):
    def GetPossibleMoves(self) -> list:
        square = self.square
        board = self.board

        moves = []
        directions = [
            -17, -15,
            -6, -10,
            17, 15,
            6, 10
        ]
        
        column = square % 8
        if column == 0:
            column = 8
        
        for direction in directions:
            target = square + direction
            if 1 <= target <= 64:
                targetColumn = target % 8
                if targetColumn == 0:
                    targetColumn = 8
                    
                if abs(targetColumn - column) <= 2:
                    piece = board.bitboard.GetPieceAtSquare(target)
                    if not piece or piece.isupper() != self.isWhite:
                        moves.append(target)
                        #take logic
        
        return moves

class Bishop(Piece):
    def GetPossibleMoves(self) -> list:
        square = self.square
        board = self.board
        
        moves = []
        directions = [7,9,-7,-9]

        #current column piece is on
        column = square % 8
        if column == 0:
            column = 8
        oldColumn = column

        # no going off the board onto the other side diagonally
        for direction in directions:
            target = square+direction

            while 1 <= target <= 64:
                # not changing columns by 1 so
                targetColumn = target%8
                if targetColumn == 0:
                    targetColumn == 8
                if abs(targetColumn - oldColumn) > 1:
                    break

                piece = board.bitboard.GetPieceAtSquare(target)
                if not piece:
                    moves.append(target)
                elif piece.isupper() != self.isWhite:
                    moves.append(target)
                    #take take take
                    break #enemy piece can be taken but still blocking further paths
                else:
                    break #friendly piece blocking.

                oldColumn = targetColumn
                target = square+direction
            
        return moves


class Rook(Piece):
    def GetPossibleMoves(self) -> list:
        square = self.square
        board = self.board

        moves = []
        directions = [8, -8, 1, -1]  # up, down, right, left

        column = square%8
        if column == 0:
            column = 8
        oldColumn = column

        for direction in directions:
            target = square+direction

            

            while 1 <= target <= 64:
                targetColumn = target%8
                if targetColumn == 0:
                    targetColumn = 8
                if abs(targetColumn - oldColumn) > 1:
                    break

                piece = board.bitboard.GetPieceAtSquare(target)
                if not piece:
                    moves.append(target)
                elif piece.isupper() != self.isWhite:
                    moves.append(target)
                    #take take take
                    break
                else:
                    break
                oldColumn = targetColumn
                target = square+direction

        return moves

class Queen(Piece):
    def GetPossibleMoves(self) -> list:
        square = self.square
        board = self.board
        
        moves = Bishop(square,board).GetPossibleMoves() + Rook(square,board).GetPossibleMoves()
        return moves


class King(Piece):
    def GetPossibleMoves(self) -> list:
        square = self.square
        board = self.board
        
        moves = []
        directions = [
            -9, -8 ,7,
            -1, 1,
            9, 8, 7
        ]

        
        for direction in directions:
            target = square + direction
            if 1 <= target <= 64:
                piece = board.bitboard.GetPieceAtSquare(target)
                if not piece or piece.isupper() != self.isWhite:
                    if not self.IsInCheck(target, board) and self.MaintainsKingDistance(target, board):
                        moves.append(target)

        # castling
        if not self.IsInCheck(square, board):
            castlingMoves = {
                # side: [rights_key, rook_square, path_squares, king_dest]
                'kingside': {
                    'white': ['K', 64, [62, 63], 62],
                    'black': ['k', 8, [6, 7], 7]
                },
                'queenside': {
                    'white': ['Q', 57, [59, 60], 59],
                    'black': ['q', 1, [3, 4], 3]
                }
            }

            side = 'white' if self.isWhite else 'black'
            for castleSide, data in castlingMoves.items():
                castleData = data[side]
                rights, rookSquare, pathSquares, target = castleData
                
                if board.castlingRights[rights]:
                    pathClear = all(not board.bitboard.GetPieceAtSquare(sq) for sq in pathSquares)
                    pathSafe = all(not self.IsInCheck(sq, board) for sq in pathSquares)
                    
                    if pathClear and pathSafe:
                        moves.append(target)

        return moves

    def IsInCheck(self, square: int, board: 'Board') -> bool:
        for i in range(1, 65):
            piece = board.bitboard.GetPieceAtSquare(i)
            if piece and (piece.isupper() != self.isWhite):
                # Map pieces to their specific classes for take checking
                #removed using initing another piece to check
                pieceMap = {
                    'P': lambda: square in Pawn(i, board).GetPossibleTakes(),
                    'R': lambda: square in Rook(i, board).GetPossibleMoves(),
                    'N': lambda: square in Knight(i, board).GetPossibleMoves(),
                    'B': lambda: square in Bishop(i, board).GetPossibleMoves(),
                    'Q': lambda: square in Queen(i, board).GetPossibleMoves()
                }
                
                checkFunc = pieceMap.get(piece.upper())
                if checkFunc and checkFunc():
                    return True
        return False

    def MaintainsKingDistance(self, square: int, board: 'Board') -> bool:
        for i in range(1,65):
            piece = board.bitboard.GetPieceAtSquare(i)
            if piece and piece.upper() == 'K' and piece.isupper() != self.isWhite:
                cannot = [
                    -9, -8 ,7,
                    -1, 1,
                    9, 8, 7
                ]
                delta = square - i
                if delta in cannot:
                    return False
                return True