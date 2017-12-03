#!/usr/bin/env python
# coding: utf-8
"""Day 2 of the advent of code challenges."""
import itertools
import typing as t

import click


# This is a bit awkward actually, but satisfies mypy.
# I actually want the type to be stricter just (int, int)!
TupleList = t.Iterator[t.Tuple[int, ...]]


class TooFewValuesInLine(ValueError):
    """Spreadsheet rows must have more than two lines to be valid."""
    pass


class NoDivisorsFound(ValueError):
    """No numbers in this row were evenly divisible."""
    pass


def line_to_numbers(line: str) -> t.List[int]:
    """Split a spreadsneet line into a list of numbers.

    raises:
      ValueError
    """
    return list(map(int, line.split()))


def spreadsheet_to_numbers(lines: t.Iterable[str]) -> t.List[t.List[int]]:
    """Text of spreadsheet to rows of numbers.

    raises:
      ValueError
    """
    return list(map(line_to_numbers, lines))


# ==== Part 1 ====
def diff_row_checksum(row: t.List[int]) -> int:
    """Calculate the first checksum of a spreadsheet row."""
    return max(row) - min(row)


def diff_checksum_of_rows(rows: t.List[t.List[int]]) -> int:
    """Checksum a spreadsheet's numeric rows."""
    return sum(map(diff_row_checksum, rows))


def difference_checksum(spreadsheet: t.IO[str]) -> int:
    """Checksum a spreadsheet file.

    raises:
      ValueError
    """
    rows = spreadsheet_to_numbers(spreadsheet.readlines())
    return diff_checksum_of_rows(rows)


# ==== Part 2 ====
def divisors(row: t.List[int]) -> t.Tuple[int, ...]:
    """Find the first evenly divisible pair in a spreadsheet row.

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
    """2nd checksum version of a row.

    Sum of evenly divisible pair in each row.

    raises:
      NoDivisorsFound
      TooFewValuesInLine
    """
    row_nums = map(divisors, rows)
    return sum(left // right for left, right in row_nums)


def divisor_checksum(spreadsheet: t.IO[str]) -> int:
    """Checksum a spreadsheet file with the even divisor pair method.

    raises:
      NoDivisorsFound
      TooFewValuesInLine
    """
    rows = spreadsheet_to_numbers(spreadsheet.readlines())
    return int(divisor_checksum_of_rows(rows))


@click.group()
def checksum() -> None:
    """Perform Santa's checksumming."""
    pass


@checksum.command()
@click.argument('spreadsheet', type=click.File())
def diff(spreadsheet: t.IO[str]) -> None:
    """Each row's minimum value is subtracted from its maximum."""
    click.echo(str(difference_checksum(spreadsheet)))


@checksum.command()
@click.argument('spreadsheet', type=click.File())
def div(spreadsheet: t.IO[str]) -> None:
    """Each row has one evenly divisible pair - each divided pair is summed."""
    click.echo(str(divisor_checksum(spreadsheet)))


def main() -> None:
    """Entrypoint."""
    checksum()


if __name__ == '__main__':
    main()
