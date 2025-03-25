class ChessMove:
    def __init__(self, fromSquare: int, toSquare: int):
        self.fromSquare = fromSquare
        self.toSquare = toSquare
    
    def __str__(self):
        """
        returns move as a string
        change later?
        """
        files = 'abcdefgh'
        ranks = '87654321'
        
        fromFile = files[(self.fromSquare - 1) % 8]
        fromRank = ranks[(self.fromSquare - 1) // 8]
        toFile = files[(self.toSquare - 1) % 8]
        toRank = ranks[(self.toSquare - 1) // 8]
        
        return f"{fromFile}{fromRank}{toFile}{toRank}"