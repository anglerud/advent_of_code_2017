#!/usr/bin/env python
# coding: utf-8
"""Tests for day 1 of the advent of code."""
import pytest

import rcaptcha


def test_easy_one_ahead():
    """1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the
    second digit and the third digit (2) matches the fourth digit.
    """
    assert rcaptcha.checksum_next(1122) == 3


def test_all_same_one_ahead():
    """1111 produces 4 because each digit (all 1) matches the next."""
    assert rcaptcha.checksum_next(1111) == 4


def test_no_pairs_one_ahead():
    """1234 produces 0 because no digit matches the next."""
    assert rcaptcha.checksum_next(1234) == 0


def test_wraparound_one_ahead():
    """ 91212129 produces 9 because the only digit that matches the next one is
    the last digit, 9."""
    assert rcaptcha.checksum_next(91212129) == 9


def test_easy_halfway_ahead():
    """1212 produces 6: the list contains 4 items, and all four digits match
    the digit 2 items ahead."""
    assert rcaptcha.checksum_opposite(1212) == 6


def test_easy_not_matching_halfway_ahead():
    """1221 produces 0, because every comparison is between a 1 and a 2."""
    assert rcaptcha.checksum_opposite(1221) == 0


def test_one_match_halfway_ahead():
    """123425 produces 4, because both 2s match each other, but no other digit
    has a match."""
    assert rcaptcha.checksum_opposite(123425) == 4


def test_all_match_halfway_ahead():
    """123123 produces 12."""
    assert rcaptcha.checksum_opposite(123123) == 12


def test_every_second_matches():
    """12131415 produces 4."""
    assert rcaptcha.checksum_opposite(12131415) == 4
