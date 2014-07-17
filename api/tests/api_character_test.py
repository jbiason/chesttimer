#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the characters API."""

import os
import json

# pylint:disable=import-error
from chesttimer.db.rooster import Rooster
from chesttimer.db.rooster import Character

from api_base import APITests


# pylint:disable=fixme
# pylint:disable=too-many-public-methods
class APICharacterTest(APITests):

    """Tests for the characters API."""

    def setUp(self):
        """Set up the tests.

        Destroys the database (if it exists) and creating a new rooster.
        """
        super(APICharacterTest, self).setUp()
        self._kill_db()
        self._demo_rooster()
        return

    def tearDown(self):
        """Tear down the tests by destroying the database."""
        super(APICharacterTest, self).tearDown()
        self._kill_db()
        return

    def test_index(self):
        """Get the list of characters."""
        response = self.app.get('/api/characters/')
        group_list = [
            {
                "characters": [
                    {
                        "disciplines": None,
                        "level": 25,
                        "name": "Sgt Buzzkill",
                        "order": None,
                        "profession": "warrior",
                        "race": "human",
                        "sex": "female",
                        "slug": "sgt_buzzkill"
                    }
                ],
                "group": 25
            },
            {
                "characters": [
                    {
                        "disciplines": {
                            "armorsmith": 500,
                            "weaponsmith": 415
                        },
                        "level": 80,
                        "name": "Thorianar",
                        "order": "durmand_priori",
                        "profession": "guardian",
                        "race": "charr",
                        "sex": "male",
                        "slug": "thorianar"
                    },
                    {
                        "disciplines": {
                            "huntsman": 400,
                            "leatherworker": 500
                        },
                        "level": 80,
                        "name": "Commander Buzzkill",
                        "order": "durmand_priori",
                        "profession": "engineer",
                        "race": "charr",
                        "sex": "male",
                        "slug": "commander_buzzkill"
                    }
                ],
                "group": 80
            }
        ]
        self.assertJSONOk(response, groups=group_list)
        return

    def test_create(self):
        """Create a new character."""
        request = {'name': 'new character',
                   'level': 70,
                   'race': 'norn',
                   'sex': 'male',
                   'profession': 'engineer',
                   'discipline1': None,
                   'discipline2': None,
                   'order': None}
        response = self.app.post('/api/characters/',
                                 data=request)
        self.assertJSONOk(response)

        # check the rooster file.
        rooster = Rooster(self.ROOSTER)
        for character in rooster.data:
            if character.slug == 'new_character':
                return

        self.fail('character is not in the list')
        return

    def test_update(self):
        """Update a character information."""
        request = {'name': 'the new thorianar',
                   'level': 40,
                   'race': 'norn',
                   'sex': 'female',
                   'profession': 'warrior',
                   'discipline1': None,
                   'discipline2': None,
                   'order': None}
        response = self.app.put('/api/characters/thorianar',
                                data=request)
        self.assertJSONOk(response)

        # check the rooster file.
        rooster = Rooster(self.ROOSTER)
        for character in rooster.data:
            if character.slug == 'thorianar':
                self.fail('old character still exists')

            if character.slug == 'the_new_thorianar':
                self.assertEqual(character.name, request['name'])
                self.assertEqual(character.level, request['level'])
                self.assertEqual(character.race.name, request['race'])
                self.assertEqual(character.sex.name, request['sex'])
                self.assertEqual(character.profession.name,
                                 request['profession'])
                self.assertEqual(character.order, request['order'])
                return
        self.fail('character was completely removed')
        return

    def test_update_json(self):
        """Update a character using JSON request."""
        request = {'name': 'the new thorianar',
                   'level': 40,
                   'race': 'norn',
                   'sex': 'female',
                   'profession': 'warrior',
                   'discipline1': 'chef',
                   'discipline1_level': 400,
                   'discipline2': 'artificer',
                   'discipline2_level': 120,
                   'order': 'vigil'}
        response = self.app.put('/api/characters/thorianar',
                                data=json.dumps(request),
                                content_type='application/json')
        self.assertJSONOk(response)

        # check the rooster file.
        rooster = Rooster(self.ROOSTER)
        for character in rooster.data:
            if character.slug == 'thorianar':
                self.fail('old character still exists')

            if character.slug == 'the_new_thorianar':
                self.assertEqual(character.name, request['name'])
                self.assertEqual(character.level, request['level'])
                self.assertEqual(character.race.name, request['race'])
                self.assertEqual(character.sex.name, request['sex'])
                self.assertEqual(character.profession.name,
                                 request['profession'])
                self.assertEqual(character.order.name, request['order'])
                return
        self.fail('character was completely removed')
        return

    def test_update_not_found(self):
        """Update a character that doesn't exist."""
        request = {'name': 'the new thorianar',
                   'level': 40,
                   'race': 'norn',
                   'sex': 'female',
                   'profession': 'warrior',
                   'discipline1': None,
                   'discipline2': None,
                   'order': None}
        response = self.app.put('/api/characters/test',
                                data=request)
        self.assertEqual(response.status_code, 404)
        return

    def test_delete(self):
        """Delete a character."""
        response = self.app.delete('/api/characters/thorianar')
        self.assertJSONOk(response)

        # check the rooster file
        rooster = Rooster(self.ROOSTER)
        for character in rooster.data:
            if character.slug == 'thorianar':
                self.fail('old character still exists')
        return

    def test_delete_get(self):
        """Delete a character using GET."""
        response = self.app.get('/api/characters/thorianar?method=DELETE')
        self.assertJSONOk(response)

        # check the rooster file
        rooster = Rooster(self.ROOSTER)
        for character in rooster.data:
            if character.slug == 'thorianar':
                self.fail('old character still exists')
        return

    def test_delete_not_found(self):
        """Delete a character that doesn't exist."""
        response = self.app.delete('/api/characters/test')
        self.assertEqual(response.status_code, 404)
        return

    def test_get(self):
        """Try to get information about a single character."""
        response = self.app.get('/api/characters/thorianar')
        character = {'disciplines': {'armorsmith': 500,
                                     'weaponsmith': 415},
                     'level': 80,
                     'name': 'Thorianar',
                     'order': 'durmand_priori',
                     'profession': 'guardian',
                     'race': 'charr',
                     'sex': 'male',
                     'slug': 'thorianar'}
        self.assertJSONOk(response, character=character)
        return

    def test_get_not_found(self):
        """Get information of a character that doesn't exist."""
        response = self.app.get('/api/characters/test')
        self.assertEqual(response.status_code, 404)
        return

    def test_name_too_long(self):
        """Create a new character with a name too long."""
        request = {'name': 'this name is too long to continue',
                   'level': 70,
                   'race': 'norn',
                   'sex': 'male',
                   'profession': 'engineer',
                   'discipline1': None,
                   'discipline2': None,
                   'order': None}
        response = self.app.post('/api/characters/',
                                 data=request)
        # self.assertEqual(response.status_code, 400)
        self.assertJSONError(response, 'CharacterNameTooLong')
        return

    def _demo_rooster(self):
        """Return a rooster with a couple of characters for group testing."""
        rooster = Rooster(self.ROOSTER)
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
        if os.path.isfile(self.ROOSTER):
            os.remove(self.ROOSTER)
        return
