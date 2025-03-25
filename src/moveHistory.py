class MoveHistory:
    def __init__(self):
        self.moves = []  # list of moves in chronological order
        self.currentMove = 1  # current move number

    def AddMove(self, move_data: dict):
        """
        Add a move to history
        move_data should contain:
            - piece: piece that moved
            - fromSquare: starting square
            - toSquare: ending square
            - capture: captured piece if any
            - check: if move gives check
            - checkmate: if move gives checkmate
            - castle: if move is castling
            - promotion: promotion piece if any
            - enPassant: if move is en passant
        """
        self.moves.append({
            'moveNumber': self.currentMove,
            'side': 'white' if len(self.moves) % 2 == 0 else 'black',
            **move_data
        })
        if len(self.moves) % 2 == 0:
            self.currentMove += 1

    def GetLastMove(self):
        return self.moves[-1] if self.moves else None

    def ToPGN(self) -> str:
        """
        convert to PGN format
        """
        pgn = []
        for move in self.moves:
            if move['side'] == 'white':
                pgn.append(f"{move['moveNumber']}.")
            
            notation = self._moveToAlgebraic(move)
            pgn.append(notation)
            
        return ' '.join(pgn)

    def _moveToAlgebraic(self, move) -> str:
        """
        Convert move data to algebraic notation
        """
        if move.get('castle') == 'kingside':
            return 'O-O'
        if move.get('castle') == 'queenside':
            return 'O-O-O'

        piece = move['piece'].upper()
        notation = ''
        
        # add piece letter for non-pawns
        if piece != 'P':
            notation += piece
            
        # add capture indicator
        if move.get('capture'):
            if piece == 'P':
                notation += self._squareToAlgebraic(move['fromSquare'])[0]
            notation += 'x'
            
        # add destination square
        notation += self._squareToAlgebraic(move['toSquare'])
        
        # add promotion
        if move.get('promotion'):
            notation += f"={move['promotion']}"
            
        # add check/checkmate
        if move.get('checkmate'):
            notation += '#'
        elif move.get('check'):
            notation += '+'
            
        return notation

    def _squareToAlgebraic(self, square: int) -> str:
        file = chr(((square - 1) % 8) + 97)  # 97 is ASCII 'a'
        rank = 8 - ((square - 1) // 8)
        return f"{file}{rank}"
