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


def test_item_circulation(db, minimal_item_record, minimal_patron_record):
    """Test item loan, return and request."""
    assert minimal_patron_record['barcode']
    patron_barcode = minimal_patron_record['barcode']
    item = Item.create(minimal_item_record)
    item.loan_item(patron_barcode=patron_barcode)
    assert item['_circulation']['status'] == 'on_loan'
    item.return_item()
    assert item['_circulation']['status'] != 'on_loan'
    item.request_item(patron_barcode=patron_barcode)
    record = item['_circulation']['holdings'][0]['patron_barcode']
    assert record == patron_barcode
