#!/usr/bin/env python
# coding: utf-8
"""Seventh day of the Advent of Code - trees."""
import collections
import itertools
import operator
import queue
import re
import typing as t

import attr
import click


@attr.s
class Program(object):
    """A program balancing other programs. An acrobat."""
    name = attr.ib()  # str
    weight = attr.ib()  # int
    holds = attr.ib()  #  t.List[Program]

    def stack(self, program: 'Program') -> 'Program':
        """Start holding up another program."""
        self.holds.append(program)
        return self

    @property
    def total_weight(self: 'Program') -> int:
        """The weight of itself, and all programs it holds up."""
        weight = 0
        q = queue.Queue()
        q.put(self)

        while not q.empty():
            prog = q.get()
            weight += prog.weight

            for held in prog.holds:
                q.put(held)

        return weight

    @property
    def weight_of_children(self) -> int:
        """The weight of *just* the programs we hold up. """
        return sum(child.total_weight for child in self.holds)

    @property
    def balanced(self) -> bool:
        """Is this branch balanced?"""
        weights = list(map(operator.attrgetter('total_weight'), self.holds))
        if not weights:
            return True

        return max(weights) == min(weights)

    @classmethod
    def from_line(cls, line: str) -> 'Program':
        """Turn a string of input into a Program."""
        match = re.match(r"(?P<name>\w+) \((?P<weight>\d+)\)", line)
        if not match:
            raise ValueError(f"Not a line containing a program: {line}.")
        match_groups = match.groupdict()

        return Program(
            name=match_groups['name'],
            weight=int(match_groups['weight']),
            holds=[]
        )


def load(tree_file: t.IO[str]) -> Program:
    """Load the input data, parse it and construct the tree."""
    lines = tree_file.readlines()

    programs_by_name: t.Dict[str: Program] = {}

    # Start by just finding out whom everyone is
    programs = {p.name: p for p in map(Program.from_line, lines)}

    def is_holding_someone(line: str) -> bool:
        return '->' in line

    hold_lines = filter(is_holding_someone, lines)
    # Then find out who is holding whom
    for line in hold_lines:
        hold_str, holds_str = line.strip().split(' -> ', 1)
        holder = hold_str.split()[0]
        holdees = holds_str.split(', ')

        for holdee in holdees:
            programs[holder] = programs[holder].stack(programs[holdee])

    return programs


def find_bottom_of_tree(programs: t.Dict[str, Program]) -> Program:
    """Find the program holding up all the others."""
    programs_maybe_holding_others = programs.copy()
    for program in programs.values():
        for holdee in program.holds:
            programs_maybe_holding_others.pop(holdee.name)

    return list(programs_maybe_holding_others.values())[0]


def find_wrong_weight(program: Program) -> Program:
    """Find which program has been wronly added and what it should weigh."""
    by_weight = operator.attrgetter('total_weight')

    while True:
        # For the currently inspected program, inspect what it's holding
        # Group them by weight:
        groups = {}
        for weight, group in itertools.groupby(sorted(program.holds, key=by_weight), by_weight):
            group_list = list(group)
            groups[len(group_list)] = group_list

        # The branch that isn't balanced only has one entry in it:
        program = groups.pop(1)[0]
        _, balanced_programs = groups.popitem()

        # So, we now have which program is not balanced.
        # IF it itself has balanced children, we know this is the node we
        # want to reach.
        if program.balanced:
            # We return the imbalanced program and the weight it should have
            # been
            balanced_weight = balanced_programs[0].total_weight
            return program, balanced_weight - program.weight_of_children


@click.group()
def tree() -> None:
    """Find out about this tree of programs."""


@tree.command()
@click.argument('tree_file', type=click.File())
def bottom(tree_file: t.IO[str]) -> None:
    """Who is holding up this tree?"""
    programs = load(tree_file)
    bottom = find_bottom_of_tree(programs)

    click.secho(f"The program at the bottom is: {bottom.name}")


@tree.command()
@click.argument('tree_file', type=click.File())
def weight(tree_file: t.IO[str]) -> None:
    """Who is the wrong weight?"""
    programs = load(tree_file)
    bottom = find_bottom_of_tree(programs)
    program, weight = find_wrong_weight(bottom)

    click.echo(f"The program with the wrong weight is: {program.name}")
    click.secho(f"It should have been: {weight}")


def main() -> None:
    """Entrypoint."""
    tree()


if __name__ == '__main__':
    main()
