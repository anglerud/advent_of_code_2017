"""
In this example, the first two numbers in the list end up being 3 and 4; to check the process, you can multiply them together to produce 12.
"""
import io

import pytest

import knot_hash as kh


def test_hash_step_one():
    """
    The list begins as [0] 1 2 3 4 (where square brackets indicate the current position).
    The first length, 3, selects ([0] 1 2) 3 4 (where parentheses indicate the sublist to be reversed).
    After reversing that section (0 1 2 into 2 1 0), we get ([2] 1 0) 3 4.
    Then, the current position moves forward by the length, 3, plus the skip size, 0: 2 1 0 [3] 4. Finally, the skip size increases to 1.
    """
    knotter = kh.KnotHash.new([0, 1, 2, 3, 4])

    assert knotter.current_position == 0
    assert knotter.current_value == 0
    assert knotter.skip_length == 0
    assert knotter.string == [0, 1, 2, 3, 4]

    knottier = knotter.tie(3)

    assert knottier.current_position == 3
    assert knottier.current_value == 3
    assert knottier.skip_length == 1
    assert knottier.string == [2, 1, 0, 3, 4]



def test_hash_step_two():
    """
    The second length, 4, selects a section which wraps: 2 1) 0 ([3] 4.
    The sublist 3 4 2 1 is reversed to form 1 2 4 3: 4 3) 0 ([1] 2.
    The current position moves forward by the length plus the skip size, a total of 5, causing it not to move because it wraps around: 4 3 0 [1] 2. The skip size increases to 2.
    """
    knotter = kh.KnotHash.new([0, 1, 2, 3, 4])
    knotter = knotter.tie(3)
    knotter = knotter.tie(4)

    assert knotter.skip_length == 2
    assert knotter.current_position == 3
    assert knotter.current_value == 1
    assert knotter.string == [4, 3, 0, 1, 2]



def test_hash_step_three():
    """
    The third length, 1, selects a sublist of a single element, and so reversing it has no effect.
    The current position moves forward by the length (1) plus the skip size (2): 4 [3] 0 1 2. The skip size increases to 3.
    """
    knotter = kh.KnotHash.new([0, 1, 2, 3, 4])
    knotter = knotter.tie(3)
    knotter = knotter.tie(4)
    knotter = knotter.tie(1)

    assert knotter.skip_length == 3
    assert knotter.current_position == 1
    assert knotter.current_value == 3
    assert knotter.string == [4, 3, 0, 1, 2]


def test_hash_step_four():
    """
    The fourth length, 5, selects every element starting with the second: 4) ([3] 0 1 2. Reversing this sublist (3 0 1 2 4 into 4 2 1 0 3) produces: 3) ([4] 2 1 0.
    Finally, the current position moves forward by 8: 3 4 2 1 [0]. The skip size increases to 4.
    """
    knotter = kh.KnotHash.new([0, 1, 2, 3, 4])
    knotter = knotter.tie(3)
    knotter = knotter.tie(4)
    knotter = knotter.tie(1)
    knotter = knotter.tie(5)

    assert knotter.skip_length == 4
    assert knotter.current_position == 4
    assert knotter.current_value == 0
    assert knotter.string == [3, 4, 2, 1, 0]

    assert knotter.checksum == 12


@pytest.mark.parametrize('example,expected', [
    ('', 'a2582a3a0e66e6e86e3812dcb672a272'),
    ('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
    ('1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'),
    ('1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e')
])
def test_dense_hashes(example, expected):
    example_io = io.StringIO(example)
    assert kh.rudolph_santa_advent_hash(example_io) == expected
