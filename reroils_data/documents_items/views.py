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

"""Blueprint used for loading templates.

The sole purpose of this blueprint is to ensure that Invenio can find the
templates and static files located in the folders of the same names next to
this file.
"""

from __future__ import absolute_import, print_function

from flask import Blueprint, abort, current_app, redirect, render_template, \
    request, url_for
from flask_login import current_user
from invenio_records_ui.signals import record_viewed

from reroils_data.items.api import Item
from reroils_data.members.api import Member
from reroils_data.patrons.api import Patrons

blueprint = Blueprint(
    'reroils_data_documents_items',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.app_template_filter()
def can_request(item):
    """Check if the current user can request a given item."""
    if current_user.is_authenticated:
        patron = Patrons.get_patron_by_user(current_user)
        if patron:
            patron_barcode = patron.get('barcode')
            item_status = item.get('_circulation', {}).get('status')
            if item_status != 'missing':
                loan = Item.loaned_to_patron(item, patron_barcode)
                request = Item.requested_by_patron(item, patron_barcode)
                if not (request or loan):
                    return True
    return False


@blueprint.app_template_filter()
def number_of_requests(item):
    """Get number of requests for a given item."""
    return Item.number_of_item_requests(item)


def doc_item_view_method(pid, record, template=None, **kwargs):
    r"""Display default view.

    Sends record_viewed signal and renders template.

    :param pid: PID object.
    :param record: Record object.
    :param template: Template to render.
    :param \*\*kwargs: Additional view arguments based on URL rule.
    :returns: The rendered template.
    """
    record_viewed.send(
        current_app._get_current_object(),
        pid=pid,
        record=record,
    )
    members = Member.get_all_members()
    return render_template(
        template,
        pid=pid,
        record=record,
        members=members
    )
