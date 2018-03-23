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

"""Click command-line utilities."""

from __future__ import absolute_import, print_function

import json
import re
from pathlib import Path

import click
from flask import current_app
from flask.cli import with_appcontext
from flask_security.confirmable import confirm_user
from invenio_accounts.cli import commit, users
from invenio_pidstore.models import PersistentIdentifier
from werkzeug.local import LocalProxy

from .documents_items.cli import create_items
from .members_locations.cli import import_organisations

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


@click.group()
def fixtures():
    """Fixtures management commands."""

fixtures.add_command(import_organisations)
fixtures.add_command(create_items)


@click.command('reverse')
def reverse():
    """Reverse the order of the data."""
    def processor(iterator):
        items = []
        for item in iterator:
            items.append(item)
        items.reverse()
        return items

    return processor


@click.command('head')
@click.argument('max', type=click.INT,)
def head(max):
    """Take only the first max items."""
    def processor(iterator):
        n = 0
        for item in iterator:
            if n >= max:
                raise StopIteration
            n += 1
            yield item

    return processor


@users.command('confirm')
@click.argument('user')
@with_appcontext
@commit
def manual_confirm_user(user):
    """Confirm a user."""
    user_obj = _datastore.get_user(user)
    if user_obj is None:
        raise click.UsageError('ERROR: User not found.')
    if confirm_user(user_obj):
        click.secho('User "%s" has been confirmed.' % user, fg='green')
    else:
        click.secho('User "%s" was already confirmed.' % user, fg='yellow')


@click.group()
def utils():
    """Misc management commands."""


@utils.command()
@click.argument('pid_value', nargs=1)
@click.option('-t', '--pid-type', 'pid-type, default(document_id)',
              default='document_id')
@with_appcontext
def show(pid_value, pid_type):
    """Show records."""
    record = PersistentIdentifier.query.filter_by(pid_type=pid_type,
                                                  pid_value=pid_value).first()
    recitem = Record.get_record(record.object_uuid)
    click.echo(json.dumps(recitem.dumps(), indent=2))


@utils.command()
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option(
    '-f', '--file', 'fname', type=click.STRING, default='',
    help='default=for all files in project'
)
@with_appcontext
def check_json(verbose, fname):
    """Check json files."""
    file_list = []
    if not fname:
        path = Path('.')
        file_list = list(path.glob('**/*.json'))
    else:
        path = Path(fname)
        file_list = [path]
    re_sub = re.compile('\s{4}')
    re_match = re.compile('^\s+')
    tot_error_cnt = 0
    for path_file in file_list:
        fname = str(path_file)
        opened_file = path_file.open()
        row_cnt = 0
        error_cnt = 0
        for row in opened_file:
            stripped_row = row.rstrip()
            new_row = re_sub.sub('', stripped_row)
            if re_match.match(new_row):
                if verbose:
                    click.echo(fname + ':' + str(row_cnt) + ': ', nl=False)
                    click.secho(stripped_row, fg='red')
                error_cnt += 1
            row_cnt += 1
        click.echo(fname + ': ', nl=False)
        if error_cnt == 0:
            click.secho('OK', fg='green')
        else:
            click.secho('NOT Ok', fg='red')
        tot_error_cnt += error_cnt
    return tot_error_cnt
