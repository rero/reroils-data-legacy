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

from flask import Blueprint, jsonify, render_template, request
from flask_babelex import gettext as _
from flask_menu import register_menu
from invenio_circulation.api import Item
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.resolver import Resolver
from reroils_record_editor.permissions import record_edit_permission

from ..documents_items.api import DocumentsWithItems

blueprint = Blueprint(
    'reroils_data_items',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/items/loan", methods=['POST'])
@record_edit_permission.require()
def loan():
    """HTTP request for Item loan action."""
    try:
        data = request.get_json()
        pid_value = data.pop('pid')
        item_resolver = Resolver(pid_type='item',
                                 object_type='rec',
                                 getter=Item.get_record)
        pid, item = item_resolver.resolve(pid_value)
        doc = DocumentsWithItems.get_record_by_itemid(item.id)
        item.loan_item(**data)
        item.commit()
        db.session.commit()
        # TODO
        # RecordIndexer().index(item)
        RecordIndexer().index(doc)
        RecordIndexer().client.indices.flush()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})


@blueprint.route("/items/return", methods=['POST'])
@record_edit_permission.require()
def return_item():
    """HTTP request for Item return action."""
    try:
        data = request.get_json()
        pid_value = data.pop('pid')
        item_resolver = Resolver(pid_type='item',
                                 object_type='rec',
                                 getter=Item.get_record)
        pid, item = item_resolver.resolve(pid_value)
        doc = DocumentsWithItems.get_record_by_itemid(item.id)
        item.return_item()
        item.commit()
        db.session.commit()
        # TODO
        # RecordIndexer().index(item)
        RecordIndexer().index(doc)
        RecordIndexer().client.indices.flush()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error: %s' % e})


@blueprint.route("/items/circulation")
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
