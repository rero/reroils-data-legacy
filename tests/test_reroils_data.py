# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Module tests."""

from __future__ import absolute_import, print_function

import pytest
from flask import Flask

from reroils_data import REROILSDATA


def test_version():
    """Test version import."""
    from reroils_data import __version__
    assert __version__


def test_jsonschema():
    """Test jsonschema for records."""

    from json import loads
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError
    from pkg_resources import resource_string

    schema_in_bytes = resource_string('reroils_data.jsonschemas',
                                      'records/record-v0.0.1.json')
    schema = loads(schema_in_bytes.decode('utf8'))

    validate({
        '$schema': 'http://ils.rero.ch/schema/records/record-v0.0.1.json',
        'bibid': '123',
        'title': 'my title'
    }, schema)

    with pytest.raises(ValidationError):
        validate({
            '$schema': 'http://ils.rero.ch/schema/records/record-v0.0.1.json',
            'bibid': '123',
            'title': 'my'
        }, schema)

    with pytest.raises(ValidationError):
        validate({
            '$schema': 'http://ils.rero.ch/schema/records/record-v0.0.1.json',
            'bibid': '123'
        }, schema)

    with pytest.raises(ValidationError):
        validate({
            '$schema': 'http://ils.rero.ch/schema/records/record-v0.0.1.json',
            'bibid': 123,
            'title': 'my title'
        }, schema)


def test_record_mappings():
    """Test elasticsearch mappings for records."""

    from json import loads
    from pkg_resources import resource_string

    mappings_in_bytes = resource_string('reroils_data.mappings',
                                        'records/record-v0.0.1.json')
    mappings = loads(mappings_in_bytes.decode('utf8'))
    assert mappings.get('mappings').get('record-v1.0.0')


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = REROILSDATA(app)
    assert 'reroils-data' in app.extensions

    app = Flask('testapp')
    ext = REROILSDATA()
    assert 'reroils-data' not in app.extensions
    ext.init_app(app)
    assert 'reroils-data' in app.extensions


def test_view(app):
    """Test view."""
    REROILSDATA(app)
    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 200
        assert 'Welcome to REROILS-DATA' in str(res.data)
