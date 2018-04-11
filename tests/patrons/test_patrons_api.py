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

from uuid import uuid4

import mock
from invenio_accounts import InvenioAccounts
from invenio_records.api import Record
from werkzeug.local import LocalProxy

from reroils_data.documents import minters
from reroils_data.documents_items.api import DocumentsWithItems
from reroils_data.patrons.api import Patrons
from reroils_data.patrons.fetchers import patron_id_fetcher as fetcher
from reroils_data.patrons.minters import patron_id_minter as minter
from reroils_data.patrons.utils import save_patron


@mock.patch('reroils_data.patrons.utils.confirm_user')
@mock.patch('reroils_data.patrons.utils.send_reset_password_instructions')
@mock.patch('reroils_data.patrons.utils.url_for')
@mock.patch('reroils_record_editor.utils.url_for')
@mock.patch('invenio_indexer.api.RecordIndexer')
@mock.patch('reroils_data.patrons.api.Patrons._get_uuid_pid_by_email')
@mock.patch('reroils_data.patrons.api.Patrons.get_borrowed_documents_pids')
def test_patron(get_borrowed_documents_pids, get_uuid_pid_by_email,
                record_indexer, url_for1, url_for2, send_email, confirm_user,
                app, db, minimal_patron_record, minimal_book_record,
                minimal_item_record):
    """Test patron"""
    InvenioAccounts(app)

    # Convenient references
    security = LocalProxy(lambda: app.extensions['security'])
    datastore = LocalProxy(lambda: security.datastore)

    with app.app_context():

        del minimal_patron_record['pid']
        next, pid = save_patron(
            minimal_patron_record,
            'ptrn',
            fetcher,
            minter,
            record_indexer,
            Record,
            None
        )
        email = minimal_patron_record.get('email')

        # Verify that user exists in app's datastore
        user = datastore.get_user(email)
        assert user

        # hack the return value
        get_uuid_pid_by_email.return_value = pid.object_uuid, pid.id
        patron = Patrons.get_patron_by_email(email)
        assert patron.get('email') == email

        patron = Patrons.get_patron_by_user(user)
        assert patron.get('email') == email

        del(minimal_book_record['pid'])
        rec_uuid = uuid4()
        minters.document_id_minter(rec_uuid, minimal_book_record)
        doc = DocumentsWithItems.create(minimal_book_record, rec_uuid)
        db.session.commit()
        # hack the return value
        get_borrowed_documents_pids.return_value = [doc.get('pid')]
        docs = patron.get_borrowed_documents()
        assert docs[0] == doc
