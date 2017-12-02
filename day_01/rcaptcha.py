#!/usr/bin/env python
# coding: utf-8
"""First and second problems in the Advent of Code, day 1.

Turn a number into a list of digits, check if each number matches the one N
steps ahead. Take the sum of the ones that do.

```bash
Usage: rcaptcha.py [OPTIONS] COMMAND [ARGS]...
  Calculate a checksum of your input numbers.
Options:
  --help  Show this message and exit.
Commands:
  next      With your input as a circular list of...
  opposite  With your input as a circular list of...
```

To get the answers for the two problems:

```bash
$ ./rcaptcha.py next $(cat input)
$ ./rcaptcha.py opposite $(cat input)
```
"""
import itertools
import operator
import typing as t

import click


head = operator.itemgetter(0)


def _pair_is_equal(digit_pair: t.Tuple[int, int]) -> bool:
    """Check if a pair of digits match."""
    return digit_pair[0] == digit_pair[1]


def _wrap_list(shift: int, digits: t.Iterable[int]) -> t.List[int]:
    """Wrap a list around `shift` steps.

    Example: shift [1, 2, 3] by 1 -> [2, 3, 1]
    """
    digits = list(digits)
    return digits[shift:] + digits[:shift]


def split_into_digits(input_value: int) -> t.List[int]:
    """Turn a number into a list of the inidividial digits it contains."""
    digit_characters = str(input_value)
    return list(map(int, digit_characters))


def checksum(steps_ahead: int, input_value: int) -> int:
    """Santa-checksum.

    Sum the numbers which match values `steps_ahead` ahead in the list of input
    digits.

    raises:
      ValueError: if input is negative.
    """
    if input_value < 0:
        raise ValueError("Can't checksum a negative value.")

    digits = split_into_digits(input_value)
    if len(digits) <= 1:
        return 0

    # Example for matches one ahead:
    # steps_ahead: 1, digits = [1, 2, 3, 1] -> wrapped_digits: [2, 3, 1, 1] ->
    # digit_pairs: [(1, 2), (2, 3), (3, 1), (1, 1)] ->
    # matching_digit_pairs: [(1, 1)] -> return value: 1
    wrapped_digits = _wrap_list(steps_ahead, digits)
    digit_pairs = zip(itertools.cycle(digits), wrapped_digits)
    matching_digit_pairs = filter(_pair_is_equal, digit_pairs)

    return sum(map(head, matching_digit_pairs))


def checksum_next(input_value: int) -> int:
    """Run the checksum with values one step ahead in the list of digits.

    raises:
      ValueError: if input is negative
    """
    return checksum(1, input_value)


def checksum_opposite(input_value: int) -> int:
    """Run the checksum with values halfway ahead in the list of digits.

    raises:
      ValueError: if input is negative
    """
    return checksum(len(str(input_value)) // 2, input_value)


@click.group()
def rcaptcha() -> None:
    """Calculate a checksum of your input numbers."""
    pass


@rcaptcha.command()
@click.argument('number', type=int)
def next(number) -> None:
    """Santa-checksum - one step ahead.

    With your input as a circular list of numbers, sum matching values one step
    ahead.
    """
    click.echo(str(checksum_next(number)))


@rcaptcha.command()
@click.argument('number', type=int)
def opposite(number) -> None:
    """Santa-checkum - halfway round the list.

    With your input as a circular list of numbers, sum matching values half way
    ahead.
    """
    click.echo(str(checksum_opposite(number)))


if __name__ == '__main__':
    rcaptcha()
