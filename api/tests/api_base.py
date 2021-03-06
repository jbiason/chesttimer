#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Base class for the API tests."""

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

import unittest
import json

# pylint:disable=import-error
from chesttimer import server
from chesttimer import exceptions


# pylint:disable=too-many-public-methods
class APITests(unittest.TestCase):

    """Base functions for testing the API."""

    ROOSTER = './rooster.json'

    def setUp(self):
        """Test set up."""
        server.app.config['DEBUG'] = True
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        return

    # ------------------------------------------------------------
    # Asserts
    # ------------------------------------------------------------
    # pylint:disable=invalid-name
    def assertJSON(self, response, expected):
        """Assert the JSON inside the response.

        Assert that:

        1) The response containts a JSON response;
        2) The JSON response has all the expected fields.

        :param response: The test_client response
        :param expected: Expected JSON
        :type expected: dict
        """
        response = json.loads(response.data)
        keys = expected.keys()
        for key in expected:
            if key not in response:
                self.fail('Key {key} not in response'.format(key=key))

            if response[key] != expected[key]:
                self.fail('Key {key} differs: Expected "{expected}", '
                          'response "{response}"'.format(
                              key=key,
                              expected=expected[key],
                              response=response[key]))

            del keys[keys.index(key)]

        if keys:
            self.fail('Extraneous keys received: {keys}'.format(
                keys=', '.join(keys)))

        return

    def assertStatus(self, response, expected_status):
        """Assert that the response have the expected status."""
        self.assertEqual(response.status_code, expected_status)
        return

    def assertJSONOk(self, response, **extras):
        """Assert for an OK response.

        Assert that the response JSON contains the "OK" status, along with
        its status. Any other fields that must be checked in the response
        should be passed in **extras.
        """
        expected = {'status': 'OK'}
        if extras:
            expected.update(extras)

        self.assertStatus(response, 200)
        self.assertJSON(response, expected)
        return

    def assertJSONError(self, response, exception):
        """Assert that the exception is being returned.

        :param response: The test_client response
        :param exception: Exception code, which is basically the exception
        name without the 'Exception' suffix.
        """
        # first of all, try to find the exception
        full_exception_name = 'Chesttimer' + exception + 'Error'
        exception_cls = getattr(exceptions, full_exception_name)
        exception_obj = exception_cls()
        self.assertStatus(response, exception_obj.status)

        expected = {'code': exception,
                    'message': exception_obj.message}
        self.assertJSON(response, expected)
        return
