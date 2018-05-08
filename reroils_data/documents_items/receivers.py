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

"""REROILS documents items receivers."""

from reroils_data.locations.api import Location


def documents_items_receiver(sender, json, doc_type, index, record):
    """To add the location name according to the location pid."""
    if doc_type == 'book-v0.0.1' and json.get('itemslist'):
        for item in json.get('itemslist'):
            try:
                pid, location = Location.get_location(item.get('location_pid'))
                item['location_name'] = location.get('name')
            except Exception:
                pass
