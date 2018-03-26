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

"""Utilities functions for reroils-data."""

from flask import current_app, url_for
from flask_security.confirmable import confirm_user
from flask_security.recoverable import send_reset_password_instructions
from invenio_accounts.ext import hash_password
from reroils_record_editor.utils import save_record
from werkzeug.local import LocalProxy

datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


def save_patron(
            data, record_type, fetcher, minter,
            record_indexer, record_class, parent_pid
        ):
    """Save a record into the db and index it.

    If the user does not exists, it well be created
    and attached to the patron.
    """
    email = data.get('email')

    if email:
        find_user = datastore.find_user(email=email)
        if not find_user:
            password = hash_password(email)

            datastore.create_user(
                email=email,
                password=password
            )
            datastore.commit()
            # send password reset
            user = datastore.find_user(email=email)
            if user:
                send_reset_password_instructions(user)
                confirm_user(user)

        _next, pid = save_record(
            data,
            record_type,
            fetcher,
            minter,
            record_indexer,
            record_class,
            parent_pid
        )

    _next = url_for('invenio_records_ui.ptrn', pid_value=pid.pid_value)
    return _next, pid
