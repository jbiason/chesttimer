#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Character rooster management."""

# ChestTimer, an agenda creator for GW2 chests.
# Copyright (C) 2014 Julio Biason
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
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

    # pylint:disable=too-few-public-methods
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

    # pylint:disable=too-few-public-methods
    class Sex(Enum):

        """Character sex."""

        male = 'Male'
        female = 'Female'

    # pylint:disable=too-few-public-methods
    class Races(Enum):

        """Each race."""

        asura = 'Asura'
        sylvari = 'Sylvari'
        human = 'Human'
        norn = 'Norn'
        charr = 'Charr'

    # pylint:disable=too-few-public-methods
    class Disciplines(Enum):

        """Crafting disciplines."""

        armorsmith = 'Armorsmith'
        artificer = 'Artificer'
        chef = 'Chef'
        huntsman = 'Huntsman'
        jeweler = 'Jeweler'
        leatherworker = 'Leatherworker'
        tailor = 'Tailor'
        weaponsmith = 'Weaponsmith'

    # pylint:disable=too-few-public-methods
    class Orders(Enum):

        """Each of the orders the character be can aligned to."""

        order_of_whispers = 'Order of Whispers'
        durmand_priori = 'Durmand Priori'
        vigil = 'Vigil'

    # pylint:disable=too-many-arguments
    def __init__(self, name, level, race, sex, profession, disciplines, order):
        """Create a character.

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
        :type order: :py:class:`Orders`
        """
        self.name = name
        self.level = level
        self.race = race
        self.sex = sex
        self.profession = profession
        self.disciplines = disciplines
        self.order = order

    @classmethod
    def from_dict(cls, data):
        """Convert a JSON to a character.

        :param data: The character data
        :type data: dict

        :return: A character
        :rtype: :py:class:`Character`
        """
        disciplines = None
        if 'disciplines' in data and data['disciplines']:
            disciplines = dict([(Character.Disciplines[disc], level)
                                for (disc, level) in
                                data['disciplines'].iteritems()])

        order = None
        if 'order' in data and data['order']:
            order = Character.Orders[data['order']]

        return Character(data['name'],
                         data['level'],
                         Character.Races[data['race']],
                         Character.Sex[data['sex']],
                         Character.Professions[data['profession']],
                         disciplines,
                         order)

    @property
    def json(self):
        """Return a JSON representation of the character.

        :return: The character
        :rtype: dict
        """
        disciplines = None
        if self.disciplines:
            disciplines = dict([(disc.name, level) for (disc, level) in
                                self.disciplines.iteritems()])

        return {
            'name': self.name,
            'level': self.level,
            'race': self.race.name if self.race else None,
            'sex': self.sex.name if self.sex else None,
            'profession': self.profession.name if self.profession else None,
            'order': self.order.name if self.order else None,
            'disciplines': disciplines,
            'slug': self.slug
        }

    @property
    def slug(self):
        """Return a slugified version of the character name.

        :return: slug
        :rtype: str
        """
        return self.name.replace(' ', '_').lower()

    def __eq__(self, other):
        """Compare this character to another character."""
        return self.json == other.json


class Rooster(UserList):

    """List of characters."""

    # pylint:disable=too-few-public-methods
    class Fields(Enum):

        """Fields that can be used to order the fields."""

        level = 'level'
        race = 'race'
        profession = 'profession'
        order = 'order'
        discipline = 'discipline'

    def __init__(self, path=None):
        """Start the rooster from the database.

        :param path: The full path for the rooster database.
        :type path: str
        """
        super(Rooster, self).__init__()
        self.data = []
        self.path = path
        self.load()
        return

    def load(self):
        """Load the list of characters from the storage."""
        if not os.path.isfile(self.path):
            # first run?
            return

        with open(self.path, 'r') as content:
            for record in json.load(content):
                self.data.append(Character.from_dict(record))
        return

    def save(self):
        """Save the current rooster list in the disk."""
        result = []
        for char in self.data:
            result.append(char.json)

        with open(self.path, 'w') as content:
            json.dump(result, content)
        return

    def add(self, character):
        """Add a new character to the list.

        :param character: The new character
        :type: :py:class:`Character`
        """
        self.data.append(character)
        return

    def group_by(self, field=Fields.level):
        """Return the list of characters in the rooster, grouped by a field.

        :param field: The field that must be used to group characters.
        :type field: :py:class:`Fields`

        :return: The characters grouped by the field
        :rtype: list
        """
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

    def find(self, character):
        """Search for a character and return its position in the rooster.

        :param character: the character to be removed
        :type character: str (either name or slug) or :py:class:`Character`

        :return: the position in the data where the character is
        :rtype: int or None
        """
        for (pos, elem) in enumerate(self.data):
            if isinstance(character, basestring):
                if elem.name == character or elem.slug == character:
                    return pos

            if isinstance(character, Character):
                if elem == character:
                    return pos
        return None

    def remove(self, character):
        """Remove a character from the rooster.

        :param character: the character to be removed
        :type character: str (either name or slug) or :py:class:`Character`
        """
        to_delete = None
        pos = None
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
