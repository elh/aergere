import pytest

from aergere.board import Board, Peg
from aergere.aergere import valid_moves, move


@pytest.mark.parametrize(
    "roll,color,expected",
    [
        pytest.param(6, 0, [(0, Peg(0)), (1, Peg(0)), (2, Peg(0)), (3, Peg(0))]),
        pytest.param(6, 1, [(0, Peg(10)), (1, Peg(10)), (2, Peg(10)), (3, Peg(10))]),
        pytest.param(6, 2, [(0, Peg(20)), (1, Peg(20)), (2, Peg(20)), (3, Peg(20))]),
        pytest.param(6, 3, [(0, Peg(30)), (1, Peg(30)), (2, Peg(30)), (3, Peg(30))]),
        pytest.param(5, 0, []),
    ],
)
def test_valid_moves_initial_board(roll, color, expected):
    b = Board()
    assert valid_moves(b, color, roll) == expected


@pytest.mark.parametrize(
    "roll,expected",
    [
        pytest.param(6, [(0, Peg(6))]),
        pytest.param(5, [(0, Peg(5))]),
        pytest.param(1, [(0, Peg(1))]),
    ],
)
def test_valid_moves_on_own_start(roll, expected):
    b = Board(pegs_0=[Peg(0), Peg(), Peg(), Peg()])

    assert valid_moves(b, 0, roll) == expected


@pytest.mark.parametrize(
    "roll,expected",
    [
        pytest.param(6, [(0, Peg(7)), (1, Peg(0)), (2, Peg(0)), (3, Peg(0))]),
        pytest.param(5, [(0, Peg(6))]),
    ],
)
def test_valid_moves_multiple(roll, expected):
    b = Board(pegs_0=[Peg(1), Peg(), Peg(), Peg()])
    assert valid_moves(b, 0, roll) == expected


@pytest.mark.parametrize(
    "roll,expected",
    [
        pytest.param(1, [(1, Peg(9))]),  # no self capture, can capture others
        pytest.param(2, [(0, Peg(9))]),  # cannot capture other color on own start
    ],
)
def test_valid_moves_capture(roll, expected):
    b = Board(pegs_0=[Peg(7), Peg(8), Peg(), Peg()], pegs_1=[Peg(9), Peg(10), Peg(), Peg()])
    assert valid_moves(b, 0, roll) == expected


@pytest.mark.parametrize(
    "board,roll,expected",
    [
        # exactly to home index. just outside of home
        pytest.param({"pegs_0": [Peg(38), Peg(), Peg(), Peg()]}, 1, [(0, Peg(39))]),
        # into home
        pytest.param({"pegs_0": [Peg(38), Peg(), Peg(), Peg()]}, 2, [(0, Peg(0, True))]),
        pytest.param({"pegs_0": [Peg(39), Peg(), Peg(), Peg()]}, 1, [(0, Peg(0, True))]),
        # too far
        pytest.param({"pegs_0": [Peg(39), Peg(), Peg(), Peg()]}, 6, [(1, Peg(0)), (2, Peg(0)), (3, Peg(0))]),
        pytest.param({"pegs_0": [Peg(39), Peg(), Peg(), Peg()]}, 5, []),
        # blocked
        pytest.param({"pegs_0": [Peg(38), Peg(0, True), Peg(), Peg()]}, 4, []),
        pytest.param({"pegs_0": [Peg(38), Peg(1, True), Peg(), Peg()]}, 4, []),
        pytest.param({"pegs_0": [Peg(38), Peg(2, True), Peg(), Peg()]}, 4, []),
        # moves in home should not affect others
        pytest.param(
            {"pegs_0": [Peg(38), Peg(), Peg(), Peg()], "pegs_1": [Peg(0, True), Peg(), Peg(), Peg()]},
            2,
            [(0, Peg(0, True))],
        ),
    ],
)
def test_valid_moves_into_home(board, roll, expected):
    b = Board(**board)

    assert valid_moves(b, 0, roll) == expected


