#!/usr/bin/env python
# coding: utf-8
"""
"""
import itertools
import typing as t

import attr
import click


@attr.s
class Step(object):
    """A move, Right, Up, Left, Down."""
    x = attr.ib(attr.validators.instance_of(int))  # type: int
    y = attr.ib(attr.validators.instance_of(int))  # type: int


@attr.s
class Coordinate(object):
    """Cartesian coordinate - (x, y)."""
    x = attr.ib(attr.validators.instance_of(int))
    y = attr.ib(attr.validators.instance_of(int))

    def move(self, step: Step):
        """Take a step, land on a new Coordinate."""
        return attr.evolve(self, x=self.x + step.x, y=self.y + step.y)

    @property
    def distance(self):
        return abs(self.x) + abs(self.y)


Right = Step(x=1, y=0)
Up = Step(x=0, y=1)
Left = Step(x=-1, y=0)
Down = Step(x=0, y=-1)


def path() -> t.Iterable[Step]:
    """Generate the movements of the memory spiral.

    Each spiral is two movements - for example, if we start at position 1:
    1
    the first part of the spiral is created by the moves Right, Up::
       3
    1  2
    Then if we add the second movement: Left, Left, Down, Down:
    5 4 3
    6 1 2
    7
    To create the next Spiral We add two of each type of step to each corner.
    The first spiral is thus RU+LLDD
    The second spiral is then: RRRUUU+LLLLDDDD
    """
    # Starting position
    first_corner = [Right, Up]
    second_corner = [Left, Left, Down, Down]

    # Yield spiral movement
    while True:
        for movement in first_corner:
            yield movement
        for movement in second_corner:
            yield movement

        # Generate next set of movements.
        first_corner = [Right, Right] + first_corner + [Up, Up]
        second_corner = [Left, Left] + second_corner + [Down, Down]



def walk(steps: int) -> Coordinate:
    """Start at Coordinate(x=0, y=0), then take `steps` spiral movements."""
    location = Coordinate(x=0, y=0)
    if steps == 0:
        return location

    for step_count, step in enumerate(path(), start=1):
        location = location.move(step)

        if step_count >= steps:
            return location


def walk_to(position: int) -> Coordinate:
    """ """
    steps_to_walk = position - 1
    return walk(steps_to_walk)


@click.group()
def spiral_walk() -> None:
    pass


@spiral_walk.command()
@click.argument('position', type=int)
def pos(position: int):
    if position < 1:
        msg = "{} is not a position in memory!".format(position)
        click.secho(msg, fg='red')
        return

    location = walk_to(position)
    click.echo("Ended up at: {}".format(location))
    click.secho("Distance walked is: {}".format(location.distance), fg="green")


def main() -> None:
    """Entrypoint."""
    spiral_walk()


if __name__ == '__main__':
    main()
