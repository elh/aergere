import random

from aergere.board import Board, Peg, Colors, has_winner, print_board
from aergere.aergere import valid_moves, move

TURN_LIMIT = 500


def turn(b: Board, color: int) -> tuple[int, tuple[int, Peg], Board]:
    """Makes a turn and returns the updated board."""
    roll = random.randint(1, 6)
    moves = valid_moves(b, color, roll)
    if not moves:
        return roll, None, b
    m = random.choice(moves)  # NOTE: selects a move at random!

    return roll, m, move(b, color, roll, m[0])


def main():
    b = Board()
    for i in range(1, TURN_LIMIT + 1):
        color = i % 4
        while True:  # handle re-rolls on 6s
            roll, m, next_b = turn(b, color)
            if m is not None:
                prior_peg = b.pegs[color][m[0]]
                print(
                    f"turn {i} - {Colors[color]} rolled {roll} and moved peg:{m[0]} from {"H" if prior_peg.is_home else ""}{prior_peg.position_idx} to {"H" if m[1].is_home else ""}{m[1].position_idx}"
                )
            else:
                print(f"turn {i} - {Colors[color]} rolled {roll} and has no moves")
            b = next_b

            w = has_winner(b)
            if w is not None:
                print_board(b)
                print(f"\n{Colors[color]} wins on turn {i}")
                return

            if roll != 6:
                break


if __name__ == "__main__":
    main()
