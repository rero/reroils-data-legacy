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

"""API for manipulating organisation."""

from uuid import uuid4

from invenio_records.api import Record

from .fetchers import member_id_fetcher
from .minters import member_id_minter


class Member(Record):
    """Member class."""

    minter = member_id_minter
    fetcher = member_id_fetcher
    record_type = 'memb'

    @classmethod
    def create(cls, data, id_=None, pid=False, **kwargs):
        """Create a new Member record."""
        if not id_:
            id_ = uuid4()
        if pid and not cls.get_pid(data):
            cls.minter(id_, data)
        return super(Member, cls).create(data=data, id_=id_, **kwargs)

    @classmethod
    def get_pid(cls, data):
        """Get member pid."""
        try:
            pid_value = cls.fetcher(None, data).pid_value
        except KeyError:
            return None
        return pid_value
