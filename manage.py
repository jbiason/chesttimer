#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Simple script to manage the application."""

import logging

from flask.ext.script import Manager

from chesttimer.server import app

manager = Manager(app)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.config.DEBUG = True
    manager.run()
