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

from ..api import RecordWithElements
from ..documents.api import Document
from ..documents.fetchers import document_id_fetcher
from ..documents.minters import document_id_minter
from ..documents.providers import DocumentProvider
from ..items.api import Item
from .models import DocumentsItemsMetadata


class DocumentsWithItems(RecordWithElements):
    """Api for Documents with Items."""

    record = Document
    element = Item
    metadata = DocumentsItemsMetadata
    elements_list_name = 'itemslist'
    minter = document_id_minter
    fetcher = document_id_fetcher
    provider = DocumentProvider

    # @property
    # def elements(self):
    #     """Return an array of Items."""
    #     if self.model is None:
    #         raise MissingModelError()
    #     # retrive all items in the relation table
    #     # sorted by item creation date
    #     document_items = self.metadata.query\
    #         .filter_by(document_id=self.id)\
    #         .join(self.metadata.item)\
    #         .order_by(RecordMetadata.created)
    #     to_return = []
    #     for doc_item in document_items:
    #         item = Item.get_record_by_id(doc_item.item.id)
    #         to_return.append(item)
    #     return to_return

    @property
    def itemslist(self):
        """Itemslist."""
        return self.elements

    def add_item(self, item, dbcommit=False, reindex=False):
        """Add an item."""
        super(DocumentsWithItems, self).add_element(
            item,
            dbcommit=dbcommit,
            reindex=reindex
        )

    def remove_item(self, item, force=False, delindex=False):
        """Remove an item."""
        super(DocumentsWithItems, self).remove_element(
            item,
            force=force,
            delindex=delindex
        )

    @classmethod
    def get_document_by_itemid(cls, id_, with_deleted=False):
        """Retrieve the record by id."""
        doc_item = cls.metadata.query.filter_by(item_id=id_).one()
        doc_id = doc_item.document_id
        doc = DocumentsWithItems.get_record_by_id(doc_id)
        return doc
