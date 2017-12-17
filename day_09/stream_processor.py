#!/usr/bin/env python
# coding: utf-8
"""Advent of code, day 8.
"""
import enum
import functools
import operator
import typing as t

import attr
import click


class Token(enum.Enum):
    START_GROUP = 1
    END_GROUP = 2
    SEPARATOR = 3
    START_GARBAGE = 4
    END_GARBAGE = 5
    ESCAPE = 6
    CHARACTER = 7


special_bytes = {
    r'{': Token.START_GROUP,
    r'}': Token.END_GROUP,
    r',': Token.SEPARATOR,
    r'<': Token.START_GARBAGE,
    r'>': Token.END_GARBAGE,
    r'!': Token.ESCAPE
}


def tokenize(stream: t.Iterable[str]) -> t.Iterable[Token]:
    """ """
    return (special_bytes.get(c, Token.CHARACTER) for c in stream)


def strip_garbage_contents(token_stream: t.Iterable[Token]) -> t.Iterable[Token]:
    """ """
    in_garbage = False
    in_escape = False

    for token in token_stream:
        if in_escape:
            # Just skip one token if we're being escaped.
            in_escape = False
        elif token is Token.ESCAPE:
            # If starting an escape just set our escape-status.
            in_escape = True
        elif not in_garbage and token is Token.START_GARBAGE:
            in_garbage = True
            yield token
        elif in_garbage and token is Token.END_GARBAGE:
            in_garbage = False
            yield token
        elif in_garbage:
            # Gargbage token discarded.
            pass
        else:
            # Token we care about - yield it.
            yield token


def count_groups(stream: t.Iterable[str]) -> int:
    """ """
    token_stream = tokenize(stream)
    stripped_token_stream = strip_garbage_contents(token_stream)

    is_group_end = functools.partial(operator.eq, Token.END_GROUP)
    group_end_tokens = filter(is_group_end, stripped_token_stream)

    return sum(1 for group_end_token in group_end_tokens)


def score_stream(token_stream: t.Iterable[Token]) -> int:
    """ """
    is_group_start = functools.partial(operator.eq, Token.START_GROUP)
    is_group_end = functools.partial(operator.eq, Token.END_GROUP)

    current_score = 0
    for token in token_stream:
        if is_group_start(token):
            current_score += 1
            yield current_score
        elif is_group_end(token):
            # We only count new groups, so we don't yield a score here. 
            current_score -= 1


def score_groups(stream: t.Iterable[str]) -> int:
    """ """
    token_stream = tokenize(stream)
    stripped_token_stream = strip_garbage_contents(token_stream)

    return sum(score_stream(stripped_token_stream))


@click.group()
def stream_processor():
    """Run the stream processor."""


@stream_processor.command()
@click.argument('stream', type=click.File())
def score(stream: t.IO[str]) -> None:
    # So, not quite a stream... but hey ;)
    score = score_groups(stream.read())

    click.secho(f"Score of stream is: {score}", fg="green")


def main():
    """Entrypoint."""
    stream_processor()


if __name__ == '__main__':
    main()
