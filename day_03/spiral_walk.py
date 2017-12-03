#!/usr/bin/env python
# coding: utf-8
"""
"""
import typing as t

import attr
import click


@attr.s
class Coordinate(object):
    """Cartesian coordinate - (x, y)."""
    x = attr.ib(attr.validators.instance_of(int))
    y = attr.ib(attr.validators.instance_of(int))


def index_to_coord(index: int) -> Coordinate:
    """ """
    return Coordinate(0, 0)


@click.group()
def spiral_walk() -> None:
    pass


@spiral_walk.command()
@click.argument('position', type=int)
def pos(position: int):
    click.echo(str(position))


def main() -> None:
    """Entrypoint."""
    spiral_walk()


if __name__ == '__main__':
    main()
