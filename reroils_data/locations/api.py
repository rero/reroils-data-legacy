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

"""API for manipulating locations."""

from uuid import uuid4

from invenio_pidstore.ext import PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record

from reroils_data.members_locations.models import MembersLocationsMetadata

from .fetchers import location_id_fetcher
from .minters import location_id_minter


class Location(Record):
    """Location class."""

    minter = location_id_minter
    fetcher = location_id_fetcher
    record_type = 'loc'

    @classmethod
    def create(cls, data, id_=None, pid=False, **kwargs):
        """Create a new location record."""
        if not id_:
            id_ = uuid4()
        if pid and not cls.get_pid(data):
            cls.minter(id_, data)
        return super(Location, cls).create(data=data, id_=id_, **kwargs)

    @classmethod
    def get_pid(cls, data):
        """Get location pid."""
        try:
            pid_value = cls.fetcher(None, data).pid_value
        except KeyError:
            return None
        return pid_value

    @classmethod
    def get_all_pids(cls):
        """Get all location pids."""
        members_locations = MembersLocationsMetadata.query.all()

        locs_id = []

        for member_location in members_locations:
            loc_id = member_location.location_id
            pid = PersistentIdentifier.get_by_object('loc', 'rec', loc_id)
            locs_id.append(pid.pid_value)

        return locs_id

    @classmethod
    def get_location(cls, pid_value):
        """Get location record with pids."""
        resolver = Resolver(
            pid_type='loc',
            object_type='rec',
            getter=Record.get_record
        )
        pid, location = resolver.resolve(pid_value)
        return pid, location
