from src.chessMove import ChessMove

class Move:
        def __init__(self, board: 'Board'):
                self.board = board
                self.move = None
                self.piece = None
                self.capturedPiece = None
                self.isCastling = False
                self.isEnPassant = False
                self.isPromotion = False
                
        def MakeMove(self, move: ChessMove) -> bool:
                """
                makes the move
                returns true if move worked
                """
                self.SetMove(move)
                if self.Execute():
                        return True
                return False

        def SetMove(self, move: ChessMove):
                """
                Set the move to be executed
                """
                self.move = move
                self.piece = self.board.bitboard.GetPieceAtSquare(move.fromSquare)

        def IsLegal(self) -> bool:
                """
                Check if move is legal
                """
                if not self.piece or not self.move:
                        return False
                
                legalMoves = self.board.GetPossibleMoves(self.move.fromSquare)
                if not self.move.toSquare in legalMoves:
                        return False
                
                if self.board.currentSide != self.piece.isupper(): # dont move opponents pieces
                        return False

                return True
        
        def Execute(self) -> bool:
                """
                Execute the move on the board
                Returns True if successful
                """
                if not self.IsLegal():
                        return False
                
                self.capturedPiece = self.board.bitboard.GetPieceAtSquare(self.move.toSquare)
                
                self.CheckSpecialMoves()
                
                # handle en passant capture
                if self.isEnPassant:
                        # Calculate the square where the captured pawn is
                        direction = -8 if self.piece.isupper() else 8
                        capturedPawnSquare = self.move.toSquare - direction
                        # remove the captured pawn
                        self.board.bitboard.ClearSquare(capturedPawnSquare)
                        self.capturedPiece = 'p' if self.piece.isupper() else 'P'
                
                self.board.bitboard.MovePiece(self.move.fromSquare, self.move.toSquare)
                
                self.board.moveHistory.AddMove({
                    'piece': self.piece,
                    'fromSquare': self.move.fromSquare,
                    'toSquare': self.move.toSquare,
                    'capture': self.capturedPiece,
                    'castle': 'kingside' if self.isCastling and self.move.toSquare > self.move.fromSquare else 
                             'queenside' if self.isCastling else None,
                    'promotion': self.promotion if self.isPromotion else None,
                    'enPassant': self.isEnPassant,
                    'check': False,  # TODO: Implement check detection
                    'checkmate': False  # TODO: Implement checkmate detection
                })
                
                self.UpdateBoardState()
                return True

        def CheckSpecialMoves(self):
                """
                Check and set flags for special moves 
                castling, en passant, promotion
                """
                piece_type = self.piece.upper()
                
                # Check castling
                if piece_type == 'K':
                        if abs(self.move.toSquare - self.move.fromSquare) == 2:
                                self.isCastling = True
                
                # Check pawn moves
                if piece_type == 'P':
                # Check promotion
                        if self.move.toSquare < 9 or self.move.toSquare > 56:
                                self.isPromotion = True
                
                # Check en passant
                if not self.capturedPiece and abs(self.move.toSquare - self.move.fromSquare) in [7, 9]:
                        self.isEnPassant = True

        def UpdateBoardState(self):
                """
                Update board state after move execution
                """
                # Update castling rights, TODO
                if self.piece.upper() == 'K':
                        if self.piece.isupper():
                                self.board.castlingRights['K'] = False
                                self.board.castlingRights['Q'] = False
                        else:
                                self.board.castlingRights['k'] = False
                                self.board.castlingRights['q'] = False