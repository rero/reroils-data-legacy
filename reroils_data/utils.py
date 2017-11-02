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

"""Utilites."""

from __future__ import absolute_import, print_function

import copy


def clean_dict_keys(data):
    """Remove key having useless values."""
    # retrun a new list with defined value only
    if isinstance(data, list):
        to_return = []
        for item in data:
            tmp = clean_dict_keys(item)
            if tmp:
                to_return.append(tmp)
        return to_return

    # retrun a new dict with defined value only
    if isinstance(data, dict):
        to_return = {}
        for k, v in data.items():
            tmp = clean_dict_keys(v)
            if tmp:
                to_return[k] = tmp
        return to_return

    return data
