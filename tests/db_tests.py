#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the 'database'."""

import os
import unittest

from chesttimer.db.rooster import Rooster
from chesttimer.db.rooster import Character


class RoosterTest(unittest.TestCase):
    def setUp(self):
        super(RoosterTest, self).setUp()
        return

    def tearDown(self):
        super(RoosterTest, self).tearDown()
        return

    def test_add(self):
        """Add a new character to the rooster."""
        char = Character('test', 80,
                         Character.Races.charr,
                         Character.Professions.guardian,
                         {}, None)
        rooster = Rooster()
        rooster.add(char)
        self.assertEqual(len(rooster), 1)
        return

    def test_save_load(self):
        """Test if saving the rooster actually saves the file."""
        char = Character('test', 80,
                         Character.Races.charr,
                         Character.Professions.guardian,
                         {}, None)
        rooster = Rooster()
        rooster.add(char)

        rooster.save('.')
        self.assertTrue(os.path.isfile('./rooster.json'))
        return

if __name__ == '__main__':
    unittest.main()
