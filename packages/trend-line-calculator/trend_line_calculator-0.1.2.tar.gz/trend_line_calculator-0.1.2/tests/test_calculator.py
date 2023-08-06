#!/usr/bin/env python
# encoding: utf-8

import unittest
from trend_line_calculator import calculator


class TestCalculator(unittest.TestCase):
    def test_calculateSum(self):
        a = 1
        b = 2
        self.assertEqual(a + b, calculator.calculateSum(a, b))
