import Board
import PlacingPlayer
import MovingPlayer
import numpy


class Player:

    LEARNING_RATE = 0.1
    LAMBDA = 0.7
    SEARCH_DEPTH = 3

    def __init__(self, colour):

        # Initialises list of states for TDLeaf function
        self.states = []

        # Extracts weights from weights.txt file.
        with open("weights.txt", "r+") as weights:
            self.w1 = float(weights.readline()[:-1])
            self.w2 = float(weights.readline()[:-1])
            self.w3 = float(weights.readline()[:-1])
            self.w4 = float(weights.readline()[:-1])
            self.w5 = float(weights.readline()[:-1])

        # Stores weights as list
        self.w = [self.w1, self.w2, self.w3, self.w4, self.w5]

        # Initialise game board
        self.board = Board.Board([], [], 0, 0, self.w1, self.w2, self.w3, self.w4, self.w5)

        # Initialise player colours
        if colour == "white":
            self.colour = "O"
            self.opponent = "@"
        else:
            self.colour = "@"
            self.opponent = "O"

    def action(self, turns):

        # determines whether a placing or moving action should be made
        if turns < 24:
            action = PlacingPlayer.alphabeta_search(self.colour, self.opponent, self.board)

            # Updates internal record of board with move
            self.board = self.board.place(self.colour, action)

        else:
            move = MovingPlayer.alphabeta_search(self.colour, self.opponent, self.board)

            # Updates internal record of board with move
            self.board = self.board.update_board(move)

            # Converts Move object to action representation
            action = (move.start_pos, move.end_pos)

        # Code to use TDLeaf function to adjust weights, used only in training.

        """
        self.tdleaf()

        # Extract updated weights from weights.txt
        with open("weights.txt", "r+") as weights:
            self.w1 = float(weights.readline()[:-1])
            self.w2 = float(weights.readline()[:-1])
            self.w3 = float(weights.readline()[:-1])
            self.w4 = float(weights.readline()[:-1])
            self.w5 = float(weights.readline()[:-1])

        self.w = [self.w1, self.w2, self.w3, self.w4, self.w5]

        self.states.append(self.board)"""

        return action

    def update(self, action):

        # Check for move forfeit
        if not action:
            return
        # Check for movement of a piece
        elif isinstance(action[0], tuple):
            self.board = self.board.update_board(Board.Move(action[0], action[1]))
        # Assume placement of a piece otherwise
        else:
            self.board = self.board.place(self.opponent, action)

    # Function to reduce value to range of -1 to 1
    def r(self, leaf):
        print(numpy.tanh(leaf)) #.utility(self.colour)))
        return numpy.tanh(leaf)  #.utility(self.colour))

    # Function to find next state or leaf
    def leaf(self, state):

        # Determines whether a placing move or a moving move needs be made
        if self.states[state].turns > 24:
            leaf_action = MovingPlayer.alphabeta_search(self.colour, self.opponent, self.states[state], d=self.SEARCH_DEPTH)
            leaf_result = self.states[state].update_board(leaf_action)
        else:
            leaf_action = PlacingPlayer.alphabeta_search(self.colour, self.opponent, self.states[state], d=self.SEARCH_DEPTH)
            leaf_result = self.states[state].place(self.colour, leaf_action)

        return leaf_result

    # TDLeaf function.
    def tdleaf(self):

        # Determines the colour of the player and opponent
        if self.colour == "O":
            us, them = self.board.white, self.board.black
        else:
            us, them = self.board.black, self.board.white

        # Tracks the change in value between states
        d = []
        for i in range(1, len(self.states)):
            d.append(self.r(self.leaf(i).utility(self.colour)) - self.r(self.leaf(i-1).utility(self.colour)))

        # Iterates through weights and updates them according to the TDLeaf function
        for weight in range(5):
            sum1 = 0
            for i in range(1, len(self.states)):
                sum2 = 0
                for m in range(1, len(self.states)):
                    sum2 += pow(self.LAMBDA, m-i) * d[m-1]

                x = self.r(self.leaf(i).utility(self.colour))

                if weight == 0:
                    y = len(us)
                elif weight == 1:
                    y = (self.board.TOTAL_PIECES - len(them))
                elif weight == 2:
                    total_dist = 0
                    for piece in us:
                        total_dist += abs(self.board.centre_x - piece[0]) + abs(self.board.centre_y - piece[1])
                    y = -total_dist/len(us)

                elif weight == 3:
                    y = -sum([abs(piece[0]-other[0]) + abs(piece[1]-other[1]) for piece in us for other in us]) / \
                             (len(us)*len(us))
                else:
                    y = -sum([abs(piece[0] - other[0]) + abs(piece[1] - other[1]) for piece in us for other in them]) / \
                                 (len(us)*len(them))

                gradient = (1 - x * x) * y
                sum1 += sum2 * gradient

            self.w[weight] += self.LEARNING_RATE * sum1

        # Write new rates to file.
        with open("weights.txt", "r+") as weights:
            for a_weight in self.w:
                weights.write(str(a_weight) + "\n")
