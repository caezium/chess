from src.chessMove import ChessMove

WHITE = True
BLACK = False

class InputParser:
    def __init__(self, board: 'Board'):
        self.board = board
        self.fileMap = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.rankMap = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}
        self.pieceMap = {'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N'}

    def ParseInput(self, move_str: str) -> tuple:
        """
        Parse both coordinate notation (e2e4) and algebraic notation (Nf3)
        returns chessmove object
        """
        move_str = move_str.strip()
        
        # try coordinate notation first (e.g., e2e4)
        if len(move_str) == 4 and move_str[0].isalpha() and move_str[2].isalpha():
            return self._ParseCoordinateNotation(move_str)
            
        # TODO: try algebraic notation (e.g., Nf3, e4, O-O)
        # this does not work
        return self._ParseAlgebraicNotation(move_str)

    def _ParseCoordinateNotation(self, move_str: str) -> tuple:
        """
        Parse coordinate notation (e.g., e2e4)
        """
        try:
            from_file = self.fileMap[move_str[0].lower()]
            from_rank = int(move_str[1])
            to_file = self.fileMap[move_str[2].lower()]
            to_rank = int(move_str[3])
            
            from_square = (8 - from_rank) * 8 + from_file
            to_square = (8 - to_rank) * 8 + to_file
            
            return ChessMove(from_square, to_square)
        except (KeyError, ValueError):
            return None

    def _ParseAlgebraicNotation(self, move_str: str) -> tuple:
        """
        Parse algebraic notation (e.g., Nf3, e4, O-O)
        """
        # castling
        if move_str in ['O-O', '0-0']:  # Kingside
            return self._GetCastlingMove(True)
        elif move_str in ['O-O-O', '0-0-0']:  # Queenside
            return self._GetCastlingMove(False)

        try:
            # Regular moves
            piece = 'P'  # Default to pawn
            disambiguation = ''
            capture = False
            destination = ''
            promotion = ''
            
            # Remove check/mate symbols
            move_str = move_str.replace('+', '').replace('#', '')
            
            # promotion
            if '=' in move_str:
                move_str, promotion = move_str.split('=')
            
            # captures
            if 'x' in move_str:
                move_str = move_str.replace('x', '')
                capture = True
                
            # Get piece type
            if move_str[0].upper() in self.pieceMap:
                piece = move_str[0].upper()
                move_str = move_str[1:]
                
            # Get destination square
            destination = move_str[-2:]
            move_str = move_str[:-2]
            
            # Any remaining characters are disambiguation
            disambiguation = move_str
            
            # Find matching piece that can make this move
            possible_sources = self._FindPossibleSources(piece, destination, disambiguation, capture)
            if len(possible_sources) == 1:
                from_square = possible_sources[0]
                to_square = self._AlgebraicToSquare(destination)
                return ChessMove(from_square, to_square)
                
        except (KeyError, ValueError, IndexError):
            return None
            
        return None

    def _GetCastlingMove(self, kingside: bool) -> tuple:
        """
        Get castling move squares based on side and color
        """
        rank = 1 if self.board.currentSide == WHITE else 8
        king_file = 'e'
        rook_file = 'h' if kingside else 'a'
        king_dest = 'g' if kingside else 'c'
        
        from_square = self._AlgebraicToSquare(f"{king_file}{rank}")
        to_square = self._AlgebraicToSquare(f"{king_dest}{rank}")
        
        return (from_square, to_square)

    def _FindPossibleSources(self, piece: str, destination: str, disambiguation: str, capture: bool) -> list:
        """
        Find all pieces that could make the specified move
        """
        possible_sources = []
        dest_square = self._AlgebraicToSquare(destination)
        
        for square in range(1, 65):
            piece_at_square = self.board.bitboard.GetPieceAtSquare(square)
            if not piece_at_square or piece_at_square.upper() != piece:
                continue
                
            # Check if piece color matches turn
            is_white_piece = piece_at_square.isupper()
            if is_white_piece != self.board.currentSide == WHITE:
                continue
            
            # Check if piece can move to destination
            valid_moves = self.board.GetPossibleMoves(square)
            if dest_square not in valid_moves:
                continue
                
            # Check disambiguation
            if disambiguation:
                algebraic_source = self._SquareToAlgebraic(square)
                if disambiguation in algebraic_source:
                    possible_sources.append(square)
            else:
                possible_sources.append(square)
                
        return possible_sources

    def _AlgebraicToSquare(self, algebraic: str) -> int:
        """
        Convert algebraic notation (e4) to square number
        """
        file = self.fileMap[algebraic[0].lower()]
        rank = int(algebraic[1])
        return (8 - rank) * 8 + file

    def _SquareToAlgebraic(self, square: int) -> str:
        """
        Convert square number to algebraic notation
        """
        rank = 8 - ((square - 1) // 8)
        file = ((square - 1) % 8) + 1
        file_letter = list(self.fileMap.keys())[list(self.fileMap.values()).index(file)]
        return f"{file_letter}{rank}"
