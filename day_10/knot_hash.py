#!/usr/bin/env python
# coding=utf-8
"""Advent of code, day 10.
"""
import typing as t

import attr
import click


@attr.s
class KnotHash(object):
    """ """
    current_position: int = attr.ib()
    skip_length: int = attr.ib()
    string: str = attr.ib()

    @classmethod
    def new(cls, string: str):
        """ """
        return KnotHash(
            current_position=0,
            skip_length=0,
            string=string
        )

    @property
    def current_value(self):
        return self.string[self.current_position]


    @property
    def checksum(self):
        return self.string[0] * self.string[1]


    def tie(self, length: int):
        """ """
        string = self.string[:]
        string_len = len(string)

        start_pos = self.current_position
        end_pos = self.current_position + length

        def wrap(n):
            return n % string_len

        # Find the segment to reverse
        forward_range = list(map(wrap, range(start_pos, end_pos)))
        reverse_range = list(reversed(forward_range))

        # Reverse the segment
        for i, j in zip(forward_range, reverse_range):
            string[i] = self.string[j]
            
        return attr.evolve(self,
            current_position=wrap(self.current_position + length + self.skip_length),
            skip_length=self.skip_length + 1,
            string=string
        )


def pinch_lengths(knot_lengths: t.IO[str]) -> t.Iterable[int]:
    """Get the pinch lengths to apply from our input."""
    return map(int, knot_lengths.read().strip().split(','))


def elf_hash(knotter: KnotHash, knot_lengths: t.Iterable[int]) -> KnotHash:
    for length in knot_lengths:
        knotter = knotter.tie(length)

    return knotter


@click.group()
def knot_hash():
    """Start pinching some string."""


@knot_hash.command()
@click.argument('knot_lengths', type=click.File())
def knot(knot_lengths: t.IO[str]) -> None:
    knotter = KnotHash.new(list(range(256)))
    knotter = elf_hash(knotter, pinch_lengths(knot_lengths))

    click.secho(f"The elf checksum is {knotter.checksum}")


def main():
    """Entrypoint."""
    knot_hash()


if __name__ == '__main__':
    main()
