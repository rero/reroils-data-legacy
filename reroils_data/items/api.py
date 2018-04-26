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

"""API for manipulating items."""

from uuid import uuid4

from invenio_circulation.api import Item as CirculationItem

from reroils_data.transactions.api import CircTransaction

from ..api import IlsRecord
from .fetchers import item_id_fetcher
from .minters import item_id_minter
from .providers import ItemProvider


class Item(IlsRecord, CirculationItem):
    """Location class."""

    minter = item_id_minter
    fetcher = item_id_fetcher
    provider = ItemProvider

    @classmethod
    def create(cls, data, id_=None, delete_pid=True, **kwargs):
        """Create a new item record."""
        if not data.get('_circulation'):
            data['_circulation'] = {
                'holdings': [],
                'status': 'on_shelf'
            }
        data['_circulation'].setdefault('holdings', [])
        return super(Item, cls).create(
            data, id_=id_, delete_pid=delete_pid, **kwargs
        )

    def number_of_item_requests(self):
        """Get number of requests for a given item."""
        circulation = self.get('_circulation', {})
        number_requests = 0
        if circulation:
            holdings = circulation.get('holdings', [])
            if holdings:
                if self.get('_circulation', {}).get('status', '') == 'on_loan':
                        number_requests = len(holdings) - 1
                else:
                    number_requests = len(holdings)
        return number_requests

    def patron_request_rank(self, patron_barcode):
        """Get the rank of patron in list of requests on this item."""
        holdings = self.get('_circulation', {}).get('holdings', [])
        if self.get('_circulation', {}).get('status', '') == 'on_loan':
            start_pos = 1
        else:
            start_pos = 0
        rank = 1
        for i_holding in range(start_pos, len(holdings)):
            holding = holdings[i_holding]
            if holding and holding.get('patron_barcode'):
                if holding['patron_barcode'] == patron_barcode:
                    return rank
            rank = rank+1
        return False

    def requested_by_patron(self, patron_barcode):
        """Check if the item is requested by a given patron."""
        for holding in self.get('_circulation', {}).get('holdings', []):
            if holding and holding.get('patron_barcode'):
                if holding['patron_barcode'] == patron_barcode:
                    return True
        return False

    def loaned_to_patron(self, patron_barcode):
        """Check if the item is loaned by a given patron."""
        for holding in self.get('_circulation', {}).get('holdings', []):
            if self.get('_circulation', {}).get('status', '') == 'on_loan':
                if holding and holding.get('patron_barcode'):
                    if holding['patron_barcode'] == patron_barcode:
                        return True
        return False

    def loan_item(self, **kwargs):
        """Loan item to the user."""
        id = str(uuid4())
        super(Item, self).loan_item(id=id, **kwargs)
        CircTransaction.create(self.build_data(0, 'add_item_loan'), id=id)

    def request_item(self, **kwargs):
        """Request item for the user."""
        id = str(uuid4())
        super(Item, self).request_item(id=id, **kwargs)
        CircTransaction.create(self.build_data(-1, 'add_item_request'), id=id)

    def return_item(self, **kwargs):
        """Return item."""
        data = self.build_data(0, 'add_item_return')
        super(Item, self).return_item()
        CircTransaction.create(data)

    def build_data(self, record, _type):
        """Build transaction json data."""
        data = {
            'transaction_type': _type,
            'item_barcode': self['barcode'],
            'patron_barcode':
                self['_circulation']['holdings'][record]['patron_barcode']
        }
        return data
