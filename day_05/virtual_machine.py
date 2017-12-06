#!/usr/bin/env python
# coding: utf-8
"""
"""
import typing as t

import attr
import click


class SegFault(IndexError):
    """Jump with a program counter pointing to an invalid location."""


@attr.s
class Machine(object):
    memory = attr.ib()  # type: t.List[int]
    program_counter = attr.ib()  # type: int
    instruction_count = attr.ib()  # type: int

    # Advanced architecture,
    # if the offset to jump is three or more, decrease origin by 1.
    # Otherwise, increase it by 1
    # The regular Rovaniemi architecture always increases by 1.
    von_santa_machine = attr.ib(default=False)  # type: bool

    @property
    def in_bounds(self):
        return 0 <= self.program_counter < len(self.memory)

    @property
    def peek(self):
        try:
            return self.memory[self.program_counter]
        except IndexError as err:
            msg = f"Invalid memory location: {self.program_counter}."
            raise SegFault(msg)

    @classmethod
    def load(cls, program, von_santa_machine=False):
        return Machine(
            memory=program,
            program_counter=0,
            instruction_count=0,
            von_santa_machine=von_santa_machine
        )

    def step(self):
        try:
            jmp_offset = self.memory[self.program_counter]
            if self.von_santa_machine:
                self.memory[self.program_counter] += -1 if jmp_offset >= 3 else 1
            else:
                self.memory[self.program_counter] += 1

            self.program_counter += jmp_offset
            self.instruction_count += 1
        except IndexError as err:
            msg = f"Invalid jump from location {self.program_counter}."
            raise SegFault(msg)

        return self


def read_program(program: t.IO[str]) -> t.List[int]:
    return list(map(int, program.readlines()))


def run_program(program: t.IO[str], von_santa=False) -> int:
    """ """
    memory = read_program(program)
    machine = Machine.load(memory, von_santa_machine=von_santa)

    while machine.in_bounds:
        machine.step()

    return machine.instruction_count


@click.group()
def virtual_machine():
    """Virtual machine """


@virtual_machine.command()
@click.argument('program', type=click.File())
def run(program: t.IO[str]) -> None:
    """Run a program """
    instructions_to_escape = run_program(program)
    msg = "It took {} instructions to escape.".format(instructions_to_escape)
    click.secho(msg, fg='green')


@virtual_machine.command()
@click.argument('program', type=click.File())
def von_santa(program: t.IO[str]) -> None:
    """Run a program on a von Santa machine. Careful now."""
    instructions_to_escape = run_program(program, von_santa=True)
    msg = "It took {} instructions to escape.".format(instructions_to_escape)
    click.secho(msg, fg='green')


def main():
    virtual_machine()


if __name__ == '__main__':
    main()
