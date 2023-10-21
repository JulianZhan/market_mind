import pytest
from unittest.mock import patch, Mock
from reddit_utils import clean_comment


def test_clean_comment():
    # Define the test case
    input_text = "@user /u/someone [removed] This is a sample reddit comment http://testurl.com [deleted] with special chars & numbers 12345."
    expected_output = "this is a sample reddit comment with special chars numbers"

    # Assert the result
    assert clean_comment(input_text) == expected_output


def test_clean_comment_empty():
    # Define the test case
    input_text = ""
    expected_output = ""

    # Assert the result
    assert clean_comment(input_text) == expected_output


def test_clean_comment_none():
    # Define the test case
    input_text = None
    expected_output = ""

    # Assert the result
    assert clean_comment(input_text) == expected_output


def test_clean_comment_numbers():
    # Define the test case
    input_text = "12345"
    expected_output = ""

    # Assert the result
    assert clean_comment(input_text) == expected_output


def test_clean_comment_special_chars():
    # Define the test case
    input_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    expected_output = ""

    # Assert the result
    assert clean_comment(input_text) == expected_output


def test_clean_comment_normal_text():
    # Define the test case
    input_text = "This is a sample reddit comment without any special chars or numbers."
    expected_output = (
        "this is a sample reddit comment without any special chars or numbers"
    )
    # Assert the result
    assert clean_comment(input_text) == expected_output
