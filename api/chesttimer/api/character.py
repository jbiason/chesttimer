#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""API for managing characters."""

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

from flask import jsonify
from flask import current_app
from flask import request

from flask_classy import FlaskView

from flask_cors import cross_origin

from ..db.rooster import Character
from ..db.rooster import Rooster


class CharacterView(FlaskView):

    """API for characters."""

    def __init__(self):
        """Class instanciation."""
        return

    # pylint:disable=no-self-use
    @cross_origin(headers=['Content-Type'])
    def index(self):
        """Return the list of characters in the rooster."""
        rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
        order = request.values.get('order', 'level')
        char_list = rooster.group_by(Rooster.Fields[order])
        return jsonify(status='OK',
                       groups=char_list)

    @cross_origin(headers=['Content-Type'])
    def post(self):
        """Create a new character."""
        rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
        character = self._from_form()
        rooster.add(character)
        rooster.save()
        return jsonify(status='OK')

    @cross_origin(headers=['Content-Type'])
    def get(self, slug):
        """Return the information of a character."""
        if request.values.get('method') == 'DELETE':
            return self.delete(slug)

        rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
        pos = rooster.find(slug)
        if pos is None:
            return jsonify(status='ERROR')

        return jsonify(status='OK',
                       character=rooster.data[pos].json)

    # def patch(self, slug)

    @cross_origin(headers=['Content-Type'])
    def put(self, slug):
        """Update a character information."""
        rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
        rooster.remove(slug)
        rooster.add(self._from_form())
        rooster.save()
        return jsonify(status='OK')

    @cross_origin(headers=['Content-Type'])
    def delete(self, slug):
        """Delete a character."""
        rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
        rooster.remove(slug)
        rooster.save()
        return jsonify(status='OK')

    # pylint:disable=no-self-use
    def _from_form(self):
        """Return a Character object from the request form."""
        json = request.get_json()
        form = request.values
        if json:
            form = json
        name = form.get('name')
        level = int(form.get('level'))
        race = Character.Races[form.get('race')]
        sex = Character.Sex[form.get('sex')]
        profession = Character.Professions[form.get('profession')]

        disciplines = {}
        discipline1 = form.get('discipline1')
        if discipline1:
            discipline1_level = int(form.get('discipline1_level'))
            disciplines[Character.Disciplines[discipline1]] = discipline1_level

        discipline2 = form.get('discipline2')
        if discipline2:
            discipline2_level = int(form.get('discipline2_level'))
            disciplines[Character.Disciplines[discipline2]] = discipline2_level

        order = None
        order_value = form.get('order')
        if order_value:
            order = Character.Orders[order_value]

        return Character(name, level, race, sex, profession, disciplines,
                         order)
