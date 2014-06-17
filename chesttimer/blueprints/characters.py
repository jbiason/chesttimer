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
                           order=order)


@characters.route('/', methods=['POST'])
def create():
    rooster = Rooster(current_app.config.get('ROOSTER_PATH'))
    rooster.add(Character())
