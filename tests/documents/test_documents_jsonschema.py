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

"""organisation JSON schema tests."""

from __future__ import absolute_import, print_function

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def test_required(book_schema, minimal_book_record):
    """Test required for jsonschema."""
    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        validate({}, book_schema)


def test_pid(book_schema, minimal_book_record):
    """Test pid for jsonschema."""
    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['pid'] = 25
        validate(minimal_book_record, book_schema)


def test_title(book_schema, minimal_book_record):
    """Test title for jsonschema."""
    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['title'] = 2
        validate(minimal_book_record, book_schema)


def test_titlesProper(book_schema, minimal_book_record):
    """Test titlesProper for jsonschema."""
    minimal_book_record['titlesProper'] = ['RERO21 pour les nuls']

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['titlesProper'] = 'string is a bad type'
        validate(minimal_book_record, book_schema)


def test_languages(book_schema, minimal_book_record):
    """Test languages for jsonschema."""
    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['languages'][0]['language'] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['languages'][0]['language'] = ['gre']
        validate(minimal_book_record, book_schema)


def test_translatedFrom(book_schema, minimal_book_record):
    """Test translatedFrom for jsonschema."""
    minimal_book_record['translatedFrom'] = ['eng']

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['translatedFrom'] = [2]
        validate(minimal_book_record, book_schema)


def test_authors(book_schema, minimal_book_record):
    """Test authors for jsonschema."""
    minimal_book_record['authors'] = [
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

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['authors'][0]['name'] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['authors'][0]['type'] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['authors'][0]['date'] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['authors'][0]['qualifier'] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['authors'][1]['type'] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['authors'][1]['name'] = [2]
        validate(minimal_book_record, book_schema)


def test_publishers(book_schema, minimal_book_record):
    """Test publishers for jsonschema."""
    minimal_book_record['publishers'] = [
        {
            'name': ['Editions de la Centrale'],
            'place': ['Martigny']
        }
    ]

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['publishers'][0]['name'][0] = [2]
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['publishers'][0]['place'][0] = [2]
        validate(minimal_book_record, book_schema)


def test_publicationYear(book_schema, minimal_book_record):
    """Test publicationYear for jsonschema."""
    minimal_book_record['publicationYear'] = 2017

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['publicationYear'] = ['2017']
        validate(minimal_book_record, book_schema)


def test_freeFormedPublicationDate(book_schema, minimal_book_record):
    """Test freeFormedPublicationDate for jsonschema."""
    minimal_book_record['freeFormedPublicationDate'] = '2017'

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['freeFormedPublicationDate'] = [2]
        validate(minimal_book_record, book_schema)


def test_extent(book_schema, minimal_book_record):
    """Test extent for jsonschema."""
    minimal_book_record['extent'] = '117'

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['extent'] = [2]
        validate(minimal_book_record, book_schema)


def test_otherMaterialCharacteristics(book_schema, minimal_book_record):
    """Test otherMaterialCharacteristics for jsonschema."""
    minimal_book_record['otherMaterialCharacteristics'] = 'ill.'

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['otherMaterialCharacteristics'] = [2]
        validate(minimal_book_record, book_schema)


def test_formats(book_schema, minimal_book_record):
    """Test formats for jsonschema."""
    minimal_book_record['formats'] = ['15 x 22 cm']

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['formats'] = 'string is a bad type'
        validate(minimal_book_record, book_schema)


def test_additionalMaterials(book_schema, minimal_book_record):
    """Test additionalMaterials for jsonschema."""
    minimal_book_record['additionalMaterials'] = '1 CD-ROM'

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['additionalMaterials'] = 2
        validate(minimal_book_record, book_schema)


def test_series(book_schema, minimal_book_record):
    """Test series for jsonschema."""
    minimal_book_record['series'] = [
        {
            'name': 'Les débuts de la suite',
            'number': '1'
        },
        {
            'name': 'Autre collection',
            'number': '2'
        }
    ]

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['series'][0]['name'] = 2
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['series'][0]['number'] = 2
        validate(minimal_book_record, book_schema)


def test_notes(book_schema, minimal_book_record):
    """Test notes for jsonschema."""
    minimal_book_record['notes'] = ["Photo de l'auteur sur le 4e de couv."]

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['notes'][0] = 2
        validate(minimal_book_record, book_schema)


def test_abstracts(book_schema, minimal_book_record):
    """Test abstracts for jsonschema."""
    minimal_book_record['abstracts'] = ["This book is about..."]

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['abstracts'][0] = 2
        validate(minimal_book_record, book_schema)


def test_identifiers(book_schema, minimal_book_record):
    """Test identifiers for jsonschema."""
    minimal_book_record['identifiers'] = {
        "reroID": "R004567655",
        "isbn": "9782082015769",
        "bnfID": "cb350330441"
    }

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['identifiers']['reroID'] = 2
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['identifiers']['isbn'] = 2
        validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['identifiers'] = {}
        validate(minimal_book_record, book_schema)

    minimal_book_record['identifiers'] = {
        "bnfID": "cb350330441"
    }

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['identifiers']['bnfID'] = 2
        validate(minimal_book_record, book_schema)


def test_subjects(book_schema, minimal_book_record):
    """Test subjects for jsonschema."""
    minimal_book_record['subjects'] = [
        'ILS',
        'informatique',
        'bibliothèque'
    ]

    validate(minimal_book_record, book_schema)

    with pytest.raises(ValidationError):
        minimal_book_record['subjects'] = 2
        validate(minimal_book_record, book_schema)
