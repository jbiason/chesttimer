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


from flask import Blueprint
from flask import render_template
from flask import current_app
from flask import request
from flask import jsonify

from ..db.rooster import Rooster
from ..db.rooster import Character

characters = Blueprint('characters', __name__)


@characters.route('/', methods=['GET'])
def index():
    rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
    order = request.values.get('order', 'level')
    char_list = rooster.group_by(Rooster.Fields(order))
    return render_template('char-list.html',
                           rooster=char_list,
                           order=order,
                           sexes=Character.Sex,
                           races=Character.Races,
                           professions=Character.Professions,
                           disciplines=Character.Disciplines,
                           orders=Character.Orders)


@characters.route('/', methods=['POST'])
def create():
    """Add a new characters to the rooster."""
    rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
    form = request.values
    name = form.get('name')
    level = int(form.get('level'))
    race = Character.Races(form.get('race'))
    sex = Character.Sex(form.get('sex'))
    profession = Character.Professions(form.get('profession'))

    disciplines = {}
    discipline1 = form.get('discipline1')
    if discipline1:
        discipline1_level = int(form.get('discipline1_level'))
        disciplines[Character.Disciplines(discipline1)] = discipline1_level

    discipline2 = form.get('discipline2')
    if discipline2:
        discipline2_level = int(form.get('discipline2_level'))
        disciplines[Character.Disciplines(discipline2)] = discipline2_level

    order = None
    order_value = form.get('order')
    if order_value:
        order = Character.Orders(order_value)

    rooster.add(Character(name, level, race, sex, profession, disciplines,
                          order))
    rooster.save()

    return jsonify(status='OK')
