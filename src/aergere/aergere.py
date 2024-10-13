from aergere.board import Board, Peg, start_position_idx


def valid_moves(board: Board, color: int, roll: int) -> list[(int, Peg)]:
    """Returns a list of valid candidate moves given a roll.

    A tuple contains the peg index and its possible new position.
    """
    out = []
    for peg_idx, p in enumerate(board.pegs[color]):
        is_out = not p.is_home and p.position_idx is None
        if is_out:
            start = start_position_idx(color)
            if roll == 6 and board.track[start] is None:
                out.append((peg_idx, Peg(start)))
        elif p.is_home:
            home_target_idx = p.position_idx + roll
            is_blocked = (
                sum(1 for e in board.homes[color][p.position_idx + 1 : home_target_idx + 1] if e is not None) > 0
            )
            if home_target_idx > 3 or is_blocked:
                continue  # blocked or going too far

            out.append((peg_idx, Peg(home_target_idx, True)))
        else:
            # check if it can advance into home
            next_home_peg = None
            bad_roll_into_home = False
            for i in range(1, roll + 1):
                step_to = (p.position_idx + i) % 40
                if step_to == start_position_idx(color):
                    home_target_idx = roll - i
                    is_blocked = sum(1 for e in board.homes[color][0 : home_target_idx + 1] if e is not None) > 0
                    if home_target_idx > 3 or is_blocked:
                        bad_roll_into_home = True
                    else:
                        next_home_peg = Peg(home_target_idx, True)
                    break
            if bad_roll_into_home:
                continue  # blocked or going too far
            if next_home_peg is not None:
                out.append((peg_idx, next_home_peg))
                continue

            # check if it can advance on track
            target_idx = (p.position_idx + roll) % 40
            target_color = board.track[target_idx]
            if target_color == color:
                continue  # can't throw out self
            if target_color is not None and target_idx == start_position_idx(target_color):
                continue  # can't throw out opponent on their own start

            out.append((peg_idx, Peg(target_idx)))

    return out


def move(board: Board, color: int, roll: int, peg: int) -> Board:
    """Returns the updated board after peg is moved."""
    moves = valid_moves(board, color, roll)
    next_peg = next((move[1] for move in moves if move[0] == peg), None)
    if next_peg is None:
        raise ValueError(f"color:{color} peg:{peg} cannot move for roll of {roll}")

    # with captures
    next_pegs = [[p if p.is_home or p != next_peg else Peg() for p in color_pegs] for color_pegs in board.pegs]
    # with moved peg
    next_pegs[color][peg] = next_peg

    return Board(next_pegs)
