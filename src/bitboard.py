# board representation
# bit boarad method
# 64 squares, 64 bits, 8 bytes
# each type of piece has a bitboard ex white pawns.
# to check if a piece is on a square, we can use bitwise operations, like and, or, xor, shift, etc
# this will make ai stuff maybe faster later
# 12 bitboards total, one for each piece
# TODO more bitboard funcs


class BitBoard:
    def __init__(self):
        """
        we will be referring to stuff from the top left to bottom right, black on top, white on bottom
        """
        self.white_pawns   = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1111_1111_0000_0000     # Rank 2
        self.white_knights = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0100_0010     # b1, g1
        self.white_bishops = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0010_0100     # c1, f1
        self.white_rooks   = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1000_0001     # a1, h1
        self.white_queens  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_0000     # d1
        self.white_king    = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1000     # e1
        
        self.black_pawns   = 0b0000_0000_1111_1111_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000     # Rank 7
        self.black_knights = 0b0100_0010_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000     # b8, g8
        self.black_bishops = 0b0010_0100_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000     # c8, f8
        self.black_rooks   = 0b1000_0001_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000     # a8, h8
        self.black_queens  = 0b0001_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000     # d8
        self.black_king    = 0b0000_1000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000     # e8

    #todo make this into redudant 8x8 board
    def GetPieceAtSquare(self, square):
        """
        Returns the piece at the given square (0-63)
        & - bitwise AND operation, returns non-zero if both bits are 1
        1 << square - shifts 1 to the left by square bits, ex 1 << 3 = 0b0000_0000_0000_0000_0000_0000_0000_1000
        square should be between 1 and 64
        """
        where = 64-square
        mask = 1 << where
        if self.white_pawns & mask: return 'P'
        if self.white_knights & mask: return 'N'
        if self.white_bishops & mask: return 'B'
        if self.white_rooks & mask: return 'R'
        if self.white_queens & mask: return 'Q'
        if self.white_king & mask: return 'K'

        if self.black_pawns & mask: return 'p'
        if self.black_knights & mask: return 'n'
        if self.black_bishops & mask: return 'b'
        if self.black_rooks & mask: return 'r'
        if self.black_queens & mask: return 'q'
        if self.black_king & mask: return 'k'
        return None

    #todo make this better, its fast tho
    def squareToCoords(self, square) -> tuple:
        """
        Convert 1-64 square to rank, file -> tuple
        """
        rank = square // 8
        file = square % 8
        return (rank, file)

    def coordsToSquare(self, rank, file) -> int:
        """
        Convert rank, file to 1-64 square -> int
        """
        return rank * 8 + file

    def getMask(self, square):
        """
        get bitmask for a square
        """
        if not 1 <= square <= 64:
            raise ValueError("Square number is not between 1 and 64")
        return 1 << square


    def MovePiece(self, fromSquare: int, toSquare: int):
        piece = self.GetPieceAtSquare(fromSquare)
        print(f"Moving {piece} from {fromSquare} to {toSquare}")  # debug
        
        self.ClearSquare(fromSquare) # TODO enpassant edge case
        self.SetPieceAtSquare(toSquare, piece)
        
        
        print(f"After move: {piece} at {toSquare}: {self.GetPieceAtSquare(toSquare)}")
        self.PrintBoard()  # for debug, but keep cuz yes
        
    def ClearSquare(self, square: int):
        """
        Clear any piece from the given square
        """
        where = 64-square
        mask = ~(1 << where)  # Invert the mask to clear the bit
        
        # Clear the bit on all piece bitboards
        self.white_pawns &= mask
        self.white_knights &= mask
        self.white_bishops &= mask
        self.white_rooks &= mask
        self.white_queens &= mask
        self.white_king &= mask
        
        self.black_pawns &= mask
        self.black_knights &= mask
        self.black_bishops &= mask
        self.black_rooks &= mask
        self.black_queens &= mask
        self.black_king &= mask

    def SetPieceAtSquare(self, square: int, piece: str):
        """
        Set a piece at the given square
        piece is a character: 'P','N','B','R','Q','K' for white
                            'p','n','b','r','q','k' for black
        """
        if not piece:
            return
            
        where = 64-square
        mask = 1 << where
        
        # set the bit on the appropriate bitboard
        if piece == 'P': self.white_pawns |= mask
        elif piece == 'N': self.white_knights |= mask
        elif piece == 'B': self.white_bishops |= mask
        elif piece == 'R': self.white_rooks |= mask
        elif piece == 'Q': self.white_queens |= mask
        elif piece == 'K': self.white_king |= mask
        elif piece == 'p': self.black_pawns |= mask
        elif piece == 'n': self.black_knights |= mask
        elif piece == 'b': self.black_bishops |= mask
        elif piece == 'r': self.black_rooks |= mask
        elif piece == 'q': self.black_queens |= mask
        elif piece == 'k': self.black_king |= mask

    def ClearAllPieces(self):
        self.white_pawns = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks = 0
        self.white_queens = 0
        self.white_king = 0
        self.black_pawns = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks = 0
        self.black_queens = 0
        self.black_king = 0

    def PrintBoard(self):
        """
        Prints the current board state in a readable format
        Separate from the printboard in board.py
        """
        print("\n  a b c d e f g h")
        print("  ---------------")
        for rank in range(8):
            print(f"{8-rank}|", end=" ")
            for file in range(8):
                square = (rank * 8) + file + 1
                piece = self.GetPieceAtSquare(square)
                print(f"{piece if piece else '.'}", end=" ")
            print(f"|{8-rank}")
        print("  ---------------")
        print("  a b c d e f g h\n")