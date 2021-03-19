import sys
import Massacre
import Player
import Board


def moves(board):

    # sum white's moves
    sum = 0

    # check every square on board to find each white piece
    for i in range(8):

        for j in range(8):

            if board[i][j] == "O":

                # look each side of each white piece to find ways it could move
                # after checking to avoid moving out-of-bounds
                if i > 0:
                    if board[i-1][j] == "-":
                        sum += 1
                    elif board[i-1][j] == "O" or board[i-1][j] == "@":
                        if i>1 and board[i-2][j] == "-":
                            sum += 1
                if i < 7:
                    if board[i+1][j] == "-":
                        sum += 1
                    elif board[i+1][j] == "O" or board[i+1][j] == "@":
                        if i < 6 and board[i+2][j] == "-":
                            sum += 1
                if j > 0:
                    if board[i][j-1] == "-":
                        sum += 1
                    elif board[i][j-1] == "O" or board[i][j-1] == "@":
                        if j > 1 and board[i][j-2] == "-":
                            sum += 1
                if j < 7:
                    if board[i][j+1] == "-":
                        sum += 1
                    elif board[i][j+1] == "O" or board[i][j+1] == "@":
                        if j < 6 and board[i][j+2] == "-":
                            sum += 1
    print(sum)

    # sum black's moves, as above
    sum = 0

    for i in range(8):

        for j in range(8):

            if board[i][j] == "@":
                if i > 0:
                    if board[i-1][j] == "-":
                        sum += 1
                    elif board[i-1][j] == "O" or board[i-1][j] == "@":
                        if i > 1 and board[i-2][j] == "-":
                            sum += 1
                if i < 7:
                    if board[i+1][j] == "-":
                        sum += 1
                    elif board[i+1][j] == "O" or board[i+1][j] == "@":
                        if i < 6 and board[i+2][j] == "-":
                            sum += 1
                if j > 0:
                    if board[i][j-1] == "-":
                        sum += 1
                    elif board[i][j-1] == "O" or board[i][j-1] == "@":
                        if j > 1 and board[i][j-2] == "-":
                            sum += 1
                if j < 7:
                    if board[i][j+1] == "-":
                        sum += 1
                    elif board[i][j+1] == "O" or board[i][j+1] == "@":
                        if j < 6 and board[i][j+2] == "-":
                            sum += 1
    print(sum)
    return


def main():

    # initialise state
    state = [[0 for j in range(8)] for i in range(8)]

    # read input; done this way to make the board notation for the game
    # match up with the board notation in the program
    squares = sys.stdin.read()

    y = 0
    x = 0
    for char in squares:
        if char == " ":
            x += 1
        elif char == "\n":
            y += 1
            x -= 7
            if y > 7:
                break
        else:
            state[y][x] = char

    # extract mode indicator
    mode = squares[128:].strip("\n")

    white, black = Board.Board.produce_piece_list(state)

    # execute analysis
    if mode == "Moves":
        moves(state)
    elif mode == "Massacre":
        # extract move list that solves board configuration
        solution = Player.ArtificialPlayer(Board.Board(white, black)).calculate_strategy()

        # iterate through moves and print
        for i in solution:
            if i:
                print(i)


if __name__ == "__main__":
    main()
