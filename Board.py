import random


class Board:

    # Constant for total pieces allowed on board
    TOTAL_PIECES = 12

    # Constants for centre of board coordinates (though not actually accessible coordinates)
    centre_x = 3.5
    centre_y = 3.5

    def __init__(self, white, black, turns, shrunk, our_weight, opponent_weight,
                 centrality_weight, bunching_weight, proximity_weight):

        # In itialise board's list of pieces
        self.white = list(white)
        self.black = list(black)

        # Initialise the ;point of the game the board is at
        self.shrunk = shrunk
        self.turns = turns

        # Initialise the size of the board
        self.upper_edge = 7

        # Initialise the heuristic parameters
        self.our_weight = our_weight
        self.opponent_weight = opponent_weight
        self.centrality_weight = centrality_weight
        self.bunching_weight = bunching_weight
        self.proximity_weight = proximity_weight

        # initialise board object with independent game state list
        self.state = self.generate_state()

    def __str__(self):
        # function to allow easy printing of board configuration
        return "\n".join([" ".join(line) for line in self.state]) + "\n"

    @staticmethod
    def produce_piece_list(game_state):
        # Deprecated static method for Part A reading in of the board

        white = []
        black = []

        for i in range(8):
            for j in range(8):
                if game_state[i][j] == "O":
                    white.append((i, j))
                elif game_state[i][j] == "@":
                    black.append((i, j))

        return white, black

    def generate_state(self):

        # function to ensure that the values of the state are copied, not the reference
        # hard codes blank state and iterates through and copies values across from old state

        # Hardcoded board sizes for each level of shrinkage. Also shifts board centre for utility function.
        if self.turns < 128:
            new = [["X", "-", "-", "-", "-", "-", "-", "X"],
                   ["-", "-", "-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-", "-", "-"],
                   ["X", "-", "-", "-", "-", "-", "-", "X"]]

        elif self.turns < 192:
            new = [["X", "-", "-", "-", "-", "X"],
                   ["-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-"],
                   ["-", "-", "-", "-", "-", "-"],
                   ["X", "-", "-", "-", "-", "X"]]

            self.upper_edge = 5
            self.centre_x = 2.5
            self.centre_y = 2.5

            # Code to shift all pieces that remain on shrunk baord to new shrunk coordionates
            if self.shrunk == 1:
                self.white = [(checker[0] - 1, checker[1] - 1) for checker in self.white if checker[0]-1 > 0
                              and checker[1]-1 <= self.upper_edge and not new[checker[0]-1][checker[1]-1] == "X"]
                self.black = [(checker[0] - 1, checker[1] - 1) for checker in self.black if checker[0]-1 > 0
                              and checker[1]-1 <= self.upper_edge and not new[checker[0]-1][checker[1]-1] == "X"]
        else:
            new = [["X", "-", "-", "X"],
                   ["-", "-", "-", "-"],
                   ["-", "-", "-", "-"],
                   ["X", "-", "-", "X"]]

            self.upper_edge = 3
            self.centre_x = 1.5
            self.centre_y = 1.5

            # Code to shift all pieces that remain on shrunk baord to new shrunk coordionates
            if self.shrunk == 1:
                self.white = [(checker[0] - 1, checker[1] - 1) for checker in self.white if checker[0]-1 > 0
                              and checker[1]-1 <= self.upper_edge and not new[checker[0]-1][checker[1]-1] == "X"]
                self.black = [(checker[0] - 1, checker[1] - 1) for checker in self.black if checker[0]-1 > 0
                              and checker[1]-1 <= self.upper_edge and not new[checker[0]-1][checker[1]-1] == "X"]

        # Code to place each piece in board's list of pieces on board. Catches error'd pieces.
        for checker in self.white:
            try:
                new[checker[0]][checker[1]] = "O"
            except IndexError:
                self.white.remove(checker)
        for checker in self.black:
            try:
                new[checker[0]][checker[1]] = "@"
            except IndexError:
                self.black.remove(checker)

        # Returns new 2D matrix representation of board
        return new

    def generate_moving_moves(self, colour):
        # Function to generate moves for the moving phase of the game. Generates moves for
        # pieces of "colour" variable colour.

        # Ensures that moves generated don't exceed possible shrunk board dimensions.
        if self.turns >= 190:
            self.upper_edge = 3
        elif self.turns >= 124:
            self.upper_edge = 5

        # list to contain move objects generated from legal move coordinates found below.
        options = []

        # Selects list of pieces to consider
        if colour == "O":
            pieces = self.white
        else:
            pieces = self.black

        # only check for moves around a white piece
        for checker in pieces:

            # for each axis, checks a single space move or a jump is possible.
            # each block checks one of the two directions along the chosen axis.
            # each block also has checks for the edges of the game board

            # check horizontally for moves
            if checker[0] > 0:

                if self.state[checker[0] - 1][checker[1]] == "-":
                    options.append(Move((checker[0], checker[1]), (checker[0] - 1, checker[1])))
                elif self.state[checker[0] - 1][checker[1]] in ["O", "@"]:
                    if checker[0] > 1 and self.state[checker[0] - 2][checker[1]] == "-":
                        options.append(Move((checker[0], checker[1]), (checker[0] - 2, checker[1])))

            if checker[0] < self.upper_edge:

                if self.state[checker[0] + 1][checker[1]] == "-":
                    options.append(Move((checker[0], checker[1]), (checker[0] + 1, checker[1])))
                elif self.state[checker[0] + 1][checker[1]] in ["O", "@"]:
                    if checker[0] < self.upper_edge - 1 and self.state[checker[0] + 2][checker[1]] == "-":
                        options.append(Move((checker[0], checker[1]), (checker[0] + 2, checker[1])))

            # check vertically for moves
            if checker[1] > 0:

                if self.state[checker[0]][checker[1] - 1] == "-":
                    options.append(Move((checker[0], checker[1]), (checker[0], checker[1] - 1)))
                elif self.state[checker[0]][checker[1] - 1] in ["O", "@"]:
                    if checker[1] > 1 and self.state[checker[0]][checker[1] - 2] == "-":
                        options.append(Move((checker[0], checker[1]), (checker[0], checker[1] - 2)))

            if checker[1] < self.upper_edge:

                if self.state[checker[0]][checker[1] + 1] == "-":
                    options.append(Move((checker[0], checker[1]), (checker[0], checker[1] + 1)))
                elif self.state[checker[0]][checker[1] + 1] in ["O", "@"]:
                    if checker[1] < self.upper_edge - 1 and self.state[checker[0]][checker[1] + 2] == "-":
                        options.append(Move((checker[0], checker[1]), (checker[0], checker[1] + 2)))

        # returns move list as independent object from Board object
        return options

    def generate_placing_moves(self, colour):
        # Function to generate moves for placing phase of game.
        # Selects moves for pieces of "colour" variable's colour.

        options = []

        # Determines which piece lists to consider and what areas of the board are playable (depending on the colour).
        if colour == "O":
            lower_limit, upper_limit = 0, 5
            our_team, opp_team = self.white, self.black
        else:
            lower_limit, upper_limit = 2, 7
            our_team, opp_team = self.white, self.white

        # Produces placing moves around teammates.
        if len(our_team) > 0:
            for ally in our_team:
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if 0 + lower_limit <= ally[0] + y <= upper_limit and 0 <= ally[1] + x < 8 \
                                and self.state[ally[0] + y][ally[1] + x] == "-" \
                                and (ally[0] + y, ally[1] + x) not in options:
                            options.append((ally[0] + y, ally[1] + x))
        # produces placing moves around opponents
        elif len(opp_team) > 0:
            for enemy in opp_team:
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if 0 + lower_limit <= enemy[0] + y <= upper_limit and 0 <= enemy[1] + x < 8 \
                                and self.state[enemy[0] + y][enemy[1] + x] == "-" \
                                and (enemy[0] + y, enemy[1] + x) not in options:
                            options.append((enemy[0] + y, enemy[1] + x))

        # Hardcoded moves for opening move.
        else:
            options = [(3, 3), (4, 3), (3, 4), (4, 4)]

        return options

    def place(self, colour, pos):

        # Initialise new board object
        temp = Board(self.white, self.black, self.turns, self.shrunk, self.our_weight, self.opponent_weight,
                     self.centrality_weight, self.bunching_weight, self.proximity_weight)

        # Check not invalid move
        if not temp.state[pos[0]][pos[1]] == "-":
            print("Error, place taken")
            return None

        # Make move on new board object state
        temp.state[pos[0]][pos[1]] = colour

        # Record new piece in appropriate piece list
        if colour == "O":
            temp.white.append(pos)
            opp = "@"
        else:
            temp.black.append(pos)
            opp = "O"

        # Check if placement has causes any kills.
        temp.check_for_kills(colour, opp, pos)

        # Iterate number of turns
        temp.turns += 1

        return temp

    def update_board(self, move):

        # create independent Board object to return
        temp = Board(self.white, self.black, self.turns, self.shrunk, self.our_weight, self.opponent_weight,
                     self.centrality_weight, self.bunching_weight, self.proximity_weight)

        try:
            # determine move end coordinates
            dest = [move.end_pos[0], move.end_pos[1]]

            # update game state of temp Board object:
            temp.state[dest[0]][dest[1]] = temp.state[move.start_pos[0]][move.start_pos[1]]
            temp.state[move.start_pos[0]][move.start_pos[1]] = "-"
        except IndexError:
            print(move)
            print(temp.upper_edge)
            print(temp)

        # Determine colour of piece that just moved
        piece_col = temp.state[dest[0]][dest[1]]

        # Update corresponding piece lists to record piece movement
        if piece_col == "O":
            temp.white.remove((move.start_pos[0], move.start_pos[1]))
            temp.white.append((dest[0], dest[1]))

            opp_col = "@"
        else:
            temp.black.remove((move.start_pos[0], move.start_pos[1]))
            temp.black.append((dest[0], dest[1]))

            opp_col = "O"

        # Check if movement has produced a kill
        temp.check_for_kills(piece_col, opp_col, dest)

        # Iterate number of turns.
        temp.turns += 1

        return temp

    def check_for_kills(self, piece_col, opp_col, dest):

        # determine the team and the enemy of the moving piece.
        if piece_col == "O":
            team, enemies = self.white, self.black
        else:
            team, enemies = self.black, self.white

        # checks for white kills along each axis in turn.
        # check for white kills first as they are moving.
        # then checks for black kills due to white's move.

        # check vertical for team kills
        for y in [-1, 1]:
            if 0 <= dest[1] + y < self.upper_edge + 1 and self.state[dest[0]][dest[1] + y] == opp_col:
                if 0 <= dest[1] + 2 * y < self.upper_edge + 1 and self.state[dest[0]][dest[1] + 2 * y] in [piece_col, "X"]:
                    self.state[dest[0]][dest[1] + y] = "-"
                    enemies.remove((dest[0], dest[1] + y))

        # check horizontal for team kills
        for x in [-1, 1]:
            if 0 <= dest[0] + x < self.upper_edge + 1 and self.state[dest[0] + x][dest[1]] == opp_col:
                if 0 <= dest[0] + 2 * x < self.upper_edge + 1 and self.state[dest[0] + 2 * x][dest[1]] in [piece_col, "X"]:
                    self.state[dest[0] + x][dest[1]] = "-"
                    enemies.remove((dest[0] + x, dest[1]))

        # Ensure the moving piece can't be killed twice.
        dead = False

        # check horizontal for opponent kills
        if 0 <= dest[1] + 1 < self.upper_edge + 1 and self.state[dest[0]][dest[1] + 1] in [opp_col, "X"]:
            if 0 <= dest[1] - 1 < self.upper_edge + 1 and self.state[dest[0]][dest[1] - 1] in [opp_col, "X"]:
                self.state[dest[0]][dest[1]] = "-"
                team.remove((dest[0], dest[1]))
                dead = True

        # check vertical for opponent kills
        if not dead and 0 <= dest[0] + 1 < self.upper_edge + 1 and self.state[dest[0] + 1][dest[1]] in [opp_col, "X"]:
            if 0 <= dest[0] - 1 < self.upper_edge + 1 and self.state[dest[0] - 1][dest[1]] in [opp_col, "X"]:
                self.state[dest[0]][dest[1]] = "-"
                team.remove((dest[0], dest[1]))

    def utility(self, player):

        # Determine the player to which the board state is being valued.
        if player == "O":
            us, them = self.white, self.black
        else:
            us, them = self.black, self.white

        # Initialise value
        score = 0

        # Weigh amount of opponent's pieces remaining
        score += (self.TOTAL_PIECES - len(them)) * self.opponent_weight

        # Weigh amount of our pieces remaining
        score += len(us) * self.our_weight

        if len(us) > 1:

            # Weigh the distance of our pieces from the centre, average the value across remaining pieces to
            # avoid under-weighing towards end of game.
            total_dist = 0
            for piece in us:
                total_dist += abs(self.centre_x - piece[0]) + abs(self.centre_y - piece[1])
            score -= total_dist / len(us) * self.centrality_weight

            # Weigh average distance from each other
            score -= sum([abs(piece[0]-other[0]) + abs(piece[1]-other[1]) for piece in us for other in us]) / \
                     (len(us)*len(us)) * self.bunching_weight

            # Weigh average distance from opponent
            if len(them) > 0:
                score -= sum([abs(piece[0] - other[0]) + abs(piece[1] - other[1]) for piece in us for other in them]) / \
                         (len(us)*len(them)) * self.proximity_weight

        # Add element of randomisation such that identically valued boards are differentiated
        score += random.randint(1, 10)

        return score

    def is_finished(self, player="O"):
        # Determine whether win conditions have been met for a given player.
        if player == "O":
            return len(self.black) < 2
        else:
            return len(self.white) < 2

    def calculate_proximity(self, colour):

        temp = []

        if colour == "O":
            us = list(self.white)
            them = list(self.black)
        else:
            us = list(self.black)
            them = list(self.white)

        for piece in us:

            total = 0
            for enemy in them:
                total += abs(piece[0]-enemy[0]) + abs(piece[1]-enemy[1])

            temp.append((total, piece))

        temp.sort(key=lambda x: x[0], reverse=True)

        return temp


class Move:

    # container for start and end coordinates of a move.
    def __init__(self, start, finish):
        self.start_pos = start
        self.end_pos = finish

    # facilitates easy output of moves for Massacre component as well as easy visualisation of move process
    def __str__(self):
        return "(" + str(self.start_pos[1]) + "," + str(self.start_pos[0]) + \
               ") -> (" + str(self.end_pos[1]) + "," + str(self.end_pos[0]) + ")"



