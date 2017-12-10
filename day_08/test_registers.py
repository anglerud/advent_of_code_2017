""" """
import operator

import registers as r


def test_example_1():
    op_str = "b inc 5 if a > 1"
    op = r.Op.from_line(op_str)

    assert op.store_register == 'b'
    assert op.operation == r.Mnemonic.INC
    assert op.change_value == 5
    assert op.compare_register == 'a'
    assert op.comparison is operator.gt
    assert op.compare_value == 1


def test_example_2():
    op_str = "a inc 1 if b < 5"
    op = r.Op.from_line(op_str)

    assert op.store_register == 'a'
    assert op.operation == r.Mnemonic.INC
    assert op.change_value == 1
    assert op.compare_register == 'b'
    assert op.comparison is operator.lt
    assert op.compare_value == 5


def test_example_3():
    op_str = "c dec -10 if a >= 1"
    op = r.Op.from_line(op_str)

    assert op.store_register == 'c'
    assert op.operation == r.Mnemonic.DEC
    assert op.change_value == -10
    assert op.compare_register == 'a'
    assert op.comparison is operator.ge
    assert op.compare_value == 1


def test_example_4():
    op_str = "c inc -20 if c == 10"
    op = r.Op.from_line(op_str)

    assert op.store_register == 'c'
    assert op.operation == r.Mnemonic.INC
    assert op.change_value == -20
    assert op.compare_register == 'c'
    assert op.comparison is operator.eq
    assert op.compare_value == 10



def test_ne():
    op_str = "c inc -20 if c != 10"
    op = r.Op.from_line(op_str)

    assert op.comparison is operator.ne


def test_le():
    op_str = "c inc -20 if c <= 10"
    op = r.Op.from_line(op_str)

    assert op.comparison is operator.le


def test_first_op() -> None:
    op = r.Op.from_line("b inc 5 if a > 1")
    vm = r.VM.load([])

    vm.step(op)
    assert vm.registers['b'] == 0


def test_second_op() -> None:
    op = r.Op.from_line("a inc 1 if b < 5")
    vm = r.VM.load([])

    vm.step(op)
    assert vm.registers['a'] == 1



def test_third_op() -> None:
    lines = [
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1"
    ]
    vm = r.VM.load(lines)

    vm.run()

    assert vm.registers['a'] == 1
    assert vm.registers['c'] == 10


def test_fourth_op() -> None:
    lines = [
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10"
    ]
    vm = r.VM.load(lines)

    vm.run()

    assert vm.registers['a'] == 1
    assert vm.registers['c'] == -10



def test_largest_register() -> None:
    lines = [
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10"
    ]
    vm = r.VM.load(lines)

    vm.run()

    register, value = vm.largest_register()
    register == 'a'
    value == 1

