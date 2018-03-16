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

"""API for manipulating members associated to a organisation."""

from copy import deepcopy

from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier
from invenio_records.api import Record
from invenio_records.errors import MissingModelError
from invenio_records.models import RecordMetadata

from ..organisations.api import Organisation
from .models import OrganisationsMembersMetadata


class MembersMixin(object):
    """Implement members attribute for organisation models.

    .. note::
       This is a prototype.
    """

    def add_member(self, member):
        """Add an Member."""
        OrganisationsMembersMetadata.create(
            organisation=self.model,
            member=member.model
        )

    def remove_member(self, member, force=False):
        """Remove an Member."""
        sql_model = OrganisationsMembersMetadata.query.filter_by(
            member_id=member.id, organisation_id=self.id).first()
        with db.session.begin_nested():
            db.session.delete(sql_model)

            import sys
            sys.stdout.flush()
            try:
                pid = PersistentIdentifier.get_by_object(
                    'memb', 'rec', member.id)
                pid.delete()
            except PIDDoesNotExistError:
                pass
            member.delete(force)

    @property
    def members(self):
        """Return an array of Members."""
        if self.model is None:
            raise MissingModelError()

        # retrive all members in the relation table
        # sorted by members creation date
        organisations_members = OrganisationsMembersMetadata.query\
            .filter_by(organisation_id=self.id)\
            .join(OrganisationsMembersMetadata.member)\
            .order_by(RecordMetadata.created)
        to_return = []
        for org_memb in organisations_members:
            member = Record.get_record(org_memb.member.id)
            to_return.append(member)
        return to_return

    @classmethod
    def get_pid(cls, data):
        """Get organisation with member pid."""
        try:
            pid_value = cls.fetcher(None, data).pid_value
        except KeyError:
            return None
        return pid_value


class OrganisationWithMembers(Organisation, MembersMixin):
    """Define API for files manipulation using ``MembersMixin``."""

    def dumps(self, **kwargs):
        """Return pure Python dictionary with record metadata."""
        data = deepcopy(dict(self))
        data['members'] = self.members
        return data

    def delete(self, force=False):
        """Delete the organisation and all the related members."""
        for member in self.members:
            self.remove_member(member, force)
        super(OrganisationWithMembers, self).delete(force)
