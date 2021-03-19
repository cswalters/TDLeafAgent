import Board
import Player


def main():

    turns = 0

    game = Board.Board([], [], 0, 0, 0, 0, 0, 0, 0)
    player1 = Player.Player("white")
    player2 = Player.Player("black")

    while (turns < 24) or (not game.is_finished("O") and not game.is_finished("@")):

        print(game.turns)

        action = player1.action(turns)

        if turns < 24:
            game = game.place(player1.colour, action)
        else:
            game = game.update_board(Board.Move(action[0], action[1]))

        player2.update(action)

        print(game)

        action = player2.action(turns)

        if turns < 24:
            game = game.place(player2.colour, action)
        else:
            game = game.update_board(Board.Move(action[0], action[1]))

        player1.update(action)

        print(game)

        turns += 2

        print("////////")


if __name__ == "__main__":
    main()
