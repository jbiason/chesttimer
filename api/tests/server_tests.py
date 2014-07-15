#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the base server."""

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

import json

from api_base import APITests


# pylint:disable=too-many-public-methods
class ServerTests(APITests):

    """Tests for the base server."""

    def test_not_found_json(self):
        """Check if the response for 404 is a JSON."""
        response = self.app.get('/not-found')
        self.assertEqual(response.status_code, 404)
        json_resp = json.loads(response.data)
        self.assertIsNotNone(json_resp)     # must conver to json

        self.assertTrue('status' in json_resp and json_resp['status'] ==
                        'ERROR')
        self.assertTrue('code' in json_resp and json_resp['code'] ==
                        'ElementNotFound')
        return

    def test_method_not_allowed(self):
        """Check if the response for 405 is a JSON."""
        response = self.app.post('/api/sexes/', data={'sex': 'undefined'})
        self.assertEqual(response.status_code, 405)
        json_resp = json.loads(response.data)
        self.assertIsNotNone(json_resp)     # must conver to json

        self.assertTrue('status' in json_resp and json_resp['status'] ==
                        'ERROR')
        self.assertTrue('code' in json_resp and json_resp['code'] ==
                        'MethodNotAllowed')
        return
