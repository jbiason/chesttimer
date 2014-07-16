#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Main server/controller."""

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

from flask import Flask

from .settings import Settings
from .exceptions import ChesttimerError
from .exceptions import ChesttimerElementNotFoundError
from .exceptions import ChesttimerMethodNotAllowedError

# ----------------------------------------------------------------------
# Start the app
# ----------------------------------------------------------------------
# pylint:disable=invalid-name
app = Flask(__name__)
app.config.from_object(Settings)
app.config.from_envvar('CHESTTIMER_CONFIG', True)


# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------
from .api.sex import SexView
from .api.profession import ProfessionView
from .api.race import RaceView
from .api.discipline import DisciplineView
from .api.order import OrderView
from .api.character import CharacterView

SexView.register(app, route_base='/api/sexes/')
ProfessionView.register(app, route_base='/api/professions/')
RaceView.register(app, route_base='/api/races/')
DisciplineView.register(app, route_base='/api/disciplines/')
OrderView.register(app, route_base='/api/orders/')
CharacterView.register(app, route_base='/api/characters/')


@app.errorhandler(ChesttimerError)
def exception_handler(error):
    """Handle all internal exceptions."""
    return error.response()


# pylint:disable=unused-argument
@app.errorhandler(404)
def not_found(error):
    """Intercept the 404 error to return a JSON instead."""
    return exception_handler(ChesttimerElementNotFoundError())


# pylint:disable=unused-argument
@app.errorhandler(405)
def not_allowed(error):
    """Intercept the 405 error to return a JSON instead."""
    return exception_handler(ChesttimerMethodNotAllowedError())
