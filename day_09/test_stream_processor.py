# coding: utf-8
"""
"""
import pytest

import stream_processor as sp
from stream_processor import Token as tk


TOKEN_EXAMPLES = (
    (r'<', [tk.START_GARBAGE]),
    (r'>', [tk.END_GARBAGE]),
    (r'c', [tk.CHARACTER]),
    (r'!c', [tk.ESCAPE, tk.CHARACTER]),
    (r'{c', [tk.START_GROUP, tk.CHARACTER]),
    (r'}', [tk.END_GROUP]),
    (r',', [tk.SEPARATOR]),
)

ALL_GARBAGE = (
    r'<>',
    r'<random characters>',
    r'<<<<>',
    r'<{!>}>',
    r'<!!>',
    r'<!!!>>',
    r'<{o"i!a,<{i<a>',
)

GROUPS = (
    (r'{}', 1),
    (r'{{{}}}', 3),
    (r'{{},{}}', 3),
    (r'{{{},{},{{}}}}', 6),
    (r'{<{},{},{{}}>}', 1),
    (r'{<a>,<a>,<a>,<a>}', 1),
    (r'{{<a>},{<a>},{<a>},{<a>}}', 5),
    (r'{{<!>},{<!>},{<!>},{<a>}}', 2)
)

GROUPS_SCORE = (
    (r'{}', 1),
    (r'{{{}}}', 6),
    (r'{{},{}}', 5),
    (r'{{{},{},{{}}}}', 16),
    (r'{<a>,<a>,<a>,<a>}', 1),
    (r'{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    (r'{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    (r'{{<a!>},{<a!>},{<a!>},{<ab>}}', 3)
)


@pytest.mark.parametrize("test_input,expected", TOKEN_EXAMPLES)
def test_parser(test_input, expected):
    """Test that we tokenize individual characters OK."""
    tokens = list(sp.tokenize(test_input))
    assert tokens == expected


@pytest.mark.parametrize("test_input", ALL_GARBAGE)
def test_all_garbage_naive(test_input):
    """Just verifies that there are barbage book-ends."""
    tokens = list(sp.tokenize(test_input))
    assert tokens[0] is tk.START_GARBAGE
    assert tokens[-1] is tk.END_GARBAGE


def test_small_naive_token_stream():
    """Test a small stream tokenizes OK."""
    tokens = list(sp.tokenize('{<abc>}'))
    assert tokens == [
        tk.START_GROUP,
        tk.START_GARBAGE,
        tk.CHARACTER,
        tk.CHARACTER,
        tk.CHARACTER,
        tk.END_GARBAGE,
        tk.END_GROUP
    ]


@pytest.mark.parametrize("test_input", ALL_GARBAGE)
def test_all_garbage(test_input):
    """Verifies that garbage is properly stripped out.

    NOTE: garbage start and end tokens are still emitted.
    """
    tokens = list(sp.strip_garbage_contents(sp.tokenize(test_input)))
    assert tokens == [tk.START_GARBAGE, tk.END_GARBAGE]


@pytest.mark.parametrize("test_input,expected", GROUPS)
def test_count_groups(test_input, expected):
    """Tests that we can count groups"""
    token_count = sp.count_groups(test_input)
    assert token_count == expected


@pytest.mark.parametrize("test_input,expected", GROUPS_SCORE)
def test_score_groups(test_input, expected):
    """Tests that we can give scores to the groups"""
    score = sp.score_groups(test_input)
    assert score == expected
