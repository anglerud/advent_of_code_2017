#!/usr/bin/env python
# coding: utf-8
"""
"""
import collections
import enum
import operator
import typing as t

import attr
import click


class Mnemonic(enum.Enum):
    INC = 1
    DEC = 2


str_cmp = {
    '>': operator.gt,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '!=': operator.ne,
    '==': operator.eq
}


@attr.s
class Op(object):
    """ """
    store_register: str = attr.ib()
    operation: Mnemonic = attr.ib()
    change_value: int = attr.ib()
    compare_register: str = attr.ib()
    comparison: t.Callable[[int], bool] = attr.ib()
    compare_value: int = attr.ib()

    @classmethod
    def from_line(cls, line):
        """ """
        # Example: b inc 5 if a > 1
        (
            store_register,
            op_str,
            change_value_str,
            _,
            compare_register,
            compare_str,
            compare_value
        ) = line.strip().split()

        return Op(
            store_register=store_register,
            operation=Mnemonic.INC if op_str=='inc' else Mnemonic.DEC,
            change_value=int(change_value_str),
            compare_register=compare_register,
            comparison=str_cmp[compare_str],
            compare_value=int(compare_value)
        )


@attr.s
class VM(object):
    """ """
    registers: t.Dict[str, int] = attr.ib()
    program: t.List[Op] = attr.ib()
    max_value_held: int = attr.ib()

    @classmethod
    def load(cls, program: t.Iterable[str]):
        """ """
        return VM(
            registers=collections.defaultdict(int),
            program=map(Op.from_line, program),
            max_value_held=0
        )

    def step(self, op: Op) -> 'VM':
        """ """
        if op.comparison(self.registers[op.compare_register], op.compare_value):
            if op.operation == Mnemonic.INC:
                self.registers[op.store_register] += op.change_value
            else:
                self.registers[op.store_register] -= op.change_value

            self.max_value_held = max(self.registers[op.store_register],
                                      self.max_value_held)

        return self

    def run(self) -> 'VM':
        """ """
        for op in self.program:
            self.step(op)

        return self


    def largest_register(self) -> t.Tuple[str, int]:
        value, register = max((v, k) for k, v in self.registers.items())

        return register, value



@click.group()
def vm():
    """Run the register machine."""


@vm.command()
@click.argument('program', type=click.File())
def largest_register(program: t.IO[str]) -> None:
    vm = VM.load(program.readlines())
    vm.run()

    register, value = vm.largest_register()
    click.secho(f"The largest register is {register} containing {value}.",
                fg="green")


@vm.command()
@click.argument('program', type=click.File())
def max_value_held(program: t.IO[str]) -> None:
    vm = VM.load(program.readlines())
    vm.run()

    click.secho(f"The largest value held was {vm.max_value_held}",
                fg="green")


def main():
    """Entrypoint."""
    vm()


if __name__ == '__main__':
    main()
