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

import json

import click
from flask.cli import with_appcontext
from invenio_db import db
from invenio_indexer.api import RecordIndexer

from reroils_data.locations.api import Location
from reroils_data.organisations_members.api import OrganisationWithMembers

from .api import MemberWithLocations


@click.command('importorganisations')
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.argument('infile', 'Json organisation file', type=click.File('r'))
@with_appcontext
def import_organisations(infile, verbose):
    """Import organisation."""
    click.secho(
        'Import organisations:',
        fg='green'
    )

    record_indexer = RecordIndexer()
    data = json.load(infile)
    for organisation in data:
        if verbose:
            click.echo('\tOrganisation: ' + organisation.get('name'))
        members = organisation.get('members', [])
        del organisation['members']
        org = OrganisationWithMembers.create(organisation, pid=True)
        for member in members:
            if verbose:
                click.echo('\t\tMember: ' + member.get('name'))
            locations = member.get('locations', [])
            del member['locations']
            memb = MemberWithLocations.create(member, pid=True)
            org.add_member(memb)
            for location in locations:
                if verbose:
                    click.echo('\t\t\tLocation: ' + location.get('name'))
                loc = Location.create(location, pid=True)
                memb.add_location(loc)
                record_indexer.index(loc)
            record_indexer.index(memb)
        db.session.commit()
        record_indexer.index(org)
        record_indexer.client.indices.flush()
