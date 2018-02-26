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

"""Persistent identifier fetchers."""


from __future__ import absolute_import, print_function

from collections import namedtuple

from invenio_circulation.providers import CirculationItemProvider
from invenio_pidstore.providers.recordid import RecordIdProvider

FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])
"""A pid fetcher."""


def bibid_fetcher(record_uuid, data):
    """Fetch a record's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`reroils_data.fetchers.FetchedPID` instance.
    """
    return FetchedPID(
        provider=RecordIdProvider,
        pid_type=RecordIdProvider.pid_type,
        pid_value=data['bibid']
    )


def circulation_itemid_fetcher(record_uuid, data):
    """Fetch a circulation itemid identifier.

    :param record_uuid: Record UUID.
    :param data: Record content.
    :returns: A :class:``invenio_pidstore.fetchers.FetchedPID`` that contains
        ``data['itemid']`` as pid_value.
    """
    return FetchedPID(
        provider=CirculationItemProvider,
        pid_type=CirculationItemProvider.pid_type,
        pid_value=str(data['itemid']),
    )


def institutionid_fetcher(record_uuid, data):
    """Fetch a institution record's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`reroils_data.fetchers.FetchedPID` instance.
    """
    return FetchedPID(
        provider=RecordIdProvider,
        pid_type=RecordIdProvider.pid_type,
        pid_value=data['institutionid']
    )
