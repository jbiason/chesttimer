#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the characters API."""

import os

from chesttimer.db.rooster import Rooster
from chesttimer.db.rooster import Character

from api_base import APITests


class APICharacterTest(APITests):
    def setUp(self):
        super(APICharacterTest, self).setUp()
        self._kill_db()
        self._demo_rooster()
        return

    def tearDown(self):
        super(APICharacterTest, self).tearDown()
        self._kill_db()
        return

    def test_index(self):
        """Get the list of characters."""
        rv = self.app.get('/api/characters/')
        group_list = [
            {
                "characters": [
                    {
                        "disciplines": None,
                        "level": 25,
                        "name": "Sgt Buzzkill",
                        "order": None,
                        "profession": "Warrior",
                        "race": "Human",
                        "sex": "Female",
                        "slug": "sgt_buzzkill"
                    }
                ],
                "group": 25
            },
            {
                "characters": [
                    {
                        "disciplines": {
                            "Armorsmith": 500,
                            "Weaponsmith": 415
                        },
                        "level": 80,
                        "name": "Thorianar",
                        "order": "Durmand Priori",
                        "profession": "Guardian",
                        "race": "Charr",
                        "sex": "Male",
                        "slug": "thorianar"
                    },
                    {
                        "disciplines": {
                            "Huntsman": 400,
                            "Leatherworker": 500
                        },
                        "level": 80,
                        "name": "Commander Buzzkill",
                        "order": "Durmand Priori",
                        "profession": "Engineer",
                        "race": "Charr",
                        "sex": "Male",
                        "slug": "commander_buzzkill"
                    }
                ],
                "group": 80
            }
        ]
        self.assertJSONOk(rv, groups=group_list)
        return

    def _demo_rooster(self):
        """Return a rooster with a couple of characters for group testing."""
        rooster = Rooster(self.DB)
        thorianar = Character('Thorianar', 80,
                              Character.Races.charr,
                              Character.Sex.male,
                              Character.Professions.guardian,
                              {Character.Disciplines.armorsmith: 500,
                               Character.Disciplines.weaponsmith: 415},
                              Character.Orders.durmand_priori)
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
        rooster.save()
        return

    def _kill_db(self):
        """Destroy the database."""
        if os.path.isfile(self.DB):
            os.remove(self.DB)
        return
