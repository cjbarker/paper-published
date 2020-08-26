#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pathlib import Path

import pp
import pytest
import sys
import os

def test_is_valid_file():
    test_file = sys.argv[0]
    assert pp.is_valid_file("foo") is False
    assert pp.is_valid_file(test_file) is True

def test_get_page():
    good_url = "https://cjbarker.com"
    bad_url = "https://23423098uasbaker.com"
    assert pp.get_page(good_url)
    assert not pp.get_page(bad_url)

def test_pubmed_search():
    # TODO
    pass

def test_google_search():
    # TODO
    pass

def test_extract_xlsx():
    test_file = Path(os.getcwd() + "/test.xlsx")
    assert not pp.extract_xlsx(test_file)
    assert not pp.extract_xlsx(None, "foo")

    # empty list - keyerror
    result = pp.extract_xlsx(test_file, "First Name")
    with pytest.raises(Exception) as e:
        assert not result[0]['First Name']

    # extract multiple headers
    result = pp.extract_xlsx(test_file, ["First Name"])
    assert result[0]['First Name'] == 'Jane'
    result = pp.extract_xlsx(test_file, ["First Name", "Last Name", "Age"])
    assert result[0]['First Name'] == 'Jane'
    assert result[0]['Last Name'] == 'Doe'
    assert result[0]['Age'] == 46

def test_extract_csv():
    test_file = Path(os.getcwd() + "/test.csv")
    assert not pp.extract_csv(test_file)
    assert not pp.extract_csv(None, "foo")

    # empty list - keyerror
    result = pp.extract_csv(test_file, "First Name")
    with pytest.raises(Exception) as e:
        assert not result[0]['First Name']

    # extract multiple headers
    result = pp.extract_csv(test_file, ["First Name"])
    assert result[0]['First Name'] == 'Jane'
    result = pp.extract_csv(test_file, ["First Name", "Last Name", "Age"])
    assert result[0]['First Name'] == 'Jane'
    assert result[0]['Last Name'] == 'Doe'
    assert result[0]['Age'] == '46'
