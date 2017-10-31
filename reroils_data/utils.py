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


def clean_dict_keys(dict_):
    """Remove key having useless values."""
    dict_copy = copy.deepcopy(dict_)

    for key, value in dict_copy.items():
        if isinstance(value, dict):
            value = clean_dict_keys(dict_[key])

        # TODO: refactor
        if value in ([None], [''], [{}], None, '', {}):
            del dict_[key]

        elif isinstance(value, list):
            to_return = []
            for n, item in enumerate(value):
                if isinstance(item, dict):
                    clean_dict_keys(dict_[key][n])
            dict_[key] = [v for v in dict_[key] if v]
            value = dict_[key]
            # TODO: refactor
            if value in ([None], [''], [{}], None, '', {}, []):
                del dict_[key]

    return dict_
