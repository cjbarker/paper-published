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


def test_extract_emails():
    assert not pp.extract_emails(None)
    assert not pp.extract_emails("")
    assert not pp.extract_emails(" ")
    assert not pp.extract_emails(" adsfljasdkl aslkjdf")
    result = pp.extract_emails(" adsfljasdkl aslkjdf")
    assert len(result) == 0
    result = pp.extract_emails(" adsfljasdkl bob@mail.com aslkjdf")
    assert len(result) == 1
    assert pp.extract_emails(
        " adsfljasdkl bob@mail.com aslkjdf asdlk me@mail.com asdfl;02"
    )
    result = pp.extract_emails(
        " adsfljasdkl bob@mail.com aslkjdf asdlk me@mail.com asdfl;02"
    )
    assert len(result) == 2
    assert "bob@mail.com" in result


def test_is_valid_email():
    assert not pp.is_valid_email(" ")
    assert not pp.is_valid_email("davea;")
    assert not pp.is_valid_email("davea;lkasd@")
    assert not pp.is_valid_email("davealkasd")
    assert not pp.is_valid_email("davealkasd@.")
    assert pp.is_valid_email("davealkasd@mail.com")


def test_valid_engine():
    assert not pp.is_valid_engine()
    assert not pp.is_valid_engine("   ")
    assert not pp.is_valid_engine("foo")
    assert pp.is_valid_engine("GooGle")
    assert pp.is_valid_engine("PmC")
    assert pp.is_valid_engine("all")


def test_get_page():
    good_url = "https://cjbarker.com"
    bad_url = "https://23423098uasbaker.com"
    assert pp.get_page(good_url)
    assert not pp.get_page(bad_url)
    assert not pp.get_page(None)
    assert not pp.get_page(
        "https://cjbarker.com/asdfasd"
    )  # should result in none w/ 404 error


def test_extract_xlsx():
    test_file = Path(TEST_DIR + "/test.xlsx")
    assert not pp.extract_xlsx(test_file)
    assert not pp.extract_xlsx(None, "foo")

    # empty list - keyerror
    result = pp.extract_xlsx(test_file, "First Name")
    with pytest.raises(Exception):
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
    with pytest.raises(Exception):
        assert not result[0]["First Name"]

    # extract multiple headers
    result = pp.extract_csv(test_file, ["First Name"])
    assert result[0]["First Name"] == "Jane"
    result = pp.extract_csv(test_file, ["First Name", "Last Name", "Age"])
    assert result[0]["First Name"] == "Jane"
    assert result[0]["Last Name"] == "Doe"
    assert result[0]["Age"] == "46"


def test_output_table(capsys):
    pp.output_table()
    out, err = capsys.readouterr()
    assert out == ""

    # load in and test output
    results = []
    result = {"First Name": "Jane", "Last Name": "Doe", "Age": "46"}
    results.append(result)
    pp.output_table(results)
    out, err = capsys.readouterr()
    assert "│ Jane │ Doe │ 46" in out


def test_google_search():
    search_term = "CJ Barker"
    assert not pp.google_search(None)
    results = pp.google_search(search_term)
    assert results
    found = False
    for result in results:
        if result["link"] == "https://cjbarker.com/":
            found = True
            break
    assert found


def test_pubmed_search():
    search_term = (
        "The Most Popular Smartphone Apps for Weight Loss: A Quality Assessment"
    )
    assert not pp.pubmed_search(None)
    results = pp.pubmed_search(search_term)
    assert results
    found_link = False
    found_authors = False
    for result in results:
        if result["link"] == "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4704947/":
            found_link = True
        if (
            result["page_authors"]
            == "Juliana Chen, Janet E Cade, Margaret Allman-Farinelli"
        ):
            found_authors = True
    assert found_link
    assert found_authors
