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

"""API for manipulating patrons."""

from invenio_search.api import RecordsSearch

from ..api import IlsRecord
from ..documents_items.api import DocumentsWithItems
from .fetchers import patron_id_fetcher
from .minters import patron_id_minter
from .providers import PatronProvider


class BorrowedDocumentsSearch(RecordsSearch):
    """RecordsSearch for borrowed documents."""

    class Meta:
        """Search only on documents index."""

        index = 'documents'


class PatronsSearch(RecordsSearch):
    """RecordsSearch for borrowed documents."""

    class Meta:
        """Search only on patrons index."""

        index = 'patrons'


class Patron(IlsRecord):
    """Define API for patrons mixing."""

    minter = patron_id_minter
    fetcher = patron_id_fetcher
    provider = PatronProvider

    @classmethod
    def get_patron_by_user(cls, user):
        """Get patron by user."""
        return cls.get_patron_by_email(email=user.email)

    @classmethod
    def get_patron_by_email(cls, email=None):
        """Get patron by email."""
        uuid, pid_value = cls._get_uuid_pid_by_email(email)
        if uuid:
            return cls.get_record(uuid)
        else:
            return None

    @classmethod
    def _get_uuid_pid_by_email(cls, email):
        """Get record by email."""
        search = PatronsSearch()
        result = search.filter(
            'term',
            email=email
        ).source(includes='pid').execute().to_dict()
        try:
            result = result['hits']['hits'][0]
            return result['_id'], result['_source']['pid']
        except Exception:
            return None, None

    def get_borrowed_documents_pids(self):
        """Get pid values borrowed documents for given patron."""
        pids = [p.pid for p in BorrowedDocumentsSearch().filter(
            'term',
            itemslist___circulation__holdings__patron_barcode=self.get(
                'barcode'
            )
        ).source(includes=['id', 'pid']).scan()]
        return pids

    def get_borrowed_documents(self):
        """Get borrowed documents."""
        pids = self.get_borrowed_documents_pids()
        to_return = []
        for pid_value in pids:
            rec = DocumentsWithItems.get_record_by_pid(pid_value)
            to_return.append(rec)
        return to_return
