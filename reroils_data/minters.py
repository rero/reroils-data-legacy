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

"""Identifier minters."""

from __future__ import absolute_import, print_function, unicode_literals

from invenio_circulation.providers import CirculationItemProvider
from invenio_pidstore.providers.recordid import RecordIdProvider


def bibid_minter(record_uuid, data):
    """RERIOLS bibid minter."""
    assert 'bibid' not in data
    provider = RecordIdProvider.create(
        object_type='rec',
        object_uuid=record_uuid
    )
    pid = provider.pid
    data['bibid'] = pid.pid_value

    return pid


def circulation_itemid_minter(record_uuid, data):
    """Mint a circulation itemid identifier."""
    assert 'itemid' not in data
    provider = CirculationItemProvider.create(
        object_type='rec',
        object_uuid=record_uuid
    )
    data['itemid'] = provider.pid.pid_value

    return provider.pid


def institutionid_minter(record_uuid, data):
    """RERIOLS institutionid minter."""
    assert 'institutionid' not in data
    provider = RecordIdProvider.create(
        object_type='rec',
        object_uuid=record_uuid
    )
    pid = provider.pid
    data['institutionid'] = pid.pid_value

    return pid
