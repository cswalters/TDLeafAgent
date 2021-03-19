# TDLeafAgent
AI for custom Watch Your Back! board game (adapted from checkers) that leverages TDLeaf algorithm.

"Player.py" is the intended Player class for use in this project.

The Player class is split up into multiple components: a board class, a player class for the placement phase, and a player class for the movement phase.

The board class holds all game logic and holds the function for evaluating the board's value to any given player. It handles movement of pieces, alteration to board size etc (all game events). The two player classes, PlacingPlayer and MovingPlayer, handle the Placing Phase and Moving Phase respectively. They both employ alpha-beta pruning but differ slightly as to what Board functions they employ. The Player file/class brings this all together and plays the game using the Board class to represent the gmae and the appropriate XXXPlayer class to make moves. It also contains the code for a TDleaf-lambda algorithm in order to find the best coefficients for our utility function. The original intention was to run the algorithm against itself for a prolonged period of time, reading and writing to a file in order to save the coefficients between games, then hard-code said coefficients into the final version. Since implementation took longer than expected, instead the Player class is set to update its coefficients in real time during testing.

Gradient Descent was considered briefly, but deemed unviable; the sheer depth of search space and branching width combined with lack of sufficient training examples made it unreasonable even before considering the problems of delayed reinforcement and credit assignment.

Instead, TDLeaf was used to update the heuristic weights in response to changes in value of subsequent states. However, it ran into several errors and succesful implementation was achieved too late to allow for the extensive extensive runtime to train the program.

The board itself is represented as two lists of coordinates that represent the pieces; this decision was intended to make the algorithm run faster (rather than having to search through the whole board) and thus allow for searches of higher ply.

The searching strategy used was a minimax with alpha-beta pruning. To try and maximise the effectiveness of said pruning, we attempted to sort moves by order of how close the piece to be moved is to the enemy pieces, but this was regarded as too inefficient in practice and would have taken too much time to implement. The evaluation function used was a sum of linear terms, valuing the following: -the number of allied pieces on the board -the number of enemy pieces eliminated -how close allied pieces are to the center of the board -how close allied pieces are to each other -how close allied pieces are to enemy pieces

"partb.py" is a rudimentary program intended simply to test basic player functionality. MovingPlayer and PlacingPlayer are files that are used by the Player file/class and do not represent alternative players for the referee.
