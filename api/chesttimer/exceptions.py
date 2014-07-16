#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Exception system for Chesttimer."""

# Chesttimer, an agenda creator for GW2 chests.
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


class ChesttimerError(Exception):

    """Base class for all exceptions."""

    def __init__(self):
        """Define status and message for the error."""
        super(ChesttimerError, self).__init__()

        self.status = 500
        self.message = 'Unknown error'
        self.json = {}

    def _json(self):
        """Fill the json property.

        If you need to change something, just extend this function.
        """
        # The code is the exception name, with the prefix "Chesttimer" and the
        # suffix "error" removed.
        code = self.__class__.__name__[10:-5]
        self.json = {'status': 'ERROR',     # always an error
                     'message': self.message,
                     'code': code}

    def response(self):
        """Return a JSON representation of the exception."""
        self._json()        # encode the error
        response = jsonify(self.json)
        response.status_code = self.status
        return response


class ChesttimerElementNotFoundError(ChesttimerError):

    """Element not found (404)."""

    def __init__(self):
        """Set the error code and message."""
        super(ChesttimerElementNotFoundError, self).__init__()
        self.status = 404
        self.message = 'Element Not Found'


class ChesttimerMethodNotAllowedError(ChesttimerError):

    """Method not allowed (405)."""

    def __init__(self):
        """Set the error code and message."""
        super(ChesttimerMethodNotAllowedError, self).__init__()
        self.status = 405
        self.message = 'Method not allowed'


class ChesttimerCharacterNameTooLongError(ChesttimerError):

    """The name of the character is too long."""

    def __init__(self):
        """Set the error code and message."""
        super(ChesttimerCharacterNameTooLongError, self).__init__()
        self.status = 400
        self.message = 'Name too long'


class ChesttimerInvalidCharacterLevelError(ChesttimerError):

    """The level for the character is invalid."""

    def __init__(self):
        """Set the error code and message."""
        super(ChesttimerInvalidCharacterLevelError, self).__init__()
        self.status = 400
        self.message = 'Invalid level'


class ChesttimerInvalidRaceError(ChesttimerError):

    """The race is invalid."""

    def __init__(self):
        """Set the error code and message."""
        super(ChesttimerInvalidRaceError, self).__init__()
        self.status = 400
        self.message = 'Invalid race'


class ChesttimerInvalidSexError(ChesttimerError):

    """The sex is invalid."""

    def __init__(self):
        """Set the error code and message."""
        super(ChesttimerInvalidSexError, self).__init__()
        self.status = 400
        self.message = 'Invalid sex'
