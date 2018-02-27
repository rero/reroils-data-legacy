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
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from pkg_resources import resource_string
from sqlalchemy_utils.functions import create_database, database_exists


@pytest.yield_fixture()
def institution_minimal_record():
    """Institution Minimal record."""
    yield {
        '$schema': 'http://ils.test.rero.ch/schema\
            /institutions/institution-v0.0.1.json',
        'institutionid': '1',
        'name': 'MV Sion',
        'address': 'address',
        'libraries': [
            {
                'code': 1,
                'name': 'MV Sion bibliothèque des jeunes',
                'address': 'Place de la Gare 18, 1950 Sion',
                'email': 'info@bibliosionjeunes.ch'
            },
            {
                'code': 2,
                'name': 'MV Sion bibliothèque des adultes',
                'address': 'Place de la Gare 18, 1950 Sion',
                'email': 'info@bibliosionadultes.ch'
            }
        ]
    }


@pytest.yield_fixture()
def item_minimal_record():
    """Item Minimal record."""
    yield {
        '$schema': 'http://ils.test.rero.ch/schema/items/item-v0.0.1.json',
        'itemid': '2',
        'barcode': 10000000001,
        'callNumber': 'PA-10001',
        'location': 'publicAccess'
    }


@pytest.yield_fixture()
def minimal_record():
    """Minimal record."""
    yield {
        '$schema': 'http://ils.test.rero.ch/schema/records/record-v0.0.1.json',
        'bibid': '2',
        'title': 'RERO21 pour les nuls : les premiers pas',
        'languages': [{'language': 'fre'}],
    }


@pytest.fixture()
def item_schema():
    """Item Jsonschema for records."""
    schema_in_bytes = resource_string('reroils_data.jsonschemas',
                                      'items/item-v0.0.1.json')
    schema = loads(schema_in_bytes.decode('utf8'))
    return schema


@pytest.fixture()
def institution_schema():
    """Institution Jsonschema for records."""
    schema_in_bytes = resource_string('reroils_data.jsonschemas',
                                      'institutions/institution-v0.0.1.json')
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
        JSONSCHEMAS_ENDPOINT='/schema',
        JSONSCHEMAS_HOST='ils.test.rero.ch'
    )

    InvenioDB(app)
    InvenioPIDStore(app)
    InvenioRecords(app)
    ext = InvenioJSONSchemas(app)
    # directory = os.path.dirname(reroils_data.jsonschemas.__file__)
    # ext.register_schemas_dir(directory)
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
