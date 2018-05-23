# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
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

import collections
import datetime
import uuid
from datetime import datetime, timedelta
from functools import partial, wraps
from operator import indexOf
from uuid import uuid4

import six
from invenio_db import db
from invenio_pidstore.errors import PIDInvalidAction
from sqlalchemy import BOOLEAN, DATE, INTEGER, cast, func, type_coerce
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_continuum import version_class

from ..api import IlsRecord
from ..locations.api import Location
from ..members.api import Member
from ..members_locations.api import MemberWithLocations
from ..transactions.api import CircTransaction
from .fetchers import item_id_fetcher
from .minters import item_id_minter
from .models import ItemStatus
from .providers import ItemProvider


def check_status(method=None, statuses=None):
    """Check that the item has a defined status."""
    if method is None:
        return partial(check_status, statuses=statuses)

    statuses = statuses or []

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Check current deposit status."""
        if self['_circulation']['status'] not in statuses:
            raise PIDInvalidAction()

        return method(self, *args, **kwargs)
    return wrapper


class Holding(dict):
    """Holding class to create and maintain holdings."""

    @classmethod
    def create(cls, id_=None, **kwargs):
        """Create a valid holding."""
        return cls(id=id_ or kwargs.pop('id', str(uuid.uuid4())), **kwargs)


class HoldingIterator(object):
    """Data access object to manage holdings associated to an item."""

    def __init__(self, iterable):
        """Initialize iterator."""
        self._iterable = iterable

    def __len__(self):
        """Get number of files."""
        return len(self._iterable)

    def __iter__(self):
        """Get iterator."""
        self._it = iter(self._iterable)
        return self._it

    def next(self):
        """Python 2.7 compatibility."""
        return self.__next__()  # pragma: no cover

    def __next__(self):
        """Get next file item."""
        return next(self._it)   # pragma: no cover

    def __contains__(self, id_):
        """Check if HoldingIterator contains a Holding by id."""
        return id_ in (x['id'] for x in self)

    def __getitem__(self, key):
        """Get a specific file."""
        return self._iterable[key]  # pragma: no cover

    def __setitem__(self, key, obj):
        """Add file inside a deposit."""
        self._iterable[key] = obj   # pragma: no cover

    def __delitem__(self, id_):
        """Delete a Holding by id.

        :raises ValueError:
        """
        index = indexOf((x['id'] for x in self), str(id_))
        del self._iterable[index]

    def append(self, obj):
        """Append a holding to the end."""
        self._iterable.append(obj)

    def insert(self, index, obj):
        """Insert a holding before given index."""
        self._iterable.insert(index, obj)

    def pop(self, index):
        """Remove and return a holding at index (default is last)."""
        return self._iterable.pop(index)


class Item(IlsRecord):
    """Item class."""

    minter = item_id_minter
    fetcher = item_id_fetcher
    provider = ItemProvider
    default_duration = 30
    durations = {
        'short_loan': 15
    }

    @property
    def holdings(self):
        """Property of holdings associated with the given item."""
        return HoldingIterator(self['_circulation']['holdings'])

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

    @classmethod
    def find_by_holding(cls, **kwargs):
        """Find item versions based on their holdings information.

        Every given kwarg will be queried as a key-value pair in the items
        holding.

        :returns: List[(UUID, version_id)] with `version_id` as used by
                  `RecordMetadata.version_id`.
        """
        def _get_filter_clause(obj, key, value):
            val = obj[key].astext
            CASTS = {
                bool: lambda x: cast(x, BOOLEAN),
                int: lambda x: cast(x, INTEGER),
                datetime.date: lambda x: cast(x, DATE),
            }
            if (not isinstance(value, six.string_types) and
                    isinstance(value, collections.Sequence)):
                if len(value) == 2:
                    return CASTS[type(value[0])](val).between(*value)
                raise ValueError('Too few/many values for a range query. '
                                 'Range query requires two values.')
            return CASTS.get(type(value), lambda x: x)(val) == value

        RecordMetadataVersion = version_class(RecordMetadata)

        data = type_coerce(RecordMetadataVersion.json, JSONB)
        path = ('_circulation', 'holdings')

        subquery = db.session.query(
            RecordMetadataVersion.id.label('id'),
            RecordMetadataVersion.version_id.label('version_id'),
            func.json_array_elements(data[path]).label('obj')
        ).subquery()

        obj = type_coerce(subquery.c.obj, JSONB)

        query = db.session.query(
            RecordMetadataVersion.id,
            RecordMetadataVersion.version_id
        ).filter(
            RecordMetadataVersion.id == subquery.c.id,
            RecordMetadataVersion.version_id == subquery.c.version_id,
            *(_get_filter_clause(obj, k, v) for k, v in kwargs.items())
        )

        for result in query:
            yield result

    @check_status(statuses=[ItemStatus.ON_SHELF])
    def loan_item(self, **kwargs):
        """Loan item to the user.

        Adds a loan to *_circulation.holdings*.

        :param user: Invenio-Accounts user.
        :param start_date: Start date of the loan. Must be today.
        :param end_date: End date of the loan.
        :param waitlist: If the desired dates are not available, the item will
                         be put on a waitlist.
        :param delivery: 'pickup' or 'mail'
        """
        id = str(uuid4())
        self['_circulation']['status'] = ItemStatus.ON_LOAN
        self.holdings.insert(0, Holding.create(id=id, **kwargs))
        CircTransaction.create(self.build_data(0, 'add_item_loan'), id=id)

    @check_status(statuses=[ItemStatus.ON_LOAN,
                            ItemStatus.ON_SHELF,
                            ItemStatus.AT_DESK,
                            ItemStatus.IN_TRANSIT])
    def request_item(self, **kwargs):
        """Request item for the user.

        Adds a request to *_circulation.holdings*.

        :param user: Invenio-Accounts user.
        :param start_date: Start date of the loan. Must be today or a future
                           date.
        :param end_date: End date of the loan.
        :param waitlist: If the desired dates are not available, the item will
                         be put on a waitlist.
        :param delivery: 'pickup' or 'mail'
        """
        id = str(uuid4())
        self.holdings.append(Holding.create(id=id, **kwargs))
        CircTransaction.create(self.build_data(-1, 'add_item_request'), id=id)

    @check_status(statuses=[ItemStatus.ON_LOAN])
    def return_item(self, **kwargs):
        """Return given item.

        The item's status will be set to ItemStatus.ON_SHELF.
        """
        data = self.build_data(0, 'add_item_return')
        self['_circulation']['status'] = ItemStatus.ON_SHELF
        self.holdings.pop(0)
        CircTransaction.create(data)

    @check_status(statuses=[ItemStatus.ON_LOAN,
                            ItemStatus.ON_SHELF,
                            ItemStatus.AT_DESK,
                            ItemStatus.IN_TRANSIT])
    def lose_item(self):
        """Lose the given item.

        This sets the status to ItemStatus.MISSING.
        All existing holdings will be canceled.
        """
        self['_circulation']['status'] = ItemStatus.MISSING

        for holding in self.holdings:
            self.cancel_hold(holding['id'])

    @check_status(statuses=[ItemStatus.MISSING])
    def return_missing_item(self, **kwargs):
        """Return the missing item.

        The item's status will be set to ItemStatus.ON_SHELF.
        """
        data = self.build_data(0, 'add_item_return_missing')
        self['_circulation']['status'] = ItemStatus.ON_SHELF
        CircTransaction.create(data)

    def cancel_hold(self, id_):
        """Cancel the identified hold.

        The item's corresponding hold information wil be removed.
        This action updates the waitlist.
        """
        del self.holdings[id_]

    @property
    def duration(self):
        """Get loan/extend duration based on item type."""
        return self.durations.get(self['item_type'], self.default_duration)

    @check_status(statuses=[ItemStatus.ON_LOAN])
    def extend_loan(
            self, requested_end_date=None, renewal_count=None, **kwargs
    ):
        """Request a new end date for the active loan.

        A possible status ItemStatus.OVERDUE will be removed.
        """
        id = str(uuid4())
        if not renewal_count:
            renewal_count = self.get_renewal_count()
        if not requested_end_date:
            end_date = self.get_item_end_date()
            request_date = end_date + timedelta(self.duration)
            requested_end_date = datetime.strftime(request_date, '%Y-%m-%d')
        self['_circulation']['status'] = ItemStatus.ON_LOAN
        self.holdings[0]['end_date'] = requested_end_date
        self.holdings[0]['renewal_count'] = renewal_count + 1
        CircTransaction.create(self.build_data(0, 'extend_item_loan'), id=id)

    def get_item_end_date(self):
        """Get item due date a given item."""
        circulation = self.get('_circulation', {})
        if circulation:
            holdings = circulation.get('holdings', [])
            if holdings:
                if self.get('_circulation', {}).get('status', '') == 'on_loan':
                    if holdings[0].get('end_date'):
                        end_date_str = holdings[0].get('end_date')
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                        return end_date
        return None

    def get_renewal_count(self):
        """Get item renewal count."""
        circulation = self.get('_circulation', {})
        if circulation:
            holdings = circulation.get('holdings', [])
            if holdings:
                if self.get('_circulation', {}).get('status', '') == 'on_loan':
                    if holdings[0].get('renewal_count'):
                        renewal_count = holdings[0].get('renewal_count')
                        return renewal_count
        return 0

    def build_data(self, record, _type):
        """Build transaction json data."""
        data = {
            'transaction_type': _type,
            'item_barcode': self['barcode'],
            'patron_barcode':
                self['_circulation']['holdings'][record]['patron_barcode']
        }
        return data

    def dumps(self, **kwargs):
        """Return pure Python dictionary with record metadata."""
        data = super(IlsRecord, self).dumps(**kwargs)
        location_pid = data.get('location_pid')
        location = Location.get_record_by_pid(location_pid)
        data['location_name'] = location.get('name')
        member = MemberWithLocations.get_member_by_locationid(location.id)
        data['member_pid'] = member.pid
        data['member_name'] = member.get('name')
        data['requests_count'] = self.number_of_item_requests()
        for holding in data.get('_circulation', {}).get('holdings', []):
            pickup_member_pid = holding.get('pickup_member_pid')
            if pickup_member_pid:
                holding_member = Member.get_record_by_pid(pickup_member_pid)
                holding['pickup_member_name'] = holding_member['name']
        return data

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
            rank += 1
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
