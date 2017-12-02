#!/usr/bin/env python
# coding: utf-8
"""
"""
import itertools
import typing as t

import click


# This is a bit awkward actually, but satisfies mypy.
# I actually want the type to be stricter just (int, int)!
TupleList = t.Iterator[t.Tuple[int, ...]]


class TooFewValuesInLine(ValueError):
    """ """
    pass


class NoDivisorsFound(ValueError):
    """ """
    pass


def line_to_numbers(line: str) -> t.List[int]:
    """

    raises:
      ValueError
    """
    return list(map(int, line.split()))


def spreadsheet_to_numbers(lines: t.Iterable[str]) -> t.List[t.List[int]]:
    """

    raises:
      ValueError
    """
    return list(map(line_to_numbers, lines))


# ==== Part 1 ====
def diff_row_checksum(row: t.List[int]) -> int:
    """
    """
    return max(row) - min(row)


def diff_checksum_of_rows(rows: t.List[t.List[int]]) -> int:
    """
    """
    return sum(map(diff_row_checksum, rows))


def difference_checksum(spreadsheet: t.IO[str]) -> int:
    """

    raises:
      ValueError
    """
    rows = spreadsheet_to_numbers(spreadsheet.readlines())
    return diff_checksum_of_rows(rows)


# ==== Part 2 ====
def divisors(row: t.List[int]) -> t.Tuple[int, ...]:
    """

    raises:
      NoDivisorsFound
      TooFewValuesInLine
    """
    if len(row) < 2:
        raise TooFewValuesInLine("Must have two numbers at least in a row.")

    # This type is definitely (t.Tuple[int, int]) -> bool, but mypy...
    def divides_evenly(pair: t.Tuple[int, ...]) -> t.Any:
        left, right = pair
        return left % right == 0

    possible_divisors = itertools.permutations(row, 2)  # type: TupleList
    divisors = list(filter(divides_evenly, possible_divisors))
    if not divisors:
        raise NoDivisorsFound("No evenly dividable numbers in the line.")

    return divisors[0]


def divisor_checksum_of_rows(rows: t.List[t.List[int]]) -> int:
    """

    raises:
      NoDivisorsFound
      TooFewValuesInLine
    """
    row_nums = map(divisors, rows)
    return int(sum(left / right for left, right in row_nums))


def divisor_checksum(spreadsheet: t.IO[str]) -> int:
    """

    raises:
      NoDivisorsFound
      TooFewValuesInLine
    """
    rows = spreadsheet_to_numbers(spreadsheet.readlines())
    return int(divisor_checksum_of_rows(rows))


@click.group()
def checksum() -> None:
    """ """
    pass


@checksum.command()
@click.argument('spreadsheet', type=click.File())
def diff(spreadsheet: t.IO[str]) -> None:
    """ """
    click.echo(str(difference_checksum(spreadsheet)))


@checksum.command()
@click.argument('spreadsheet', type=click.File())
def div(spreadsheet: t.IO[str]) -> None:
    """ """
    click.echo(str(divisor_checksum(spreadsheet)))


def main() -> None:
    """Entrypoint."""
    checksum()


if __name__ == '__main__':
    main()
