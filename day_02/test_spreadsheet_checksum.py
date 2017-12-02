"""
"""
import io

import spreadsheet_checksum as sc


test_data = """5 1 9 5
7 5 3
2 4 6 8"""

test_divisor_data = """5 9 2 8
9 4 7 3
3 8 6 5"""


def test_line_to_numbers() -> None:
    """ """
    assert sc.line_to_numbers("5 1 9 5") == [5, 1, 9, 5]


def test_spreadsheet_to_numbers() -> None:
    """ """
    rows = sc.spreadsheet_to_numbers(test_data.splitlines())
    assert rows == [[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]]


def test_single_line_checksum() -> None:
    """ """
    assert sc.diff_row_checksum([5, 1, 9, 5]) == 8
    assert sc.diff_row_checksum([7, 5, 3]) == 4
    assert sc.diff_row_checksum([2, 4, 6, 8]) == 6


def test_checksum_of_rows() -> None:
    """ """
    spreadsheet = [
        [5, 1, 9, 5],
        [7, 5, 3],
        [2, 4, 6, 8]
    ]
    assert sc.diff_checksum_of_rows(spreadsheet) == 18


def test_checksum() -> None:
    """ """
    assert sc.difference_checksum(io.StringIO(test_data)) == 18


def test_divisors() -> None:
    """ """
    spreadsheet = [
        [5, 9, 2, 8],
        [9, 4, 7, 3],
        [3, 8, 6, 5]
    ]
    expected_divisors = [(8, 2), (9, 3), (6, 3)]
    assert list(map(sc.divisors, spreadsheet)) == expected_divisors


def test_divisor_checksum() -> None:
    """ """
    spreadsheet = [
        [5, 9, 2, 8],
        [9, 4, 7, 3],
        [3, 8, 6, 5]
    ]
    assert sc.divisor_checksum_of_rows(spreadsheet) == 9


def test_file_divisor_checksum() -> None:
    """ """
    assert sc.divisor_checksum(io.StringIO(test_divisor_data)) == 9
