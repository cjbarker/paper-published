#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pp
import pytest
import sys

def test_is_valid_file():
    test_file = sys.argv[0]
    assert pp.is_valid_file("foo") is False
    assert pp.is_valid_file(test_file) is True

def test_get_page():
    good_url = "https://cjbarker.com"
    bad_url = "https://23423098uasbaker.com"
    assert pp.get_page(good_url)
    assert not pp.get_page(bad_url)
