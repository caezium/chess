import sys
import random
import re # regex

from src.board import Board
# from src.inputParser import inputParser
# from src.move import Move
# from src.piece import Piece

WHITE = True
BLACK = False
playerOne = WHITE
playerTwo = BLACK
turn = WHITE



def ChooseSides() -> bool:
        """
        Asks for which side the players would like to be on.
        We will only ask player 1, then assign the other role to player two
        white will be true and black will be false
        Returns a bool.
        """
        choice = input("Which side does PLAYER ONE want to be on? [w or b]")
        if 'w' in choice:
                print("PLAYER ONE will play as WHITE \n  PLAYER TWO will play as BLACK")
                return WHITE
        else:
                print(" PLAYER TWO will play as WHITE \n PLAYER ONE will play as BLACK")
                return BLACK


def PrintAvailableCommands() -> None:
        """
        prints all the available commands that the user can use
        """
        printGameMoves = 'gm: moves of current game in PGN (portable game notation) format'
        quitOption = 'quit : resign'
        moveOption = 'a3, Nc3, Qxa2, etc : make the move'
        options = [
                printGameMoves,
                quitOption,
                moveOption,
                '',
        ]
        print('\n'.join(options))

def MakeMove() -> None:
        """
        makes a move
        """    
        



def PrintBoard(board : Board) -> None:
        """
        displays the board
        """
        print()
        print(board)
        print()


# def ParseInput(input: str) -> Move:
#         """
#         parses input
#         """
#         regexCoordinateNotation = re.compile('(?i)[a-h][1-8][a-h][1-8][QRBN]?') #QRBN promotion not required
#         if regexCoordinateNotation.match(input):
#                 pieceX = input[0]
#                 pieceY = input[1]
#                 toX = input[2]
#                 toY = input[3]
#                 return input
        
#         raise ValueError('Invalid move: %s' % input)

def StartGame(board : Board) -> None:
        """
        init and game loop of a two player game
        displays board
        checks win conditions
        shows commands
        processes inputs
        calls moves
        """
        playerOne = ChooseSides()
        playerTwo = not playerOne
        

        while True:
                PrintBoard(board)
                # if board.isCheckmate():
                #         print('Checkmate')
                #         return

                # if board.isStalemate():
                #         print('Stalemate')
                #         return

                # if board.noMatingMaterial():
                #         print('Draw')
                #         return

                # printPointAdvantage(board) calculate advantage (use apis? cannot compute locally easily)
                #update commands
                # if board.currentSide == WHITE:
                #         parser = parserWhite
                # else:
                #         parser = parserBlack
                if turn == playerOne:
                        command = input(
                                f"It's PLAYER ONE's move."
                                + " Type '?' for options. ? ",
                        )
                else:
                        command = input(
                                f"It's PLAYER TWO's move."
                                + " Type '?' for options. ? ",
                        )
                
                if command.lower() == '?':
                        PrintAvailableCommands()
                        continue
                elif command.lower() == 'exit' or command.lower() == 'quit':
                        return
                
                # try:
                #         move = parser.parse(command)
                # except ValueError as error:
                #         print('%s' % error)
                #         continue

                # MakeMove(move, board)

#init board
board = Board()


def main() -> None:
        try:
                StartGame(board)
        except KeyboardInterrupt:
                sys.exit()



if __name__=='__main__':
        main()