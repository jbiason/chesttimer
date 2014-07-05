#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the race API."""

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

from api_base import APITests


# pylint:disable=too-many-public-methods
class APIRaceTests(APITests):

    """Tests for the race API."""

    def test_get(self):
        """Get the list of races."""
        response = self.app.get('/api/races/')
        self.assertJSONOk(response, races={'asura': 'Asura',
                                           'charr': 'Charr',
                                           'human': 'Human',
                                           'norn': 'Norn',
                                           'sylvari': 'Sylvari'})
        return
