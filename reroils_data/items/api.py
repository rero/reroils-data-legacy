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

"""API for item."""

from uuid import uuid4

from invenio_circulation.api import Item as CirculationItem

from reroils_data.transactions.api import CircTransaction


class Item(CirculationItem):
    """Data model to store circulation item informations."""

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
