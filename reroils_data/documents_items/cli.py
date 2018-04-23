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

import random
from random import randint

import click
from flask.cli import with_appcontext
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PersistentIdentifier

from reroils_data.items.api import Item
from reroils_data.locations.api import Location

from .api import DocumentsWithItems


@click.command('createitems')
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option(
    '-c', '--count', 'count', type=click.INT, default=-1,
    help='default=for all records'
)
@click.option(
    '-i', '--itemscount', 'itemscount', type=click.INT, default=5,
    help='default=1'
)
@with_appcontext
def create_items(verbose, count, itemscount):
    """Create circulation items."""
    records = PersistentIdentifier.query.filter_by(pid_type='doc')
    if count == -1:
        count = records.count()

    click.secho(
        'Starting generating {0} items, random {1} ...'.format(
            count, itemscount),
        fg='green')

    locations_pids = Location.get_all_pids()
    with click.progressbar(records[:count], length=count) as bar:
        for rec in bar:
            document = DocumentsWithItems.get_record_by_id(rec.object_uuid)
            for i in range(0, randint(1, itemscount)):
                item = create_random_item(locations_pids)
                document.add_item(item)
            document.dbcommit(reindex=True)
            RecordIndexer().client.indices.flush()


def create_random_item(locations_pids, verbose=False):
    """Create items with randomised values."""
    item_types = ['standard_loan', 'short_loan', 'no_loan']
    item_type = random.choice(item_types)

    data = {
        'barcode': '????',
        'callNumber': '????',
        'location_pid': random.choice(locations_pids),
        'item_type': random.choice(item_types)
    }
    item = Item.create(data)

    n = int(item.pid)
    data['barcode'] = str(10000000000 + n)
    data['callNumber'] = str(n).zfill(5)
    item.update(data)

    if randint(0, 5) == 0 and item_type != 'no_loan':
        # TODO task 509 patron barcodes to create
        item.loan_item(patron_barcode='1234')
    elif randint(0, 40) == 0:
        item.lose_item()
    item.commit()
    if verbose:
        click.echo(item.id)
    item.dbcommit()
    return item
