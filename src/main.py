import sys
import random

from src.board import Board
from src.inputParser import inputParser
from src.move import Move
from src.piece import Piece

#white will be True, black will be False
WHITE = True
BLACK = False
PlayerOne = WHITE
PlayerTwo = BLACK

def chooseSides() -> bool:
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


#TODO add more
def printAvailableCommands() -> None:
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

def makeMove(move: Move, board: Board) -> None:
        """
        makes a move
        """    
        print('Making move : ' + move.notation)
        board.makeMove(move)



def printBoard(board: Board) -> None:
        """
        displays the board
        """
        print()
        print(board)
        print()


def printGameMoves(history: list[tuple[Move, Piece | None]]) -> None:
        """
        prints out the game history of moves in of the current game in PGN format
        """
        counter = 0
        for num, mv in enumerate(history):
                if num % 2 == 0:
                        if counter % 6 == 0:
                                print()
                        print(f'{counter + 1}.', end=' ')
                        counter += 1

                print(mv[0].notation, end=' ')
        print()

#basic AI thing later? AI depth probably can only compute 2
def startGame(board: Board) -> None:
        """
        init and game loop of a two player game
        displays board
        checks win conditions
        shows commands
        processes inputs
        calls moves
        """
        parserWhite = inputParser(board, WHITE)
        parserBlack = inputParser(board, BLACK)
        while True:
                printBoard(board)
                if board.isCheckmate():
                        print('Checkmate')
                        printGameMoves(board.history)
                        return

                if board.isStalemate():
                        print('Stalemate')
                        printGameMoves(board.history)
                        return

                if board.noMatingMaterial():
                        print('Draw due to no mating material')
                        printGameMoves(board.history)
                        return

                # printPointAdvantage(board) calculate advantage (use apis? cannot compute locally easily)
                #update commands
                if board.currentSide == WHITE:
                        parser = parserWhite
                else:
                        parser = parserBlack
                command = input(
                        f"It's your move, {board.currentSideRep()}."
                        + " Type '?' for options. ? ",
                )
                if command.lower() == '?':
                        printAvailableCommands()
                        continue
                elif command.lower() == 'gm':
                        printGameMoves(board.history)
                elif command.lower() == 'exit' or command.lower() == 'quit':
                        return
                
                try:
                        move = parser.parse(command)
                except ValueError as error:
                        print('%s' % error)
                        continue
                makeMove(move, board)

#init board
board = Board()


def main() -> None:
        parser = argparse.ArgumentParser(
                prog='chess',
                description='A python program to play chess '
                'against an AI in the terminal.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                epilog='Enjoy the game!',
        )
        parser.add_argument(
                '-t',
                '--two',
                action='store_true',
                default=False,
                help='to play a 2-player game',
        )
        parser.add_argument(
                '-w',
                '--white',
                action='store',
                default='white',
                metavar='W',
                help='color for white player',
        )
        parser.add_argument(
                '-b',
                '--black',
                action='store',
                default='black',
                metavar='B',
                help='color for black player',
        )
        parser.add_argument(
                '-c',
                '--checkered',
                action='store_true',
                default=False,
                help='use checkered theme for the chess board',
        )

        args = parser.parse_args()
        board.whiteColor = args.white
        board.blackColor = args.black
        board.isCheckered = args.checkered
        try:
                if args.two:
                        twoPlayerGame(board)
                else:
                        playerSide = chooseSides()
                        board.currentSide = WHITE
                        print()
                        aiDepth = askForDepthOfAI()
                        opponentAI = AI(board, not playerSide, aiDepth)
                        printBoard(board)
                        startGame(board, playerSide, opponentAI)
        except KeyboardInterrupt:
                sys.exit()



if __name__=='__main__':
        main()