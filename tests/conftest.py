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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
from json import loads

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_db import InvenioDB
from invenio_pidstore import InvenioPIDStore
from pkg_resources import resource_string
from sqlalchemy_utils.functions import create_database, database_exists


@pytest.yield_fixture()
def item_minimal_record():
    """Item Minimal record."""
    yield {
        '$schema': 'ils.test.rero.ch/schemas/records/item-v0.0.1.json',
        'itemid': '2',
        'barcode': 10000000001,
        'callNumber': 'PA-10001',
        'localisation': 'publicAccess'
    }


@pytest.yield_fixture()
def minimal_record():
    """Minimal record."""
    yield {
        '$schema': 'ils.test.rero.ch/schemas/records/record-v0.0.1.json',
        'bibid': '2',
        'title': 'RERO21 pour les nuls : les premiers pas',
        'languages': ['fre'],
        'identifiers': {'reroID': 'R004567655'}
    }


@pytest.fixture()
def item_schema():
    """Item Jsonschema for records."""
    schema_in_bytes = resource_string('reroils_data.jsonschemas',
                                      'records/item-v0.0.1.json')
    schema = loads(schema_in_bytes.decode('utf8'))
    return schema


@pytest.fixture()
def schema():
    """Jsonschema for records."""
    schema_in_bytes = resource_string('reroils_data.jsonschemas',
                                      'records/record-v0.0.1.json')
    schema = loads(schema_in_bytes.decode('utf8'))
    return schema


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.yield_fixture()
def app(request):
    """Flask application fixture."""
    # Set temporary instance path for sqlite
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'
        ),
        TESTING=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    InvenioDB(app)
    InvenioPIDStore(app)
    Babel(app)

    with app.app_context():
        yield app

    # Teardown instance path.
    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    from invenio_db import db as db_
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()

    yield db_

    db_.session.remove()
    db_.drop_all()
