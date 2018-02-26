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

"""Minters module tests."""

from __future__ import absolute_import, print_function

from uuid import uuid4

from reroils_data import minters


def test_bibid_minter(app, db):
    """Test bibid minter."""

    with app.app_context():
        data = {}
        # first record
        rec_uuid = uuid4()
        pid = minters.bibid_minter(rec_uuid, data)
        assert pid
        assert data['bibid'] == pid.pid_value
        assert pid.object_type == 'rec'
        assert pid.object_uuid == rec_uuid


def test_circulation_itemid_minter(app, db):
    """Test circulation itemid minter."""

    with app.app_context():
        data = {}
        # first record
        rec_uuid = uuid4()
        pid = minters.circulation_itemid_minter(rec_uuid, data)
        assert pid
        assert data['itemid'] == pid.pid_value
        assert pid.object_type == 'rec'
        assert pid.object_uuid == rec_uuid


def test_institutionid_minter(app, db):
    """Test institutionid minter."""

    with app.app_context():
        data = {}
        # first record
        rec_uuid = uuid4()
        pid = minters.institutionid_minter(rec_uuid, data)
        assert pid
        assert data['institutionid'] == pid.pid_value
        assert pid.object_type == 'rec'
        assert pid.object_uuid == rec_uuid
