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

"""Organisation with Members module tests."""

from __future__ import absolute_import, print_function

from invenio_pidstore.models import PersistentIdentifier
from invenio_records.api import Record
from invenio_records.models import RecordMetadata

from reroils_data.members.api import Member
from reroils_data.organisations_members.api import OrganisationWithMembers
from reroils_data.organisations_members.models import \
    OrganisationsMembersMetadata


def test_organisation_members_create(
            app, db, minimal_organisation_record, minimal_member_record
        ):
    """Test organisation with members creation."""

    with app.app_context():
        org = OrganisationWithMembers.create(minimal_organisation_record)
        memb = Record.create(minimal_member_record)
        assert org.members == []

        org.add_member(memb)
        db.session.commit()
        assert org.members[0] == memb

        dump = org.dumps()
        assert dump['members'][0] == memb.dumps()


def test_delete_member(
            app, db, minimal_organisation_record, minimal_member_record
        ):
    """Test OrganisationsMembers delete."""
    with app.app_context():
        del minimal_organisation_record['pid']
        org = OrganisationWithMembers.create(
            minimal_organisation_record,
            pid=True
        )
        del minimal_member_record['pid']
        member = Member.create(minimal_member_record, pid=True)
        org.add_member(member)
        db.session.commit()
        pid = PersistentIdentifier.get_by_object('memb', 'rec', member.id)
        assert pid.is_registered()
        org.remove_member(member)
        db.session.commit()
        assert pid.is_deleted()
        assert org.members == []

        del minimal_member_record['pid']
        member1 = Member.create(minimal_member_record, pid=True)
        org.add_member(member1)
        del minimal_member_record['pid']
        member2 = Member.create(minimal_member_record, pid=True)
        org.add_member(member2)
        del minimal_member_record['pid']
        member3 = Member.create(minimal_member_record, pid=True)
        org.add_member(member3)
        db.session.commit()
        org.remove_member(member2)
        db.session.commit()
        assert len(org.members) == 2
        assert org.members[0]['pid'] == '2'
        assert org.members[1]['pid'] == '4'


def test_delete_organisation(
            app, db, minimal_organisation_record, minimal_member_record
        ):
    """Test Organisation delete."""
    with app.app_context():
        del minimal_organisation_record['pid']
        org = OrganisationWithMembers.create(
            minimal_organisation_record,
            pid=True
        )
        del minimal_member_record['pid']
        member1 = Member.create(minimal_member_record, pid=True)
        pid1 = PersistentIdentifier.get_by_object('memb', 'rec', member1.id)
        del minimal_member_record['pid']
        member2 = Member.create(minimal_member_record, pid=True)
        pid2 = PersistentIdentifier.get_by_object('memb', 'rec', member2.id)
        del minimal_member_record['pid']
        member3 = Member.create(minimal_member_record, pid=True)
        pid3 = PersistentIdentifier.get_by_object('memb', 'rec', member3.id)
        org.add_member(member1)
        org.add_member(member2)
        org.add_member(member3)
        db.session.commit()
        assert OrganisationsMembersMetadata.query.count() == 3
        assert RecordMetadata.query.count() == 4
        assert pid1.is_registered()
        assert pid2.is_registered()
        assert pid3.is_registered()
        org.delete(force=True)
        db.session.commit()
        assert OrganisationsMembersMetadata.query.count() == 0
        assert RecordMetadata.query.count() == 0
        assert pid1.is_deleted()
        assert pid2.is_deleted()
        assert pid3.is_deleted()
