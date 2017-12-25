#!/usr/bin/env python
# coding=utf-8
"""Advent of code, day 10.
"""
import functools
import operator
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


def byte_pinch_lengths(knot_lengths: t.IO[str]) -> t.List[int]:
    """Get the pinch lengths to apply from our input."""
    return list(map(ord, knot_lengths.read().strip())) + [17, 31, 73, 47, 23]


def elf_hash(knotter: KnotHash, knot_lengths: t.Iterable[int]) -> KnotHash:
    for length in knot_lengths:
        knotter = knotter.tie(length)

    return knotter


def elf_sparse_hash(knotter: KnotHash, knot_lengths: t.Iterable[int]) -> KnotHash:
    """ """
    for _ in range(64):
        knotter = elf_hash(knotter, knot_lengths)

    return knotter


def dense_hash_blocks(knotter: KnotHash) -> t.Iterable[int]:
    string = knotter.string
    while string:
        chunk, string = string[:16], string[16:]

        yield functools.reduce(operator.xor, chunk)


def elf_dense_hash(knotter: KnotHash) -> str:
    """ """
    def hex_pad(num: int) -> str:
        return hex(num)[2:].zfill(2)

    return ''.join(map(hex_pad, dense_hash_blocks(knotter)))


def rudolph_santa_advent_hash(knot_lengths: t.IO[str]) -> str:
    knotter = KnotHash.new(list(range(256)))
    knotter = elf_sparse_hash(knotter, byte_pinch_lengths(knot_lengths))

    return elf_dense_hash(knotter)


@click.group()
def knot_hash():
    """Start pinching some string."""


@knot_hash.command()
@click.argument('knot_lengths', type=click.File())
def knot(knot_lengths: t.IO[str]) -> None:
    knotter = KnotHash.new(list(range(256)))
    knotter = elf_hash(knotter, pinch_lengths(knot_lengths))

    click.secho(f"The elf checksum is {knotter.checksum}")


@knot_hash.command()
@click.argument('knot_lengths', type=click.File())
def knot_64(knot_lengths: t.IO[str]) -> None:
    hash_str = rudolph_santa_advent_hash(knot_lengths)

    click.secho(f"The elf hash string is {hash_str}")


def main():
    """Entrypoint."""
    knot_hash()


if __name__ == '__main__':
    main()
