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

"""Utilities functions for reroils-data."""

from flask import url_for

from ..documents_items.api import DocumentsWithItems
from ..items.api import Item


def delete_item(record_type, pid, record_indexer, parent_pid):
    """Remove an item from a document.

    The item is marked as deleted in the db, his pid as well.
    The document is reindexed.
    """
    document = DocumentsWithItems.get_record_by_pid(parent_pid)
    item = Item.get_record_by_pid(pid)
    persistent_identifier = item.persistent_identifier
    document.remove_item(item, delindex=True)

    _next = url_for('invenio_records_ui.doc', pid_value=parent_pid)
    return _next, persistent_identifier


def save_item(data, record_type, fetcher, minter,
              record_indexer, record_class, parent_pid):
    """Save a record into the db and index it.

    If the item does not exists, it well be created
    and attached to the parent document.
    """
    document = DocumentsWithItems.get_record_by_pid(parent_pid)
    pid = data.get('pid')
    if pid:
        item = Item.get_record_by_pid(pid)
        item.update(data, dbcommit=True, reindex=True)
    else:
        item = Item.create(data, dbcommit=True, reindex=True)
        document.add_item(item, dbcommit=True, reindex=True)
    _next = url_for('invenio_records_ui.doc', pid_value=parent_pid)
    return _next, item.persistent_identifier
