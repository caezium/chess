from src.bitboard import BitBoard
from src.piece import Piece

WHITE = True
BLACK = False

class Board:
    def __init__(self):
        self.bitboard = BitBoard()
        self.currentSide = WHITE 
        self.movementHistory = {}
        # the game state string, to check if a piece has moved or not

        self.castlingRights = { #WILL NOT change if a piece will check during the castling move, in other words, check if move can be intercepted in piece.py, here won't show it, only show if it has moved
            'K': True, #white, kingside
            'Q': True, #queenside
            'k': True, #black
            'q': True
        }

    def GetCurrentSide(self):
        return "White" if self.currentSide else "Black"
    
    def __str__(self):
        """
        Returns string representation of the board
        """
        boardStr = []
        #rank 1 (bottom) to 8 (top)
        for rank in range(1,9):
            rankStr = []
            for file in range(1,9):
                square = (8-rank) * 8 + file
                piece = self.bitboard.GetPieceAtSquare(square)
                rankStr.append(piece if piece else '.')
            boardStr.append(' '.join(rankStr))
        # reverse the final array to display black at top
        return '\n'.join(boardStr[::-1])

    def MovePiece(self, fromSquare: int, toSquare: int) -> bool:
        piece = self.bitboard.GetPieceAtSquare(fromSquare)
        if not piece:
            return False
            
        #check if able to go there
        if toSquare not in Piece.GetPossibleMoves(fromSquare, self):
            return False
        
        #record move
        self.movement_history[toSquare] = True
        
        #perform move
        return True