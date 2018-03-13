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
def minimal_patron_record():
    """Simple patron record."""
    yield {
        '$schema': 'http://ils.test.rero.ch/schema\
            /patrons/patron-v0.0.1.json',
        'pid': '1',
        'first_name': 'Simonetta',
        'last_name': 'Casalini',
        'street': 'Avenue Leopold-Robert, 132',
        'postal_code': '2300',
        'city': 'La Chaux-de-Fonds',
        'barcode': '2050124311',
        'birth_date': '1967-06-07',
        'email': 'simolibri07@gmail.com',
        'phone': '+41324993585',
        'patron_type': 'standard_user'
    }


@pytest.fixture()
def patron_schema():
    """Patron Jsonschema for records."""
    schema_in_bytes = resource_string('reroils_data.patrons.jsonschemas',
                                      'patrons/patron-v0.0.1.json')
    schema = loads(schema_in_bytes.decode('utf8'))
    return schema


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)
