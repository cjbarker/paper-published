#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os.path import abspath
from os.path import dirname as d
from pathlib import Path

import pytest

import pp

# Load in root dir to system path for easy access
ROOT_DIR = d(d(abspath(__file__)))
sys.path.append(ROOT_DIR)

if ROOT_DIR.endswith("tests"):
    TEST_DIR = str(ROOT_DIR)
else:
    TEST_DIR = str(Path(ROOT_DIR + "/tests"))


def test_is_valid_file():
    test_file = sys.argv[0]
    assert pp.is_valid_file("foo") is False
    assert pp.is_valid_file(test_file) is True


def test_get_page():
    good_url = "https://cjbarker.com"
    bad_url = "https://23423098uasbaker.com"
    assert pp.get_page(good_url)
    assert not pp.get_page(bad_url)


def test_extract_xlsx():
    test_file = Path(TEST_DIR + "/test.xlsx")
    assert not pp.extract_xlsx(test_file)
    assert not pp.extract_xlsx(None, "foo")

    # empty list - keyerror
    result = pp.extract_xlsx(test_file, "First Name")
    with pytest.raises(Exception) as e:  # noqa F841
        assert not result[0]["First Name"]
    # extract multiple headers
    result = pp.extract_xlsx(test_file, ["First Name"])
    assert result[0]["First Name"] == "Jane"
    result = pp.extract_xlsx(test_file, ["First Name", "Last Name", "Age"])
    assert result[0]["First Name"] == "Jane"
    assert result[0]["Last Name"] == "Doe"
    assert result[0]["Age"] == 46


def test_extract_csv():
    test_file = Path(TEST_DIR + "/test.csv")
    assert not pp.extract_csv(test_file)
    assert not pp.extract_csv(None, "foo")

    # empty list - keyerror
    result = pp.extract_csv(test_file, "First Name")
    with pytest.raises(Exception) as e:  # noqa F841
        assert not result[0]["First Name"]

    # extract multiple headers
    result = pp.extract_csv(test_file, ["First Name"])
    assert result[0]["First Name"] == "Jane"
    result = pp.extract_csv(test_file, ["First Name", "Last Name", "Age"])
    assert result[0]["First Name"] == "Jane"
    assert result[0]["Last Name"] == "Doe"
    assert result[0]["Age"] == "46"


def test_pubmed_search():
    pass


def test_google_search():
    search_term = "CJ Barker"
    results = pp.google_search(search_term)
    assert results
    found = False
    for result in results:
        print(result)
        if result["link"] == "https://cjbarker.com/":
            found = True
            break
    assert found
