from src.bitboard import BitBoard

class Board:
    def __init__(self):
        self.bitboard = BitBoard()
        self.currentSide = True 
        
    
    def currentSideRep(self):
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
                piece = self.bitboard.getPieceAtSquare(square)
                rankStr.append(piece if piece else '.')
            boardStr.append(' '.join(rankStr))
        # reverse the final array to display black at top
        return '\n'.join(boardStr[::-1])