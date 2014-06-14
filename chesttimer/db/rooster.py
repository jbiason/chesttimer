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
from UserDict import UserDict


class Character(UserDict):
    """Single character information."""

    def __init__(self, name, level, profession, discipline, discipline_level,
                 order):
        super(Character, self).__init__()
        self['name'] = name
        self['level'] = level
        self['profession'] = profession
        self['discipline'] = discipline
        self['discipline_level'] = discipline_level
        self['order'] = order

    @classmethod
    def from_dict(self, data):
        return Character(data['name'],
                         data['level'],
                         data['profession'],
                         data['discipline'],
                         data['discipline_level'],
                         data['order'])


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
        with file(filename, 'w') as content:
            json.dumps(content)
        return

    def add(self, character):
        """Add a new character to the list."""
        self.data.append(character)
        return
