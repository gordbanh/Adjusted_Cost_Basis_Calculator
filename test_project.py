# Unit tests for project.py
# Import libraries
from project import csv_to_dict, pivot_acc, print_xlsx, add_space
import pytest
import sys
import pandas as pd
# Although openpyxl was not explicitly used, it was an engine in pd.to_excel
import openpyxl
import argparse
from functools import partial
import re


def test_csv_to_dict_df():
    # Test valid inputs to csv_to_dict returns a dataframe
    assert isinstance(csv_to_dict("Dummy.csv"), pd.DataFrame)


def test_csv_to_dict_exist():
    # Test if csv's exist
    with pytest.raises(SystemExit):
        csv_to_dict("123.csv")
        csv_to_dict("Not_exist.csv")


def test_csv_to_dict_type():
    # Tests invalid filetype
    with pytest.raises(SystemExit):
        csv_to_dict("123")
        csv_to_dict("123.csv.txt")
        csv_to_dict("123.txt")


def test_csv_to_dict_empty():
    # Test empty inputs to csv_to_dict
    with pytest.raises(SystemExit):
        # Empty Keys
        csv_to_dict("Empty.csv")


def test_csv_to_dict_wrong():
    # Test wrong key inputs to csv_to_dict
    with pytest.raises(SystemExit):
        # Empty Keys
        csv_to_dict("Wrong.csv")


def test_pivot_acc_df():
    # Test valid inputs to csv_to_dict returns a dataframe
    assert isinstance(pivot_acc(csv_to_dict("Dummy.csv")), pd.DataFrame)


def test_pivot_acc_str():
    # Test wrong value inputs to pivot
    with pytest.raises(SystemExit):
        # Not an int
        pivot_acc(csv_to_dict("Wrong2.csv"))
