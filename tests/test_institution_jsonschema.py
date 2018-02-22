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

"""INSTITUTION JSON schema tests."""

from __future__ import absolute_import, print_function

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def test_institution_required(institution_schema, institution_minimal_record):
    """Test required for institution jsonschema."""
    validate(institution_minimal_record, institution_schema)

    with pytest.raises(ValidationError):
        validate({}, institution_schema)


def test_institutionid(institution_schema, institution_minimal_record):
    """Test institutionid for institution jsonschema."""
    validate(institution_minimal_record, institution_schema)

    with pytest.raises(ValidationError):
        institution_minimal_record['institutionid'] = '25'
        validate(institution_minimal_record, institution_schema)


def test_name(institution_schema, institution_minimal_record):
    """Test name for institution jsonschema."""
    validate(institution_minimal_record, institution_schema)

    with pytest.raises(ValidationError):
        institution_minimal_record['name'] = 25
        validate(institution_minimal_record, institution_schema)


def test_address(institution_schema, institution_minimal_record):
    """Test address for institution jsonschema."""
    validate(institution_minimal_record, institution_schema)

    with pytest.raises(ValidationError):
        institution_minimal_record['address'] = 25
        validate(institution_minimal_record, institution_schema)
