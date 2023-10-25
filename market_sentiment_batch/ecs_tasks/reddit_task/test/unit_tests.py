import pytest
from unittest.mock import patch, Mock
from reddit_utils import clean_comment


def test_clean_comment():
    """
    test if clean_comment function removes special characters and numbers
    """
    input_text = "@user /u/someone [removed] This is a sample reddit comment http://testurl.com [deleted] with special chars & numbers 12345."
    expected_output = "this is a sample reddit comment with special chars numbers"

    assert clean_comment(input_text) == expected_output


def test_clean_comment_empty():
    """
    test if clean_comment function returns empty string when input is empty
    """
    input_text = ""
    expected_output = ""

    assert clean_comment(input_text) == expected_output


def test_clean_comment_none():
    """
    test if clean_comment function returns empty string when input is None
    """
    input_text = None
    expected_output = ""

    assert clean_comment(input_text) == expected_output


def test_clean_comment_numbers():
    """
    test if clean_comment function removes numbers
    """
    input_text = "12345"
    expected_output = ""

    assert clean_comment(input_text) == expected_output


def test_clean_comment_special_chars():
    """
    test if clean_comment function removes special characters
    """
    input_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    expected_output = ""

    assert clean_comment(input_text) == expected_output


def test_clean_comment_normal_text():
    """
    test if clean_comment function returns same text when input is normal text
    """
    input_text = "This is a sample reddit comment without any special chars or numbers."
    expected_output = (
        "this is a sample reddit comment without any special chars or numbers"
    )

    assert clean_comment(input_text) == expected_output
