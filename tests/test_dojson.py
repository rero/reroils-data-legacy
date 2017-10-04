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

"""DOJSON module tests."""

from __future__ import absolute_import, print_function

from dojson.contrib.marc21.utils import create_record

from reroils_data.dojson.contrib.marc21tojson import marc21tojson


def test_marc21totitle():
    """Test dojson marc21totitle."""

    marc21xml = """
    <record>
      <datafield tag="245" ind1="1" ind2="0">
        <subfield code="a">RERO21 pour les nuls</subfield>
      </datafield>
    </record>
    """
    blob = create_record(marc21xml)
    data = marc21tojson.do(blob)
    assert data.get('title') == 'RERO21 pour les nuls'


def test_marc21toauthor():
    """Test dojson marc21toauthor."""

    marc21xml = """
    <record>
      <datafield tag="100" ind1=" " ind2=" ">
        <subfield code="a">Jean Dumont</subfield>
      </datafield>
    </record>
    """
    blob = create_record(marc21xml)
    data = marc21tojson.do(blob)
    assert data.get('author') == 'Jean Dumont'
