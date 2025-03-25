from src.bitboard import BitBoard
from src.piece import Piece
from src.moveHistory import MoveHistory

WHITE = True
BLACK = False

class Board:
    def __init__(self):
        self.bitboard = BitBoard()
        self.currentSide = WHITE 
        self.moveHistory = MoveHistory()
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

    def GetPossibleMoves(self, square: int) -> list:
        """
        Get all possible moves for a piece at given square
        """
        piece = self.bitboard.GetPieceAtSquare(square)
        print(f"Getting moves for {piece} at {square}")  # Debug
        return Piece(square, self).GetPossibleMoves()

    def MovePiece(self, fromSquare: int, toSquare: int) -> bool:
        piece = self.bitboard.GetPieceAtSquare(fromSquare)
        if not piece:
            return False
        
        
        #record move
        self.movement_history[toSquare] = True
        
        #perform move
        

        return True
    
    def MakeMove(self, move: 'ChessMove') -> bool:
        """
        Execute a move on the board
        """
        result = super().MakeMove(move)
        if result:
            print("Move executed successfully")  # Debug
            self.bitboard.PrintBoard()  # Debug
        return result
    
    def exportFEN(self) -> str:
        """
        exports the current state of the board as a FEN string
        note: no game history, only current
        Format: piece_placement/active_color/castling/en_passant/halfmove/fullmove
        """
        # 1. Piece placement (from 8th to 1st rank)
        fen_parts = []
        
        # Process board state
        for rank in range(8):
            empty_squares = 0
            rank_str = ''
            
            for file in range(8):
                square = (rank * 8) + file + 1
                piece = self.bitboard.GetPieceAtSquare(square)
                
                if piece:
                    if empty_squares > 0:
                        rank_str += str(empty_squares)
                        empty_squares = 0
                    rank_str += piece
                else:
                    empty_squares += 1
                    
            if empty_squares > 0:
                rank_str += str(empty_squares)
            fen_parts.append(rank_str)
        
        piece_placement = '/'.join(fen_parts)
        
        # 2. Active color
        active_color = 'w' if self.currentSide else 'b'
        
        # 3. Castling availability
        castling = ''
        if self.castlingRights['K']: castling += 'K'
        if self.castlingRights['Q']: castling += 'Q'
        if self.castlingRights['k']: castling += 'k'
        if self.castlingRights['q']: castling += 'q'
        castling = castling if castling else '-'
        
        # 4. En passant target square
        last_move = self.moveHistory.GetLastMove()
        en_passant = '-'
        if last_move and last_move['piece'].upper() == 'P':
            if abs(last_move['fromSquare'] - last_move['toSquare']) == 16:
                # Convert to algebraic notation (e.g., 'e3')
                file = chr(((last_move['toSquare'] - 1) % 8) + 97)
                rank = '3' if last_move['piece'].isupper() else '6'
                en_passant = file + rank
        
        # 5. Halfmove clock (not implementing 50-move rule yet)
        halfmove = '0'
        
        # 6. Fullmove number
        fullmove = str(self.moveHistory.currentMove)
        
        return f"{piece_placement} {active_color} {castling} {en_passant} {halfmove} {fullmove}"

    def importFEN(self, fen: str) -> bool:
        """
        Import a FEN string and set up the board state
        Returns True if successful
        Format: piece_placement active_color castling en_passant halfmove fullmove
        """
        try:
            parts = fen.split()
            if len(parts) != 6:
                return False
            
            # Clear current board state
            self.bitboard = BitBoard()
            self.bitboard.ClearAllPieces()
            
            # 1. Piece placement
            placement, color, castling, en_passant, halfmove, fullmove = parts
            
            # Process piece placement
            square = 1
            for char in placement:
                if char.isdigit():
                    square += int(char)
                elif char == '/':
                    continue
                else:
                    self.bitboard.SetPieceAtSquare(square, char)
                    square += 1
            
            # 2. Active color
            self.currentSide = (color == 'w')
            
            # 3. Castling rights
            self.castlingRights = {
                'K': 'K' in castling,
                'Q': 'Q' in castling,
                'k': 'k' in castling,
                'q': 'q' in castling
            }
            
            # 4. En passant target (store in move history if needed)
            if en_passant != '-':
                file = ord(en_passant[0]) - ord('a') + 1
                rank = 8 - (int(en_passant[1]))
                square = rank * 8 + file
                # Add a mock last move to enable en passant
                self.moveHistory.AddMove({
                    'piece': 'P' if self.currentSide else 'p',
                    'fromSquare': square + (16 if self.currentSide else -16),
                    'toSquare': square + (8 if self.currentSide else -8),
                    'capture': None,
                    'enPassant': True
                })
            
            # 5. Set move counters
            self.moveHistory.currentMove = int(fullmove)
            
            return True
            
        except Exception as e:
            print(f"Error importing FEN: {e}")
            return False

    def exportPGN(self) -> str:
        """
        exports the board history in PGN format
        """
        return self.moveHistory.ToPGN()