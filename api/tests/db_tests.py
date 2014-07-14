#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the 'database'."""

import os
import unittest

# pylint:disable=import-error
from chesttimer.db.rooster import Rooster
from chesttimer.db.rooster import Character


# pylint:disable=too-many-public-methods
class RoosterTest(unittest.TestCase):

    """Tests for the rooster/database."""

    ROOSTER = './rooster.json'

    def setUp(self):
        """Set up the global database.

        Just make sure the database doesn't exist.
        """
        super(RoosterTest, self).setUp()
        self._kill_db()
        return

    def tearDown(self):
        """Tear down the global database."""
        super(RoosterTest, self).tearDown()
        self._kill_db()
        return

    def test_add(self):
        """Add a new character to the rooster."""
        char = Character('test', 80,
                         Character.Races.charr,
                         Character.Sex.male,
                         Character.Professions.guardian,
                         {}, None)
        rooster = Rooster(self.ROOSTER)
        rooster.add(char)
        self.assertEqual(len(rooster), 1)
        return

    def test_save_load(self):
        """Test if saving the rooster actually saves the file."""
        char = Character('test', 80,
                         Character.Races.charr,
                         Character.Sex.male,
                         Character.Professions.guardian,
                         {Character.Disciplines.armorsmith: 500,
                          Character.Disciplines.weaponsmith: 415},
                         Character.Orders.durmand_priori)
        rooster = Rooster(self.ROOSTER)
        rooster.add(char)

        rooster.save()
        self.assertTrue(os.path.isfile(self.ROOSTER))

        # try to load it back
        new_rooster = Rooster(self.ROOSTER)

        self.assertEqual(len(new_rooster), 1)
        self.assertEqual(new_rooster[0].name, 'test')
        return

    def test_group_by_level(self):
        """Request the list of characters grouped by level."""
        rooster = self._demo_rooster()
        levels = rooster.group_by(Rooster.Fields.level)
        self.assertEqual(len(levels), 2)    # 2 groups, 80 & 25
        self.assertEqual(levels[0]['group'], 25)    # first group is 25
        self.assertEqual(levels[1]['group'], 80)    # second group is 80
        self.assertEqual(len(levels[0]['characters']), 1)   # only sgt
        self.assertEqual(len(levels[1]['characters']), 2)   # thor & buzz
        return

    def test_group_by_race(self):
        """Request the list of characters grouped by race."""
        rooster = self._demo_rooster()
        races = rooster.group_by(Rooster.Fields.race)
        self.assertEqual(len(races), 2)     # humans and charr
        return

    def test_group_by_profession(self):
        """Request the list of characters grouped by profession."""
        rooster = self._demo_rooster()
        professions = rooster.group_by(Rooster.Fields.profession)
        self.assertEqual(len(professions), 3)    # guard, warr and engi
        return

    def test_group_by_order(self):
        """Request the lsit of characters grouped by order."""
        rooster = self._demo_rooster()
        orders = rooster.group_by(Rooster.Fields.order)
        self.assertEqual(len(orders), 2)    # priori & none
        return

    def test_group_by_discipline(self):
        """Request the list of characters grouped by discipline."""
        rooster = self._demo_rooster()
        disciplines = rooster.group_by(Rooster.Fields.discipline)
        # hunts, armor, weapon, leather & None
        self.assertEqual(len(disciplines), 5)
        return

    def test_find_slug(self):
        """Find a character by slug."""
        rooster = self._demo_rooster()
        self.assertEqual(0, rooster.find('thorianar'))
        return

    def test_find_full_character(self):
        """Find a character position by full charaacter info."""
        rooster = self._demo_rooster()
        self.assertEqual(0, rooster.find(self._thorianar()))
        return

    def test_remove_slug(self):
        """Remove a character by slug."""
        rooster = self._demo_rooster()
        rooster.remove('thorianar')
        self.assertIsNone(rooster.find('thorianar'))
        return

    def test_remove_character(self):
        """Remove a character by character object."""
        rooster = self._demo_rooster()
        rooster.remove(self._thorianar())
        self.assertIsNone(rooster.find(self._thorianar()))
        return

    def _kill_db(self):
        """Destroy the database."""
        if os.path.isfile(self.ROOSTER):
            os.remove(self.ROOSTER)
        return

    # pylint:disable=no-self-use
    def _thorianar(self):
        """Return the test character "Thorianar"."""
        return Character('Thorianar', 80,
                         Character.Races.charr,
                         Character.Sex.male,
                         Character.Professions.guardian,
                         {Character.Disciplines.armorsmith: 500,
                          Character.Disciplines.weaponsmith: 415},
                         Character.Orders.durmand_priori)

    def _demo_rooster(self):
        """Return a rooster with a couple of characters for group testing."""
        rooster = Rooster(self.ROOSTER)
        thorianar = self._thorianar()
        buzzkill = Character('Commander Buzzkill', 80,
                             Character.Races.charr,
                             Character.Sex.male,
                             Character.Professions.engineer,
                             {Character.Disciplines.leatherworker: 500,
                              Character.Disciplines.huntsman: 400},
                             Character.Orders.durmand_priori)
        sgt_buzzkill = Character('Sgt Buzzkill', 25,
                                 Character.Races.human,
                                 Character.Sex.female,
                                 Character.Professions.warrior,
                                 {},
                                 None)
        rooster.add(thorianar)
        rooster.add(buzzkill)
        rooster.add(sgt_buzzkill)
        return rooster

if __name__ == '__main__':
    unittest.main()
