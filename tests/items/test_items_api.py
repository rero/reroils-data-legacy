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

"""Utils tests."""

from __future__ import absolute_import, print_function

from reroils_data.items.api import Item
from reroils_data.locations.api import Location
from reroils_data.members_locations.api import MemberWithLocations


def test_nb_item_requests(db, minimal_item_record, minimal_patron_only_record):
    """Test number of item requests."""
    assert minimal_patron_only_record['barcode']
    patron_barcode = minimal_patron_only_record['barcode']
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    item.request_item(patron_barcode=patron_barcode)
    tr_barcode = item['_circulation']['holdings'][2]['patron_barcode']
    assert tr_barcode == patron_barcode
    number_requests = item.number_of_item_requests()
    assert number_requests == 2


def test_member_name(db, minimal_member_record, minimal_item_record,
                     minimal_location_record):
    """Test member names."""
    member = MemberWithLocations.create(minimal_member_record, dbcommit=True)
    assert member
    location = Location.create(minimal_location_record, dbcommit=True)
    assert location
    member.add_location(location)
    assert member.locations
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    assert item
    data = item.dumps()
    assert data.get('member_pid') == '1'
    assert data.get('member_name') == 'MV Sion'
    holding = data.get('_circulation').get('holdings')[1]
    assert holding['pickup_member_name'] == 'MV Sion'
