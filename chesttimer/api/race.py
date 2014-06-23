#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""API to return the list of valid races."""

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

from flask_classy import FlaskView

from ..db.rooster import Character


class RaceView(FlaskView):

    """API to return the list of valid races."""

    # pylint:disable=no-self-use
    def index(self):
        """Return the list of races."""
        return jsonify(status='OK',
                       races=dict([(elem.name, elem.value) for elem in
                                   Character.Races]))
