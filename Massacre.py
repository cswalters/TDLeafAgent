import queue


class Board:

    # initialise piece counters
    num_white = 0
    num_black = 0

    def __init__(self, game_state, white=0, black=0):
        # initialise board object with independent game state list
        self.state = self.state_deep_copy(game_state)

        # either is passed number of pieces or iterate through game state and count number of pieces remaining
        if white and black:
            self.num_black = black
            self.num_white = white
        else:
            for i in range(8):
                for j in range(8):
                    if self.state[i][j] == "O":
                        self.num_white += 1
                    elif self.state[i][j] == "@":
                        self.num_black += 1

    def __str__(self):
        # function to allow easy printing of board configuration
        return "\n".join([" ".join(line) for line in self.state]) + "\n"

    def state_deep_copy(self, state):
        # function to ensure that the values of the state are copied, not the reference

        # hard codes blank state and iterates through and copies values across from old state
        new = [[], [], [], [], [], [], [], []]

        col = 0

        for line in state:
            new[col] = list(line)
            col += 1

        return new

    def generate_white_moves(self):

        # list to contain move objecvts generated from legal move coordinates found below.
        options = []

        # iterate through game board
        for col in range(8):
            for row in range(8):

                # only check for moves around a white piece
                if self.state[col][row] == "O":

                    # for each axis, checks a single space move or a jump is possible.
                    # each block checks one of the two directions along the chosen axis.
                    # each block also has checks for the edges of the game board

                    # check horizontally for moves
                    if col > 0:

                        if self.state[col - 1][row] == "-":
                            options.append(Move((col, row), (col - 1, row)))
                        elif self.state[col - 1][row] in ["O", "@"]:
                            if col > 1 and self.state[col - 2][row] == "-":
                                options.append(Move((col, row), (col - 2, row)))

                    if col < 7:

                        if self.state[col + 1][row] == "-":
                            options.append(Move((col, row), (col + 1, row)))
                        elif self.state[col + 1][row] in ["O", "@"]:
                            if col < 6 and self.state[col + 2][row] == "-":
                                options.append(Move((col, row), (col + 2, row)))

                    # check vertically for moves
                    if row > 0:

                        if self.state[col][row - 1] == "-":
                            options.append(Move((col, row), (col, row - 1)))
                        elif self.state[col][row - 1] in ["O", "@"]:
                            if row > 1 and self.state[col][row - 2] == "-":
                                options.append(Move((col, row), (col, row - 2)))

                    if row < 7:

                        if self.state[col][row + 1] == "-":
                            options.append(Move((col, row), (col, row + 1)))
                        elif self.state[col][row + 1] in ["O", "@"]:
                            if row < 6 and self.state[col][row + 2] == "-":
                                options.append(Move((col, row), (col, row + 2)))

        # returns move list as independent object from Board object
        return options

    def update_board(self, move):

        # create independent Board object to return
        temp = Board(self.state, self.num_white, self.num_black)

        # determine move end coordinates
        dest = [move.end_pos[0], move.end_pos[1]]

        # update game state of temp Board object
        temp.state[dest[0]][dest[1]] = temp.state[move.start_pos[0]][move.start_pos[1]]
        temp.state[move.start_pos[0]][move.start_pos[1]] = "-"

        # checks for white kills along each axis in turn.
        # check for white kills first as they are moving.
        # then checks for black kills due to white's move.

        # check vertical for white kills
        for y in [-1, 1]:
            if 0 <= dest[1] + y < 8 and temp.state[dest[0]][dest[1] + y] == "@":
                if 0 <= dest[1] + 2 * y < 8 and temp.state[dest[0]][dest[1] + 2 * y] in ["O", "X"]:
                    temp.state[dest[0]][dest[1] + y] = "-"
                    temp.num_black -= 1

        # check horizontal for white kills
        for x in [-1, 1]:
            if 0 <= dest[0] + x < 8 and temp.state[dest[0] + x][dest[1]] == "@":
                if 0 <= dest[0] + 2 * x < 8 and temp.state[dest[0] + 2 * x][dest[1]] in ["O", "X"]:
                    temp.state[dest[0] + x][dest[1]] = "-"
                    temp.num_black -= 1

        # check horizontal for black kills
        for x in [-1, 1]:
            if 0 <= dest[1] + x < 8 and temp.state[dest[0]][dest[1] + x] == "@":
                if 0 <= dest[1] - x < 8 and temp.state[dest[0]][dest[1] - x] in ["@", "X"]:
                    temp.state[dest[0]][dest[1]] = "-"
                    temp.num_white -= 1

        # check vertical for black kills
        for y in [-1, 1]:
            if 0 <= dest[0] + y < 8 and temp.state[dest[0] + y][dest[1]] == "@":
                if 0 <= dest[0] - y < 8 and temp.state[dest[0] - y][dest[1]] in ["@", "X"]:
                    temp.state[dest[0]][dest[1]] = "-"
                    temp.num_white -= 1

        # return updated Board object
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


class ArtificialPlayer:

    # simply holds desired game state and determines a static solution to it
    def __init__(self, game):
        self.initial_state = game

    def calculate_strategy(self):

        # Uses breadth-first search to find state solution

        solution = []

        # determines final solution state and dict of nodes and predecessors that lead to it
        end_state, path_dict = bfs(self.initial_state.state)

        # catches failure to find solution
        if not end_state:
            return None

        # finds predecessor node of final state
        final = end_state[2]

        # adds final move
        solution.append(end_state[3])

        # loops through predecessors, adding the move that resulted in them to solution list.
        while final:
            solution.append(path_dict[final][3])
            final = path_dict[final][2]

        # reverses list so correct order of moves is produced and returns move list
        return list(reversed(solution))


def bfs(init_state):

    # initialise start node of search graph
    # tuple of Board object, distance travelled to arrive at this state, predecessor Board object and move
    # that resulted in  this Board object from the predecessor.
    start = (Board(init_state), 0, None, None)

    # initialise queue to hold nodes to-be-explored
    # initialise oath_dict to hold history of nodes, for determining move sequence
    q = queue.Queue()
    path_dict = {}

    # begin the queue with the initial Board
    q.put(start)
    path_dict[start[0]] = start

    # search until no nodes left to search
    while q.qsize() > 0:

        current = q.get()

        # for current node, determine all possible moves
        for move in current[0].generate_white_moves():

            # simulate making move
            temp = current[0].update_board(move)
            new = (temp, current[1] + 1, current[0], move)

            # check for goal
            if temp.num_black == 0:
                return new, path_dict

            # if not goal, add to queue and keep searching
            q.put(new)
            path_dict[new[0]] = new
