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

import datetime

from reroils_data.items.api import Item
from reroils_data.items.models import ItemStatus
from reroils_data.locations.api import Location
from reroils_data.members_locations.api import MemberWithLocations


def test_item_extend(db, minimal_item_record,
                     minimal_patron_only_record,
                     minimal_member_record,
                     minimal_location_record):
    """Test validate item request and receive item."""
    member = MemberWithLocations.create(minimal_member_record, dbcommit=True)
    assert member
    location = Location.create(minimal_location_record, dbcommit=True)
    assert location
    member.add_location(location)
    assert member.locations
    patron_barcode = minimal_patron_only_record['barcode']
    assert patron_barcode
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    assert item['_circulation']['status'] == 'on_loan'
    item['_circulation']['holdings'].pop(1)
    item.extend_loan(requested_end_date='2018-02-01')
    assert item['_circulation']['holdings'][0]['end_date'] == '2018-02-01'
    item.extend_loan()
    current_date = datetime.date.today()
    end_date = (current_date + datetime.timedelta(days=30)).isoformat()
    assert item['_circulation']['holdings'][0]['end_date'] == end_date


def test_item_validate(db, minimal_item_record,
                       minimal_patron_only_record,
                       minimal_member_record,
                       minimal_location_record):
    """Test validate item request and receive item."""
    member = MemberWithLocations.create(minimal_member_record, dbcommit=True)
    assert member
    location = Location.create(minimal_location_record, dbcommit=True)
    assert location
    member.add_location(location)
    assert member.locations
    patron_barcode = minimal_patron_only_record['barcode']
    assert patron_barcode
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item(transaction_member_pid='1')
    assert item['_circulation']['status'] == 'at_desk'
    item['_circulation']['status'] = ItemStatus.ON_SHELF
    assert item['_circulation']['status'] == 'on_shelf'
    item.validate_item_request()
    assert item['_circulation']['status'] == 'at_desk'
    item['_circulation']['status'] = ItemStatus.ON_SHELF
    assert item['_circulation']['status'] == 'on_shelf'
    item['_circulation']['holdings'][0]['pickup_member_pid'] = '2'
    item.validate_item_request()
    assert item['_circulation']['status'] == 'in_transit'


def test_item_receive(db, minimal_item_record,
                      minimal_patron_only_record,
                      minimal_member_record,
                      minimal_location_record):
    """Test validate item request and receive item."""
    member = MemberWithLocations.create(minimal_member_record, dbcommit=True)
    assert member
    location = Location.create(minimal_location_record, dbcommit=True)
    assert location
    member.add_location(location)
    assert member.locations
    patron_barcode = minimal_patron_only_record['barcode']
    assert patron_barcode
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item(transaction_member_pid='2')
    assert item['_circulation']['status'] == 'in_transit'
    item['_circulation']['holdings'].pop(0)
    item.receive_item(transaction_member_pid='2')
    assert item['_circulation']['status'] == 'in_transit'
    item.receive_item(transaction_member_pid='1')
    assert item['_circulation']['status'] == 'on_shelf'


def test_item_receive_requested(db, minimal_item_record,
                                minimal_patron_only_record,
                                minimal_member_record,
                                minimal_location_record):
    """Test validate item request and receive item."""
    member = MemberWithLocations.create(minimal_member_record, dbcommit=True)
    assert member
    location = Location.create(minimal_location_record, dbcommit=True)
    assert location
    member.add_location(location)
    assert member.locations
    patron_barcode = minimal_patron_only_record['barcode']
    assert patron_barcode
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item(transaction_member_pid='2')
    assert item['_circulation']['status'] == 'in_transit'

    item.receive_item(transaction_member_pid='1')
    assert item['_circulation']['status'] == 'at_desk'


def test_item_return_loan(db, minimal_item_record,
                          minimal_patron_only_record,
                          minimal_member_record,
                          minimal_location_record):
    """Test validate item request and receive item."""
    member = MemberWithLocations.create(minimal_member_record, dbcommit=True)
    assert member
    location = Location.create(minimal_location_record, dbcommit=True)
    assert location
    member.add_location(location)
    assert member.locations
    patron_barcode = minimal_patron_only_record['barcode']
    assert patron_barcode
    item = Item.create({})
    item.update(minimal_item_record, dbcommit=True)
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item(transaction_member_pid='1')
    assert item['_circulation']['status'] == 'at_desk'
    item.loan_item(patron_barcode='654321')
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item(transaction_member_pid='1')
    assert item['_circulation']['status'] == 'on_shelf'

    item.loan_item(patron_barcode=patron_barcode)
    assert item['_circulation']['status'] == 'on_loan'

    item.return_item(transaction_member_pid='2')
    assert item['_circulation']['status'] == 'in_transit'

    item['_circulation']['status'] = ItemStatus.ON_SHELF
    item.loan_item(patron_barcode='123456')
    assert item['_circulation']['status'] == 'on_loan'
    item.request_item(patron_barcode=patron_barcode, pickup_member_pid='1')
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item(transaction_member_pid='2')
    assert item['_circulation']['status'] == 'in_transit'