@pytest.mark.parametrize(
    "board,roll,expected",
    [
        pytest.param({"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()]}, 1, [(0, Peg(1, True))]),
        pytest.param({"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()]}, 3, [(0, Peg(3, True))]),
        # too far
        pytest.param({"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()]}, 4, []),
        # blocked
        pytest.param({"pegs_0": [Peg(0, True), Peg(1, True), Peg(), Peg()]}, 1, [(1, Peg(2, True))]),
        pytest.param({"pegs_0": [Peg(0, True), Peg(3, True), Peg(), Peg()]}, 3, []),
    ],
)
def test_valid_moves_in_home(board, roll, expected):
    b = Board(**board)

    assert valid_moves(b, 0, roll) == expected


@pytest.mark.parametrize(
    "board,color,roll,peg,expected",
    [
        # come out
        pytest.param({}, 0, 6, 0, {"pegs_0": [Peg(0), Peg(), Peg(), Peg()]}),
        pytest.param({}, 0, 6, 1, {"pegs_0": [Peg(), Peg(0), Peg(), Peg()]}),
        pytest.param({"pegs_0": [Peg(1), Peg(), Peg(), Peg()]}, 0, 6, 1, {"pegs_0": [Peg(1), Peg(0), Peg(), Peg()]}),
        # movement
        pytest.param({"pegs_0": [Peg(0), Peg(), Peg(), Peg()]}, 0, 6, 0, {"pegs_0": [Peg(6), Peg(), Peg(), Peg()]}),
        pytest.param({"pegs_0": [Peg(0), Peg(), Peg(), Peg()]}, 0, 5, 0, {"pegs_0": [Peg(5), Peg(), Peg(), Peg()]}),
        # capture
        pytest.param(
            {"pegs_0": [Peg(0), Peg(), Peg(), Peg()], "pegs_1": [Peg(3), Peg(4), Peg(), Peg()]},
            0,
            3,
            0,
            {"pegs_0": [Peg(3), Peg(), Peg(), Peg()], "pegs_1": [Peg(), Peg(4), Peg(), Peg()]},
        ),
        # moving into home
        pytest.param({"pegs_0": [Peg(38), Peg(), Peg(), Peg()]}, 0, 1, 0, {"pegs_0": [Peg(39), Peg(), Peg(), Peg()]}),
        pytest.param(
            {"pegs_0": [Peg(39), Peg(), Peg(), Peg()]}, 0, 1, 0, {"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()]}
        ),
        pytest.param(
            {"pegs_0": [Peg(38), Peg(), Peg(), Peg()]}, 0, 2, 0, {"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()]}
        ),
        pytest.param(
            {"pegs_0": [Peg(38), Peg(2, True), Peg(), Peg()]},
            0,
            3,
            0,
            {"pegs_0": [Peg(1, True), Peg(2, True), Peg(), Peg()]},
        ),
        # moving within home
        pytest.param(
            {"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()]}, 0, 1, 0, {"pegs_0": [Peg(1, True), Peg(), Peg(), Peg()]}
        ),
        pytest.param(
            {"pegs_0": [Peg(1, True), Peg(), Peg(), Peg()]}, 0, 2, 0, {"pegs_0": [Peg(3, True), Peg(), Peg(), Peg()]}
        ),
        pytest.param(
            {"pegs_0": [Peg(1, True), Peg(3, True), Peg(), Peg()]},
            0,
            1,
            0,
            {"pegs_0": [Peg(2, True), Peg(3, True), Peg(), Peg()]},
        ),
        # moves in home should not affect others
        pytest.param(
            {"pegs_0": [Peg(38), Peg(), Peg(), Peg()], "pegs_1": [Peg(0, True), Peg(), Peg(), Peg()]},
            0,
            2,
            0,
            {"pegs_0": [Peg(0, True), Peg(), Peg(), Peg()], "pegs_1": [Peg(0, True), Peg(), Peg(), Peg()]},
        ),
    ],
)
def test_move(board, color, roll, peg, expected):
    b = Board(**board)
    assert move(b, color, roll, peg).pegs == Board(**expected).pegs


@pytest.mark.parametrize(
    "board,color,roll,peg",
    [
        pytest.param({}, 0, 5, 0),
        pytest.param({"pegs_0": [Peg(0), Peg(), Peg(), Peg()]}, 0, 6, 1),
    ],
)
def test_invalid_move(board, color, roll, peg):
    b = Board(**board)
    with pytest.raises(ValueError):
        move(b, color, roll, peg)
