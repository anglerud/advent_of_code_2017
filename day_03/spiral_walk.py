#!/usr/bin/env python
# coding: utf-8
"""Day 3 of the Advent of Code puzzles.

Puzzles involving memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location
marked 1 and then counting up while spiraling outward.
"""
import typing as t

import attr
import click


@attr.s(frozen=True)
class Step(object):
    """A move, Right, Up, Left, Down."""
    x = attr.ib(attr.validators.instance_of(int))  # type: int
    y = attr.ib(attr.validators.instance_of(int))  # type: int


@attr.s(frozen=True)
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

Memory = t.Dict[Coordinate, int]


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


def neighbor_path() -> t.Iterable[Step]:
    """The path to walk once around our home base. """
    return (Right, Up, Left, Left, Down, Down, Right, Right)


def walk_neighborhood(location: Coordinate) -> t.Iterable[Coordinate]:
    """Take a walk around your own memory location."""
    for step in neighbor_path():
        location = location.move(step)
        yield location


def sum_neighborhood(memory: Memory, location: Coordinate) -> int:
    """Sum of all memory locations around """
    acc = 0

    for place in walk_neighborhood(location):
        acc += memory.get(place, 0)

    return acc


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
    """Walk the spiral until `position`"""
    steps_to_walk = position - 1
    return walk(steps_to_walk)


def sum_walk() -> t.Iterable[int]:
    """For each memory location, fill it with the sum of neighbor values.

    Return the value for each location we visit.
    """
    location = Coordinate(x=0, y=0)
    memory = {location: 1}  # Set up basic memory.

    for step in path():
        # Start moving
        location = location.move(step)
        # Sum around each location we're at.
        neighborhood_value = sum_neighborhood(memory, location)
        memory[location] = neighborhood_value

        yield neighborhood_value


def sum_bigger_than(puzzle_input) -> int:
    """Find the first memory contents larger than the `puzzle_input`."""
    for memory_value in sum_walk():
        if memory_value > puzzle_input:
            return memory_value


@click.group()
def spiral_walk() -> None:
    """Day 3 of the Advent of code puzzles."""
    pass


@spiral_walk.command()
@click.argument('position', type=int)
def pos(position: int) -> None:
    """Get the distance from the origin to memory location in `position`."""
    if position < 1:
        msg = "{} is not a position in memory!".format(position)
        click.secho(msg, fg='red')
        return

    location = walk_to(position)
    click.echo("Ended up at: {}".format(location))
    click.secho("Distance walked is: {}".format(location.distance), fg="green")


@spiral_walk.command()
@click.argument('value', type=int)
def sum(value: int) -> None:
    """Get the first value in a neighbor-sum walk larger than `value`."""
    if value < 1:
        msg = "Can't sum our memory values to less than one".format(value)
        click.secho(msg, fg='red')
        return

    first_larger_value = sum_bigger_than(value)
    msg = "First value larger than {} is: {}".format(value, first_larger_value)
    click.echo(msg)


def main() -> None:
    """Entrypoint."""
    spiral_walk()


if __name__ == '__main__':
    main()
