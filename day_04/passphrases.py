#!/usr/bin/env python
# coding: utf-8
"""Day 4 Advent of Code problems.

Each line of our input file contains a pass phrase. For the phrase to be valid
it must contain no duplicate words. We count how many passphrases in the list
are valid.
"""
import collections
import typing as t

import click


CharCount = t.Tuple[t.Tuple[str, int], ...]


# ==== part 1
def valid_passphrase(passphrase: str) -> bool:
    """Find if there are no repeated words in this passphrase."""
    all_words = passphrase.split()
    return len(all_words) == len(set(all_words))


def valid_passphrases(passwd_lines: t.List[str]) -> t.List[str]:
    """Find only the valid passphrases in the passwd lines."""
    return list(filter(valid_passphrase, passwd_lines))


def count_valid_passphrases(passwd: t.IO[str]) -> int:
    """Count how many valid passphrases are in the file."""
    return len(valid_passphrases(passwd.readlines()))


# ==== part 2
def freeze(counter: collections.Counter) -> CharCount:
    """Turn a counter into a hashable representation."""
    # Oh well, not efficient - but hey ho.
    return tuple(sorted(counter.items()))


def frequency_counter(word: str) -> CharCount:
    return freeze(collections.Counter(word))


def extra_valid_passphrase(passphrase: str) -> bool:
    """Find if there are no repeated words, or anagrams in this passphrase."""
    all_words = list(map(frequency_counter, passphrase.split()))
    return len(all_words) == len(set(all_words))


def count_extra_valid_passphrases(passwd_lines: t.List[str]) -> int:
    """Find only the valid passphrases in the passwd lines."""
    return len(list(filter(extra_valid_passphrase, passwd_lines)))


@click.group()
def passphrases() -> None:
    """Work with Santa's passphrase list. How did we get it?"""
    pass


@passphrases.command()
@click.argument('passwd', type=click.File())
def count(passwd: t.IO[str]) -> None:
    """Each row contains space-deliminated words in a pass phrase."""
    click.echo(str(count_valid_passphrases(passwd)))


@passphrases.command()
@click.argument('passwd', type=click.File())
def count_paranoidly(passwd: t.IO[str]) -> None:
    """Each row contains space-deliminated words in a pass phrase."""
    click.echo(str(count_extra_valid_passphrases(passwd)))


def main() -> None:
    """Entrypoint"""
    passphrases()


if __name__ == '__main__':
    main()
