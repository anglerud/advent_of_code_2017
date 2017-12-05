#!/usr/bin/env python
# coding: utf-8
"""Tests for day 4 of the advent of code."""
import io

import passphrases

passwd_file = """correct horse battery shore
correct horse staple horse
"""


def test_valid_passphrase() -> None:
    """Contains no repeated words."""
    phrase = "correct horse battery staple"
    assert passphrases.valid_passphrase(phrase) is True


def test_invalid_passphrase() -> None:
    """Contains repeated words."""
    phrase = "correct horse staple horse"
    assert passphrases.valid_passphrase(phrase) is False


def test_valid_passphrases() -> None:
    """Filter our invalid passphrases."""
    good = "correct horse battery staple"
    bad = "correct horse staple horse"
    phrases = [good, bad]
    assert passphrases.valid_passphrases(phrases) == [good]


def test_count_valid_passphrases() -> None:
    """Count quantity of good passphrases."""
    passwd = io.StringIO(passwd_file)
    assert passphrases.count_valid_passphrases(passwd) == 1


def test_extra_valid_passphrase() -> None:
    """Contains no repeated words, or anagrams."""
    phrase = "correct horse battery staple"
    assert passphrases.extra_valid_passphrase(phrase) is True


def test_extra_invalid_passphrase() -> None:
    """Contains an anagram."""
    phrase = "correct horse battery shore"
    assert passphrases.extra_valid_passphrase(phrase) is False


def test_count_extra_valid_passphrases() -> None:
    """Count quantity of good passphrases."""
    passwd = io.StringIO(passwd_file)
    assert passphrases.count_extra_valid_passphrases(passwd) == 0

