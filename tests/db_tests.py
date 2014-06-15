#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the 'database'."""

import os
import unittest

from chesttimer.db.rooster import Rooster
from chesttimer.db.rooster import Character


class RoosterTest(unittest.TestCase):
    DB = './rooster.json'

    def setUp(self):
        super(RoosterTest, self).setUp()
        self._kill_db()
        return

    def tearDown(self):
        super(RoosterTest, self).tearDown()
        self._kill_db()
        return

    def test_add(self):
        """Add a new character to the rooster."""
        char = Character('test', 80,
                         Character.Races.charr,
                         Character.Professions.guardian,
                         {}, None)
        rooster = Rooster(self.DB)
        rooster.add(char)
        self.assertEqual(len(rooster), 1)
        return

    def test_save_load(self):
        """Test if saving the rooster actually saves the file."""
        char = Character('test', 80,
                         Character.Races.charr,
                         Character.Professions.guardian,
                         {Character.Disciplines.armorsmith: 500,
                          Character.Disciplines.weaponsmith: 415},
                         Character.Orders.durmand_priori)
        rooster = Rooster(self.DB)
        rooster.add(char)

        rooster.save()
        self.assertTrue(os.path.isfile(self.DB))

        # try to load it back
        new_rooster = Rooster(self.DB)

        self.assertEqual(len(new_rooster), 1)
        self.assertEqual(new_rooster[0].name, 'test')
        return

    def _kill_db(self):
        """Destroy the database."""
        if os.path.isfile(self.DB):
            os.remove(self.DB)
        return

if __name__ == '__main__':
    unittest.main()
