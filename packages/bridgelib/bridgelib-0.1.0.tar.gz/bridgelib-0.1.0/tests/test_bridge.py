#!/usr/bin/env python
# encoding: utf-8

import unittest
from bridgelib import bridge


class TestCalculator(unittest.TestCase):
    def test_calculateSum(self):
        a = 1
        b = 2
        self.assertEqual(a + b, bridge.add(a, b))
