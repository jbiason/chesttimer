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

    def test_group_by_level(self):
        """Request the list of characters grouped by level."""
        rooster = Rooster(self.DB)
        thorianar = Character('Thorianar', 80,
                              Character.Races.charr,
                              Character.Professions.guardian,
                              {Character.Disciplines.armorsmith: 500,
                               Character.Disciplines.weaponsmith: 415},
                              Character.Orders.durmand_priori)
        buzzkill = Character('Commander Buzzkill', 80,
                             Character.Races.charr,
                             Character.Professions.engineer,
                             {Character.Disciplines.leatherworker: 500,
                              Character.Disciplines.huntsman: 400},
                             Character.Orders.durmand_priori)
        sgt_buzzkill = Character('Sgt Buzzkill', 25,
                                 Character.Races.human,
                                 Character.Professions.warrior,
                                 {},
                                 None)
        rooster.add(thorianar)
        rooster.add(buzzkill)
        rooster.add(sgt_buzzkill)

        levels = rooster.group_by(Rooster.Fields.level)
        self.assertEqual(len(levels), 2)    # 2 groups, 80 & 25
        self.assertEqual(levels[0]['group'], 25)    # first group is 25
        self.assertEqual(levels[1]['group'], 80)    # second group is 80
        self.assertEqual(len(levels[0]['values']), 1)   # only sgt
        self.assertEqual(len(levels[1]['values']), 2)   # thor & buzz
        return

    def _kill_db(self):
        """Destroy the database."""
        if os.path.isfile(self.DB):
            os.remove(self.DB)
        return

if __name__ == '__main__':
    unittest.main()
