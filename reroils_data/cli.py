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

"""Click command-line interface for record management."""

from __future__ import absolute_import, print_function

import uuid
from random import randint

import click
from flask.cli import with_appcontext


#
# Item management commands
#
@click.group()
def fixtures():
    """Item management commands."""


@fixtures.command()
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option(
    '-c', '--count', 'count', type=click.INT, default=10000,
    help='default=10000'
)
@with_appcontext
def createitems(verbose, count):
    """Create circulation items."""
    from invenio_db import db
    from invenio_indexer.api import RecordIndexer

    from invenio_circulation.api import Item
    from reroils_data.minters import circulation_itemid_minter
    click.secho(
        'Starting generating {0} items...'.format(count),
        fg='green')
    prefixes = ['PA', 'SR', 'RR']
    locations = ['publicAccess', 'storeroom', 'readingRoom']
    for x in range(count):
        id_ = uuid.uuid4()
        call_number = prefixes[randint(0, 2)] + '-' + str(x + 1).zfill(5)
        location = locations[randint(0, 2)]
        data = {
            "barcode": 10000000000 + x,
            "callNumber": call_number,
            "localisation": location
        }
        circulation_itemid_minter(id_, data)
        item = Item.create(data, id_=id_)
        if randint(0, 5) == 0:
            item.loan_item()
        elif randint(0, 20) == 0:
            item.lose_item()
        if verbose:
            click.echo(item.id, item)
        item.commit()
        record_indexer = RecordIndexer()
        record_indexer.index(item)

    db.session.commit()
