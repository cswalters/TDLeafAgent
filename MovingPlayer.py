import sys

# Skeleton of code taken  from AIMA website: http://aima.cs.berkeley.edu/python/games.html
# Adapted by Marcus Swann and Chris Walters for Watch Your Back!


def alphabeta_search(player, opponent, board, d=3):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    # Function to evaluate most valuable next move to player denoted by "player" variable
    def max_value(current, alpha, beta, depth):
        # Checks if search should terminate due to game completion or reaching max depth
        if cutoff_test(current, depth):
            return eval_fn(current)
        value = -sys.maxsize
        # Iterates through possible moves for other player (min) and explores each consequent state
        for move in current.generate_moving_moves(player):
            value = max(value, min_value(current.update_board(move), alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    # Function to evaluate least valuable next move to player denoted by "player" variable
    def min_value(current, alpha, beta, depth):
        # Checks if search should terminate due to game completion or reaching max depth
        if cutoff_test(current, depth):
            return eval_fn(current)
        value = sys.maxsize
        # Iterates through possible moves for other player (max) and explores each consequent state
        for move in current.generate_moving_moves(opponent):
            value = min(value, max_value(current.update_board(move), alpha, beta, depth + 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    # Body of alphabeta_search starts here:
    # The test cuts off at depth d or at a terminal state
    cutoff_test = lambda state, depth: depth > d or state.is_finished(player)
    # Alphabeta search evaluates board's value based on utility function in Board class.
    eval_fn = lambda state: state.utility(player)

    # Determine action to be made
    action = max([(min_value(board.update_board(move), -sys.maxsize, sys.maxsize, 0), move) for move in
                  board.generate_moving_moves(player)],
                 key=lambda item: item[0])[1]

    return action
