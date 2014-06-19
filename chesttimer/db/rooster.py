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

    class Sex(Enum):
        """Character sex."""
        male = 'Male'
        female = 'Female'

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

    def __init__(self, name, level, race, sex, profession, disciplines, order):
        """Create a character

        :param name: character name
        :type name: str
        :param level: character level
        :type level: int
        :param race: character race
        :type race: :py:class:`Races`
        :param sex: character sex
        :type sex: :py:class:`Sex`
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
        self.sex = sex
        self.profession = profession
        self.disciplines = disciplines
        self.order = order

    @classmethod
    def from_dict(self, data):
        disciplines = None
        if 'disciplines' in data and data['disciplines']:
            disciplines = dict([(Character.Disciplines(disc), level)
                                for (disc, level) in
                                data['disciplines'].iteritems()])

        order = None
        if 'order' in data and data['order']:
            order = Character.Orders(data['order'])

        return Character(data['name'],
                         data['level'],
                         Character.Races(data['race']),
                         Character.Sex(data['sex']),
                         Character.Professions(data['profession']),
                         disciplines,
                         order)

    @property
    def json(self):
        disciplines = None
        if self.disciplines:
            disciplines = dict([(disc.value, level) for (disc, level) in
                                self.disciplines.iteritems()])

        return {
            'name': self.name,
            'level': self.level,
            'race': self.race.value if self.race else None,
            'sex': self.sex.value if self.sex else None,
            'profession': self.profession.value if self.profession else None,
            'order': self.order.value if self.order else None,
            'disciplines': disciplines,
            'slug': self.slug
        }

    @property
    def slug(self):
        """Return a slugified version of the character name."""
        return self.name.replace(' ', '_').lower()


class Rooster(UserList):
    """List of characters."""

    class Fields(Enum):
        """Fields that can be used to order the fields."""
        level = 'level'
        race = 'race'
        profession = 'profession'
        order = 'order'
        discipline = 'discipline'

    def __init__(self, path=None):
        self.data = []
        self.path = path
        self.load()
        return

    def load(self):
        """Load the list of characters from the storage."""
        if not os.path.isfile(self.path):
            # first run?
            return

        with file(self.path, 'r') as content:
            for record in json.load(content):
                self.data.append(Character.from_dict(record))
        return

    def save(self):
        """Save the current rooster list in the disk."""
        result = []
        for char in self.data:
            result.append(char.json)

        with file(self.path, 'w') as content:
            json.dump(result, content)
        return

    def add(self, character):
        """Add a new character to the list."""
        self.data.append(character)
        return

    def group_by(self, field=Fields.level):
        """Return the list of characters in the rooster, grouped by a
        field."""
        if field == Rooster.Fields.discipline:
            # disciplines require a different ordering method, as a character
            # may appear in more than one discipline at the same time
            return self._group_by_discipline()

        # first, order the rooster by the field
        grouping = {}
        for record in self.data:
            key = getattr(record, field.value)
            if isinstance(key, Enum):
                key = key.value

            if key not in grouping:
                grouping[key] = {'group': key,
                                 'characters': []}

            grouping[key]['characters'].append(record.json)

        result = []
        for group_key in sorted(grouping.keys()):
            result.append(grouping[group_key])
        return result

    def remove(self, character):
        """Remove a character from the rooster.

        :param character: the character to be removed
        :type character: str (either name or slug) or :py:class:`Character`"""
        to_delete = None
        for (pos, elem) in enumerate(self.data):
            if isinstance(character, basestring):
                if elem.name == character or elem.slug == character:
                    to_delete = pos
                    break

            if isinstance(character, Character):
                if elem == character:
                    to_delete = pos
                    break

        if to_delete is not None:
            del self.data[pos]
        return

    def _group_by_discipline(self):
        """Return the rooster ordered by discipline."""
        grouping = {}
        for record in self.data:
            if not record.disciplines or not record.disciplines.keys():
                disciplines = [None]
            else:
                disciplines = record.disciplines.keys()
                disciplines = [disc.value for disc in disciplines]

            for disc in disciplines:
                if disc not in grouping:
                    grouping[disc] = {'group': disc,
                                      'characters': []}
                grouping[disc]['characters'].append(record.json)

        result = []
        for group_key in sorted(grouping.keys()):
            result.append(grouping[group_key])
        return result
