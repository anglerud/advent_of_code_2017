#!/usr/bin/env python
# coding: utf-8

"""
1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and the third digit (2) matches the fourth digit.
1111 produces 4 because each digit (all 1) matches the next.
1234 produces 0 because no digit matches the next.
91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
"""


def test_easy():
    # 1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and the third digit (2) matches the fourth digit.
    input_data = 1122
    expected = 3

def test_all_same():
    # 1111 produces 4 because each digit (all 1) matches the next.
    input_data = 1111
    expected = 4

def test_no_pairs():
    # 1234 produces 0 because no digit matches the next.
    input_data = 1234
    expected = 0

def test_wraparound():
    # 91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
    input_data = 91212129 
    expected = 9

