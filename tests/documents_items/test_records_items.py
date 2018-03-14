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

from reroils_data.documents_items.api import DocumentsWithItems


def test_create(app, db, minimal_book_record, minimal_item_record):
    """Test RecordsItems creation."""

    with app.app_context():
        doc = DocumentsWithItems.create(minimal_book_record)
        item = Item.create(minimal_item_record)

        doc.add_item(item)
        assert doc.itemslist[0] == item

        dump = doc.dumps()
        assert dump['itemslist'][0] == item.dumps()
