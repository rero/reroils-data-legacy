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

"""Minters module tests."""

from __future__ import absolute_import, print_function

from invenio_circulation.api import Item
from invenio_pidstore.models import PersistentIdentifier
from invenio_records.models import RecordMetadata

from reroils_data.documents_items.api import DocumentsWithItems
from reroils_data.documents_items.models import DocumentsItemsMetadata


def create_item(data):
    """Item creation."""
    from uuid import uuid4
    from reroils_data.items import minters
    if data.get('pid'):
        del(data['pid'])
    rec_uuid = uuid4()
    minters.item_id_minter(rec_uuid, data)
    return Item.create(data, rec_uuid)


def test_create(app, db, minimal_book_record, minimal_item_record):
    """Test DocumentWithItems creation."""
    with app.app_context():
        doc = DocumentsWithItems.create(minimal_book_record)
        item = Item.create(minimal_item_record)
        assert doc.itemslist == []

        doc.add_item(item)
        db.session.commit()
        assert doc.itemslist[0] == item

        dump = doc.dumps()
        assert dump['itemslist'][0] == item.dumps()


def test_delete_item(app, db, minimal_book_record, minimal_item_record):
    """Test DocumentWithItems item deletion."""
    with app.app_context():
        doc = DocumentsWithItems.create(minimal_book_record)
        item = create_item(minimal_item_record)
        doc.add_item(item)
        db.session.commit()
        pid = PersistentIdentifier.get_by_object('item', 'rec', item.id)
        assert pid.is_registered()
        doc.remove_item(item)
        db.session.commit()
        assert pid.is_deleted()
        assert doc.itemslist == []

        minimal_item_record['pid'] = '1'
        item1 = Item.create(minimal_item_record)
        doc.add_item(item1)
        minimal_item_record['pid'] = '2'
        item2 = Item.create(minimal_item_record)
        doc.add_item(item2)
        minimal_item_record['pid'] = '3'
        item3 = Item.create(minimal_item_record)
        doc.add_item(item3)
        db.session.commit()
        doc.remove_item(item2)
        db.session.commit()
        assert len(doc.itemslist) == 2
        assert doc.itemslist[0]['pid'] == '1'
        assert doc.itemslist[1]['pid'] == '3'


def test_delete_document(app, db, minimal_book_record, minimal_item_record):
    """Test DocumentWithItems deletion."""
    with app.app_context():
        doc = DocumentsWithItems.create(minimal_book_record)
        item1 = create_item(minimal_item_record)
        pid1 = PersistentIdentifier.get_by_object('item', 'rec', item1.id)
        item2 = create_item(minimal_item_record)
        pid2 = PersistentIdentifier.get_by_object('item', 'rec', item2.id)
        item3 = create_item(minimal_item_record)
        pid3 = PersistentIdentifier.get_by_object('item', 'rec', item3.id)
        doc.add_item(item1)
        doc.add_item(item2)
        doc.add_item(item3)
        db.session.commit()
        assert DocumentsItemsMetadata.query.count() == 3
        assert RecordMetadata.query.count() == 4
        assert pid1.is_registered()
        assert pid2.is_registered()
        assert pid3.is_registered()
        doc.delete(force=True)
        db.session.commit()
        assert DocumentsItemsMetadata.query.count() == 0
        assert RecordMetadata.query.count() == 0
        assert pid1.is_deleted()
        assert pid2.is_deleted()
        assert pid3.is_deleted()
