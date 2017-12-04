"""

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

NOTE: the spiral is 1-indexed.
"""
import itertools

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


# ==== Part 2
def nth(iterable, index):
    """Returns the nth item"""
    return next(itertools.islice(iterable, index, None))


def test_sum_pos_2() -> None:
    """Square 2 has one adjacent filled square (with 1), so it stores 1."""
    # Note: We take 1 step (first item) - thus end up on square 2
    # (square 1 being home).
    assert nth(sw.sum_walk(), 0) == 1


def test_sum_pos_3() -> None:
    """Square 3 has both of the above squares as neighbors and stores 2."""
    # 2nd step - 3rd square
    assert nth(sw.sum_walk(), 1) == 2


def test_sum_pos_4() -> None:
    """Square 4 has all three squares as neighbors and stores 4."""
    # Third step, 4th square.
    assert nth(sw.sum_walk(), 2) == 4


def test_sum_pos_5() -> None:
    """Square 5 has the first and fourth squares as neighbors, so stores 5."""
    # Fourth step, 5th square.
    assert nth(sw.sum_walk(), 3) == 5


def test_sum_larger_than_4() -> None:
    """First value larger than 4 in a location is 5, in location 5."""
    assert sw.sum_bigger_than(4) == 5
