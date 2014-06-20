#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Main server/controller."""

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

from flask import Flask
from flask import render_template

from .settings import Settings

# ----------------------------------------------------------------------
# Start the app
# ----------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Settings)
app.config.from_envvar('CHESTTIMER_CONFIG', True)


# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------
from .api.sex import SexView
from .api.profession import ProfessionView

SexView.register(app, route_base='/api/sexes/')
ProfessionView.register(app, route_base='/api/professions/')


# ----------------------------------------------------------------------
# Blueprints
# ----------------------------------------------------------------------
from .blueprints.characters import characters
app.register_blueprint(characters, url_prefix='/chars')


# this is temporary
@app.route('/')
def index():
    return render_template('index.html')
