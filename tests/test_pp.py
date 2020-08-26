#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pp
import pytest
import sys

def test_is_valid_file():
    test_file = sys.argv[0]
    assert pp.is_valid_file("foo") is False
    assert pp.is_valid_file(test_file) is True

