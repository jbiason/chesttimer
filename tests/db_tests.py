#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the 'database'."""

from chesttimer.db.rooster import Rooster
from chesttimer.db.rooster import Character

import unittest


class RoosterTest(unittest.TestCase):
    def setUp(self):
        super(RoosterTest, self).setUp()
        return

    def tearDown(self):
        super(RoosterTest, self).tearDown()
        return

    def test_add(self):
        """Add a new character to the rooster."""
        char = Character('test', 80, Character.Profession.guardian,
                         {}, None)
        rooster = Rooster()
        rooster.add(char)


if __name__ == '__main__':
    unittest.main()
