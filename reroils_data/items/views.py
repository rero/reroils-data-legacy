# -*- coding: utf-8 -*-
#
# This file is part of items.
# Copyright (C) 2018 RERO.
#

"""Blueprint used for loading templates.

The sole purpose of this blueprint is to ensure that Invenio can find the
templates and static files located in the folders of the same names next to
this file.
"""

from __future__ import absolute_import, print_function

from datetime import datetime, timedelta

from flask import Blueprint, flash, jsonify, redirect, render_template, \
    request, url_for
from flask_babelex import gettext as _
from flask_login import current_user
from flask_menu import register_menu
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.resolver import Resolver
from reroils_record_editor.permissions import record_edit_permission

from reroils_data.items.api import Item

from ..documents_items.api import DocumentsWithItems
from ..patrons.api import Patron
from .utils import commit_item, item_from_web_request, request_start_end_date

blueprint = Blueprint(
    'reroils_data_items',
    __name__,
    url_prefix='/items',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/loan", methods=['POST', 'PUT'])
@record_edit_permission.require()
def loan_item():
    """HTTP request for Item loan action."""
    try:
        data = request.get_json()
        item = item_from_web_request(data)
        item.loan_item(**data)
        commit_item(item)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})


@blueprint.route("/return", methods=['POST', 'PUT'])
@record_edit_permission.require()
def return_item():
    """HTTP request for Item return action."""
    try:
        data = request.get_json()
        item = item_from_web_request(data)
        item.return_item()
        commit_item(item)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})


@blueprint.route("/return_missing", methods=['POST', 'PUT'])
@record_edit_permission.require()
def return_missing_item():
    """HTTP request for Item return_missing action."""
    try:
        data = request.get_json()
        item = item_from_web_request(data)
        item.return_missing_item()
        commit_item(item)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})


@blueprint.route("/extend", methods=['POST', 'PUT'])
@record_edit_permission.require()
def extend_loan():
    """HTTP request for Item due date extend action."""
    try:
        data = request.get_json()
        requested_end_date = data.get('end_date')
        renewal_count = data.get('renewal_count')
        item = item_from_web_request(data)
        extend_data = {
            'requested_end_date': requested_end_date,
            'renewal_count': renewal_count,
        }
        item.extend_loan(extend_data)
        commit_item(item)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})


@blueprint.route("/request/<pid_value>/<member>", methods=['GET'])
def request_item(pid_value, member):
    """HTTP GET request for Item request action."""
    try:
        patron = Patron.get_patron_by_email(current_user.email)
        patron_barcode = patron['barcode']
        start_date, end_date = request_start_end_date()
        item_resolver = Resolver(pid_type='item',
                                 object_type='rec',
                                 getter=Item.get_record)
        pid, item = item_resolver.resolve(pid_value)
        doc = DocumentsWithItems.get_document_by_itemid(item.id)
        item.request_item(
            patron_barcode=patron_barcode,
            pickup_member_pid=member,
            start_date=start_date,
            end_date=end_date
        )
        commit_item(item)
        flash(_('The item %s has been requested.' % pid_value), 'success')
        return redirect(
            url_for('invenio_records_ui.doc', pid_value=doc['pid'])
        )
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})
        flash(_('Something went wrong'), 'danger')


@blueprint.route("/circulation")
@record_edit_permission.require()
@register_menu(
    blueprint,
    'main.manage.circulation',
    _('%(icon)s Circulation', icon='<i class="fa fa-barcode fa-fw"></i>'),
    order=-1
)
def circulation_ui():
    """Angular circulation application."""
    return render_template('reroils_data/circulation_ui.html')
