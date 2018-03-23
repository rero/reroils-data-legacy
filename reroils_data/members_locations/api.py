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

"""API for manipulating locations associated to a members."""

from copy import deepcopy

from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier
from invenio_records.api import Record
from invenio_records.errors import MissingModelError
from invenio_records.models import RecordMetadata

from ..members.api import Member
from ..organisations_members.models import OrganisationsMembersMetadata
from .models import MembersLocationsMetadata


class LocationMixin(object):
    """Implement location attribute for member models.

    .. note::
       This is a prototype.
    """

    def add_location(self, location):
        """Add an Location."""
        MembersLocationsMetadata.create(
            member=self.model,
            location=location.model
        )

    def remove_location(self, location, force=False):
        """Remove an Location."""
        sql_model = MembersLocationsMetadata.query.filter_by(
            location_id=location.id, member_id=self.id).first()
        with db.session.begin_nested():
            db.session.delete(sql_model)

            import sys
            sys.stdout.flush()
            try:
                pid = PersistentIdentifier.get_by_object(
                    'loc', 'rec', location.id)
                pid.delete()
            except PIDDoesNotExistError:
                pass
            location.delete(force)

    @property
    def locations(self):
        """Return an array of Locations."""
        if self.model is None:
            raise MissingModelError()

        # retrive all members in the relation table
        # sorted by members creation date
        members_locations = MembersLocationsMetadata.query\
            .filter_by(member_id=self.id)\
            .join(MembersLocationsMetadata.location)\
            .order_by(RecordMetadata.created)
        to_return = []
        for memb_loc in members_locations:
            location = Record.get_record(memb_loc.location.id)
            to_return.append(location)
        return to_return


class MemberWithLocations(Member, LocationMixin):
    """Define API for files manipulation using ``LocationMixin``."""

    def dumps(self, **kwargs):
        """Return pure Python dictionary with record metadata."""
        data = deepcopy(dict(self))
        data['locations'] = self.locations
        return data

    def delete(self, force=False):
        """Delete the member and all the related locations."""
        for location in self.locations:
            self.remove_location(location, force)
        super(MemberWithLocations, self).delete(force)
