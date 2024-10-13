from typing import Union
import collections

"""Player colors in order"""
Colors = ["yellow", "green", "red", "black"]

"""Peg's position on the board

position_idx (Union[int, None]): None if peg is "out", else index in either the track or own color's home.
is_home (bool): True if the peg is in own color's home.
"""
Peg = collections.namedtuple("Peg", ["position_idx", "is_home"], defaults=[None, False])


class Board:
    """Board state. Construct with either `pegs` XOR the color-specific `pegs_i` lists.

    Args:
        pegs (list[list[Peg]], optional): 4 pegs for each of the 4 colors.
        pegs_0 (list[Peg], optional): For yellow.
        pegs_1 (list[Peg], optional): For green.
        pegs_2 (list[Peg], optional): For red.
        pegs_3 (list[Peg], optional): For black.

    Attributes:
        pegs (list[list[Peg]]): 4 pegs for each of the 4 colors.
        track (list[Union[int, None]]): 40 positions making the outer track of the board.
        homes (list[list[Union[int, None]]]): for the 4 colors, 4 positions making the home row.
    """

    def __validate_pegs(self):
        assert len(self.pegs) == 4, "pegs must have length of 4 (4 colors)"

        track_pegs = []
        for color_idx, pegs in enumerate(self.pegs):
            assert len(pegs) == 4, "each inner peg list must have length of 4"
            for peg_idx, p in enumerate(pegs):
                if not (
                    (not p.is_home and p.position_idx is None)
                    or (not p.is_home and 0 <= p.position_idx <= 39)
                    or (p.is_home and 0 <= p.position_idx <= 4)
                ):
                    raise AssertionError(f"color:{color_idx} peg:{peg_idx} contains invalid value: {p}")

                if p.is_home and p.position_idx is None:
                    raise AssertionError(f"color:{color_idx} peg:{peg_idx} is home but has no position")

                if not p.is_home and p.position_idx is not None:
                    track_pegs.append(p)

            home_pegs = [p for p in pegs if p.is_home]
            if len(home_pegs) != len(set(home_pegs)):
                raise AssertionError(f"color:{color_idx} has multiple pegs in the same home position")

        if len(track_pegs) != len(set(track_pegs)):
            raise AssertionError("multiple pegs are in the same track location")

    def __update_track_and_homes(self):
        self.track: list[Union[int, None]] = [None for _ in range(40)]
        self.homes: list[list[Union[int, None]]] = [[None for _ in range(4)] for _ in range(4)]

        for color_idx, pegs in enumerate(self.pegs):
            for p in pegs:
                if p.position_idx is None:
                    continue
                if p.is_home:
                    self.homes[color_idx][p.position_idx] = color_idx
                else:
                    self.track[p.position_idx] = color_idx

    def __init__(
        self,
        pegs: list[list[Peg]] = None,  # all of them
        pegs_0: list[Peg] = None,  # yellow
        pegs_1: list[Peg] = None,  # green
        pegs_2: list[Peg] = None,  # red
        pegs_3: list[Peg] = None,  # black
    ):
        if pegs is not None and (pegs_0 is not None or pegs_1 is not None or pegs_2 is not None or pegs_3 is not None):
            raise AssertionError("cannot provide any of the color-specific args and the full pegs arg in the same call")
        if pegs is None:
            pegs = [
                pegs_i if pegs_i is not None else [Peg() for _ in range(4)]
                for pegs_i in [pegs_0, pegs_1, pegs_2, pegs_3]
            ]
        self.pegs: list[list[Peg]] = pegs

        self.__validate_pegs()
        self.__update_track_and_homes()


def start_position_idx(color: int) -> int:
    """Returns the track index of the starting position."""
    return color * 10


def has_winner(board: dict[str, list]) -> Union[int, None]:
    """Returns the color of the winner if there is one."""
    for color, pegs in enumerate(board.pegs):
        if all(peg.is_home for peg in pegs):
            return color
    return None


def print_board(b: Board):
    """Prints the board state."""
    for color, pegs in enumerate(b.pegs):
        print(f"{Colors[color]}\t", [peg.position_idx if not peg.is_home else f"H{peg.position_idx}" for peg in pegs])
