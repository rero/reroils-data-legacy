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

"""patron reciever tests."""

from __future__ import absolute_import, print_function

import pytest

from reroils_data.patrons.receivers import patron_receiver


def test_patron_name(minimal_patron_record):
    """Test patron name."""
    first_name = minimal_patron_record.get('first_name' or '')
    last_name = minimal_patron_record.get('last_name' or '')

    patron_receiver(
            json=minimal_patron_record, doc_type='patron-v0.0.1',
            sender=None, index=None, record=None)
    assert minimal_patron_record['name']

    minimal_patron_record['first_name'] = ''
    patron_receiver(
            json=minimal_patron_record, doc_type='patron-v0.0.1',
            sender=None, index=None, record=None)
    assert minimal_patron_record['name'] == minimal_patron_record.get(
                                            'last_name') + ', '

    minimal_patron_record['first_name'] = first_name
    minimal_patron_record['last_name'] = ''
    patron_receiver(
            json=minimal_patron_record, doc_type='patron-v0.0.1',
            sender=None, index=None, record=None)
    assert minimal_patron_record['name'] == ', ' + minimal_patron_record.get(
                                            'first_name')

    minimal_patron_record['first_name'] = ''
    patron_receiver(
            json=minimal_patron_record, doc_type='patron-v0.0.1',
            sender=None, index=None, record=None)
    assert minimal_patron_record['name'] == ', '
