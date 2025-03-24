# board representation
# bit boarad method
# 64 squares, 64 bits, 8 bytes
# each type of piece has a bitboard ex white pawns.
# to check if a piece is on a square, we can use bitwise operations, like and, or, xor, shift, etc
# this will make ai stuff maybe faster later
# 12 bitboards total, one for each piece


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
