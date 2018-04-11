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

"""API for manipulating items associated to a document."""

from copy import deepcopy

from invenio_circulation.api import Item
from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record
from invenio_records.errors import MissingModelError
from invenio_records.models import RecordMetadata

from .models import DocumentsItemsMetadata


class ItemsMixin(object):
    """Implement items attribute for Document models.

    .. note::
       This is a prototype.
    """

    def add_item(self, item):
        """Add an Item."""
        DocumentsItemsMetadata.create(document=self.model, item=item.model)

    def remove_item(self, item, force=False):
        """Remove an Item."""
        sql_model = DocumentsItemsMetadata.query.filter_by(
            item_id=item.id, document_id=self.id).first()
        with db.session.begin_nested():
            db.session.delete(sql_model)

            import sys
            sys.stdout.flush()
            try:
                pid = PersistentIdentifier.get_by_object(
                    'item', 'rec', item.id)
                pid.delete()
            except PIDDoesNotExistError:
                pass
            item.delete(force)

    @property
    def itemslist(self):
        """Return an array of Item."""
        if self.model is None:
            raise MissingModelError()
        # retrive all items in the relation table
        # sorted by item creation date
        documents_items = DocumentsItemsMetadata.query\
            .filter_by(document_id=self.id)\
            .join(DocumentsItemsMetadata.item)\
            .order_by(RecordMetadata.created)
        to_return = []
        for doc_item in documents_items:
            item = Item.get_record(doc_item.item.id)
            to_return.append(item)
        return to_return

    @classmethod
    def get_record_by_itemid(cls, id_, with_deleted=False):
        """Retrieve the record by id.

        Raise a database exception if the record does not exist.

        :param id_: record ID.
        :param with_deleted: If `True` then it includes deleted records.
        :returns: The :class:`Record` instance.
        """
        doc_item = DocumentsItemsMetadata.query.filter_by(item_id=id_).one()
        doc_id = doc_item.document_id
        return DocumentsWithItems.get_record(doc_id)


class DocumentsWithItems(Record, ItemsMixin):
    """Define API for files manipulation using ``ItemsMixin``."""

    def dumps(self, **kwargs):
        """Return pure Python dictionary with record metadata."""
        data = deepcopy(dict(self))
        data['itemslist'] = self.itemslist
        return data

    def delete(self, force=False):
        """Delete the document and all the related items."""
        for item in self.itemslist:
            self.remove_item(item, force)
        super(DocumentsWithItems, self).delete(force)

    @classmethod
    def get_record_by_pid(cls, pid_value):
        """Get record by pid value."""
        resolver = Resolver(
            pid_type='doc',
            object_type='rec',
            getter=DocumentsWithItems.get_record
        )
        pid, record = resolver.resolve(pid_value)
        return record
