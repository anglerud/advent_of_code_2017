"""Haven't tested the von Santa machine. Only a madman would try."""
import pytest

import virtual_machine as v


def test_load() -> None:
    """(0) 3  0  1  -3  - before we have taken any steps."""
    vm = v.Machine.load([0, 3, 0, 1, -3])
    assert vm.program_counter == 0
    assert vm.in_bounds is True
    assert vm.instruction_count == 0
    assert vm.memory == [0, 3, 0, 1, -3]


def test_inc_jump_0() -> None:
    """(1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all). Fortunately, the instruction is then incremented to 1."""
    vm = v.Machine.load([0, 3, 0, 1, -3]).step()

    assert vm.program_counter == 0
    assert vm.peek == 1
    assert vm.in_bounds is True
    assert vm.instruction_count == 1
    assert vm.memory == [1, 3, 0, 1, -3]


def test_inc_jump_one() -> None:
    """ 2 (3) 0  1  -3  - step forward because of the instruction we just modified. The first instruction is incremented again, now to 2."""
    vm = v.Machine.load([0, 3, 0, 1, -3]).step().step()

    assert vm.program_counter == 1
    assert vm.peek == 3
    assert vm.in_bounds is True
    assert vm.instruction_count == 2
    assert vm.memory == [2, 3, 0, 1, -3]


def test_inc_jump_three() -> None:
    """2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind."""
    vm = v.Machine.load([0, 3, 0, 1, -3]).step().step().step()

    assert vm.program_counter == 4
    assert vm.peek == -3
    assert vm.in_bounds is True
    assert vm.instruction_count == 3
    assert vm.memory == [2, 4, 0, 1, -3]


def test_inc_jump_negative_three() -> None:
    """2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2."""
    vm = v.Machine.load([0, 3, 0, 1, -3]).step().step().step().step()

    assert vm.program_counter == 1
    assert vm.peek == 4
    assert vm.in_bounds is True
    assert vm.instruction_count == 4
    assert vm.memory == [2, 4, 0, 1, -2]


def test_inc_jump_segfault() -> None:
    """ 2  5  0  1  -2  - jump 4 steps forward, escaping the maze.

    In this example, the exit is reached in 5 steps.
    """
    vm = v.Machine.load([0, 3, 0, 1, -3]).step().step().step().step().step()

    assert vm.program_counter == 5  # invalid, yay.
    assert vm.in_bounds is False
    assert vm.instruction_count == 5
    assert vm.memory == [2, 5, 0, 1, -2]

    with pytest.raises(v.SegFault):
        vm.peek

    with pytest.raises(v.SegFault):
        vm.step()
