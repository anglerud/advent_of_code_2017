"""

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

NOTE: the spiral is 1-indexed.
"""
import spiral_walk as sw


def test_first_pos() -> None:
    """Data from square 1 is carried 0 steps, since it's at the access port."""
    assert sw.walk_to(1) == sw.Coordinate(0, 0)


def test_pos_one_east() -> None:
    """ """
    assert sw.walk_to(2) == sw.Coordinate(1, 0)


def test_pos_12() -> None:
    """Data from square 12 is carried 3 steps, such as: down, left, left."""
    assert sw.walk_to(12).distance == 3


def test_pos_23() -> None:
    """Data from square 23 is carried only 2 steps: up twice."""
    assert sw.walk_to(23).distance == 2


def test_pos_1024() -> None:
    """Data from square 1024 must be carried 31 steps."""
    assert sw.walk_to(1024).distance == 31
