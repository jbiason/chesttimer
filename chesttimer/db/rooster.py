#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Character rooster management."""

# ChestTimer, an agenda creator for GW2 chests.
# Copyright (C) 2014 Julio Biason
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.ArithmeticError#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import json

from UserList import UserList

from enum import Enum


class Character(object):
    """Single character information."""

    class Professions(Enum):
        """Each profession a character can be."""
        engineer = 'Engineer'
        necromancer = 'Necromancer'
        thief = 'Thief'
        elementalist = 'Elementalist'
        warrior = 'Warrior'
        ranger = 'Ranger'
        mesmer = 'Mesmer'
        guardian = 'Guardian'

    class Races(Enum):
        """Each race."""
        asura = 'Asura'
        sylvari = 'Sylvari'
        human = 'Human'
        norn = 'Norn'
        charr = 'Charr'

    class Disciplines(Enum):
        """Crafting disciplines"""
        armorsmith = 'Armorsmith'
        artificer = 'Artificer'
        chef = 'Chef'
        huntsman = 'Huntsman'
        jeweler = 'Jeweler'
        leatherworker = 'Leatherworker'
        tailor = 'Tailor'
        weaponsmith = 'Weaponsmith'

    class Orders(Enum):
        """Each of the orders the character be can aligned to."""
        order_of_whispers = 'Order of Whispers'
        durmand_priori = 'Durmand Priori'
        vigil = 'Vigil'

    def __init__(self, name, level, race, profession, disciplines, order):
        """Create a character

        :param name: character name
        :type name: str
        :param level: character level
        :type level: int
        :param race: character race
        :type race: :py:class:`Races`
        :param profession: character profession
        :type profession: :py:class:`Professions`
        :param disciplines: crafting disciplines and levels
        :type disciplines: dict, :py:class:`Disciplines` as key, level as
                           value
        :param order: character order
        :type order: :py:class:`Orders`"""
        self.name = name
        self.level = level
        self.race = race
        self.profession = profession
        self.disciplines = disciplines
        self.order = order

    @classmethod
    def from_dict(self, data):
        return Character(data['name'],
                         data['level'],
                         Character.Races(data['race']),
                         Character.Professions(data['profession']),
                         dict([(Character.Disciplines(disc), level)
                               for (disc, level) in
                               data['disciplines'].iteritems()]),
                         Character.Orders(data['order']))

    @property
    def json(self):
        return {
            'name': self.name,
            'level': self.level,
            'race': self.race.value if self.race else None,
            'profession': self.profession.value if self.profession else None,
            'order': self.order.value if self.order else None,
            'disciplines': dict([(disc.value, level) for (disc, level) in
                                 self.disciplines.iteritems()])
        }


class Rooster(UserList):
    """List of characters."""

    def __init__(self):
        self.data = []
        return

    def load(self, path):
        """Load the list of characters from the storage."""
        filename = os.path.join(path, 'rooster.json')
        with file(filename, 'r') as content:
            for record in json.loads(content):
                self.data.append(Character.from_dict(record))
        return

    def save(self, path):
        """Save the current rooster list in the disk."""
        filename = os.path.join(path, 'rooster.json')
        result = []
        for char in self.data:
            result.append(char.json)
        with file(filename, 'w') as content:
            json.dump(result, content)
        return

    def add(self, character):
        """Add a new character to the list."""
        self.data.append(character)
        return
