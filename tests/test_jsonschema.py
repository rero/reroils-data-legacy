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

"""JSON schema tests."""

from __future__ import absolute_import, print_function

from json import loads

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pkg_resources import resource_string


def test_required(schema, minimal_record):
    """Test required for jsonschema."""
    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        validate({}, schema)


def test_bibid(schema, minimal_record):
    """Test bibid for jsonschema."""
    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['bibid'] = 25
        validate(minimal_record, schema)


def test_title(schema, minimal_record):
    """Test title for jsonschema."""
    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['title'] = 2
        validate(minimal_record, schema)


def test_titlesProper(schema, minimal_record):
    """Test titlesProper for jsonschema."""
    minimal_record['titlesProper'] = ['RERO21 pour les nuls']

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['titlesProper'] = 'string is a bad type'
        validate(minimal_record, schema)


def test_languages(schema, minimal_record):
    """Test languages for jsonschema."""
    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['languages'] = [2]
        validate(minimal_record, schema)


def test_translatedFrom(schema, minimal_record):
    """Test translatedFrom for jsonschema."""
    minimal_record['translatedFrom'] = ['eng']

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['translatedFrom'] = [2]
        validate(minimal_record, schema)


def test_authors(schema, minimal_record):
    """Test authors for jsonschema."""
    minimal_record['authors'] = [
        {
            'name': 'Dumont, Jean',
            'type': 'person',
            'date': '1954 -',
            'qualifier': 'Développeur'
        },
        {
            'type': 'organisation',
            'name': 'RERO'
        }
    ]

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['authors'][0]['name'] = [2]
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['authors'][0]['type'] = [2]
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['authors'][0]['date'] = [2]
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['authors'][0]['qualifier'] = [2]
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['authors'][1]['type'] = [2]
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['authors'][1]['name'] = [2]
        validate(minimal_record, schema)


def test_publishers(schema, minimal_record):
    """Test publishers for jsonschema."""
    minimal_record['publishers'] = [
        {
            'name': ['Editions de la Centrale'],
            'place': ['Martigny']
        }
    ]

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['publishers'][0]['name'][0] = [2]
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['publishers'][0]['place'][0] = [2]
        validate(minimal_record, schema)


def test_publicationDate(schema, minimal_record):
    """Test publicationDate for jsonschema."""
    minimal_record['publicationDate'] = '2017'

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['publicationDate'] = [2]
        validate(minimal_record, schema)


def test_extent(schema, minimal_record):
    """Test extent for jsonschema."""
    minimal_record['extent'] = '117'

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['extent'] = [2]
        validate(minimal_record, schema)


def test_otherMaterialCharacteristics(schema, minimal_record):
    """Test otherMaterialCharacteristics for jsonschema."""
    minimal_record['otherMaterialCharacteristics'] = 'ill.'

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['otherMaterialCharacteristics'] = [2]
        validate(minimal_record, schema)


def test_formats(schema, minimal_record):
    """Test formats for jsonschema."""
    minimal_record['formats'] = ['15 x 22 cm']

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['formats'] = 'string is a bad type'
        validate(minimal_record, schema)


def test_additionalMaterials(schema, minimal_record):
    """Test additionalMaterials for jsonschema."""
    minimal_record['additionalMaterials'] = '1 CD-ROM'

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['additionalMaterials'] = 2
        validate(minimal_record, schema)


def test_series(schema, minimal_record):
    """Test series for jsonschema."""
    minimal_record['series'] = [
        {
            'name': 'Les débuts de la suite',
            'number': '1'
        },
        {
            'name': 'Autre collection',
            'number': '2'
        }
    ]

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['series'][0]['name'] = 2
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['series'][0]['number'] = 2
        validate(minimal_record, schema)


def test_notes(schema, minimal_record):
    """Test notes for jsonschema."""
    minimal_record['notes'] = ["Photo de l'auteur sur le 4e de couv."]

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['notes'][0] = 2
        validate(minimal_record, schema)


def test_abstracts(schema, minimal_record):
    """Test abstracts for jsonschema."""
    minimal_record['abstracts'] = ["This book is about..."]

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['abstracts'][0] = 2
        validate(minimal_record, schema)


def test_identifiers(schema, minimal_record):
    """Test identifiers for jsonschema."""
    minimal_record['identifiers'] = {
        "reroID": "R004567655",
        "isbn": "9782082015769"
    }

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['identifiers']['reroID'] = 2
        validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['identifiers']['isbn'] = 2
        validate(minimal_record, schema)


def test_subjects(schema, minimal_record):
    """Test subjects for jsonschema."""
    minimal_record['subjects'] = [
        'ILS',
        'informatique',
        'bibliothèque'
    ]

    validate(minimal_record, schema)

    with pytest.raises(ValidationError):
        minimal_record['subjects'] = 2
        validate(minimal_record, schema)
