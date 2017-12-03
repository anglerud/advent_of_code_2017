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
    """ """
    assert sw.index_to_coord(1) == sw.Coordinate(0, 0)


def test_pos_one_east() -> None:
    """ """
    assert sw.index_to_coord(2) == sw.Coordinate(1, 0)


def test_manhattan_distance_from_origin() -> None:
    """ """
    assert sw.distance(sw.Coordinate(0, 0)) == 0
