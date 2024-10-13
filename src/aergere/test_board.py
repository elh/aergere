import pytest

from aergere.board import Board, Peg, has_winner


# starting positions for a color
def pegs() -> list[Peg]:
    return [Peg() for _ in range(4)]


@pytest.mark.parametrize(
    "input",
    [
        pytest.param({"pegs": None}),
        pytest.param({"pegs": [pegs(), pegs(), pegs(), pegs()]}),
        pytest.param({"pegs_0": pegs()}),
        pytest.param({"pegs_0": [Peg(0), Peg(1), Peg(2), Peg(3)]}),
        pytest.param({"pegs_0": [Peg(0, True), Peg(1, True), Peg(2), Peg(3)]}),
        pytest.param(
            {
                "pegs_0": [Peg(0, True), Peg(1, True), Peg(2), Peg(3)],
                "pegs_1": [Peg(0, True), Peg(1, True), Peg(4), Peg(5)],
            }
        ),
    ],
)
def test_board(input):
    Board(**input)


@pytest.mark.parametrize(
    "input",
    [
        pytest.param({"pegs": [pegs(), pegs(), pegs()]}),
        pytest.param({"pegs_0": [Peg()]}),
        pytest.param({"pegs_0": [Peg(100), Peg(), Peg(), Peg()]}),
        pytest.param({"pegs_0": [Peg(-1), Peg(), Peg(), Peg()]}),
        pytest.param({"pegs_0": [Peg(5, True), Peg(), Peg(), Peg()]}),
        pytest.param({"pegs_0": [Peg(0), Peg(0), Peg(), Peg()]}),
        pytest.param(
            {
                "pegs_0": [Peg(0), Peg(), Peg(), Peg()],
                "pegs_1": [Peg(0), Peg(), Peg(), Peg()],
            }
        ),
    ],
)
def test_invalid_board(input):
    with pytest.raises(AssertionError):
        Board(**input)


def test_has_winner():
    b = Board()
    assert has_winner(b) is None

    b.pegs[0] = [Peg(0, True), Peg(1, True), Peg(), Peg()]
    assert has_winner(b) is None

    b.pegs[0] = [Peg(0, True), Peg(1, True), Peg(True, 2), Peg(True, 3)]
    assert has_winner(b) == 0
