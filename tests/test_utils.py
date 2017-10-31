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

'''Minters module tests.'''

from __future__ import absolute_import, print_function

from reroils_data.utils import clean_dict_keys


def test_clean_dict_keys():
    data = {'languages': [None]}
    assert clean_dict_keys(data) == {}
    data = {
        'title': 'mytitle',
        'languages': [None]
    }
    assert clean_dict_keys(data) == {'title': 'mytitle'}

    data = {
        'title': 'mytitle',
        'translatedFrom': ['']
    }
    assert clean_dict_keys(data) == {'title': 'mytitle'}

    data = {
        'title': 'mytitle',
        'series': [{}]
    }
    assert clean_dict_keys(data) == {'title': 'mytitle'}

    data = {
        'title': 'mytitle',
        'authors': {
            'type': None,
            'date': ''
        }
    }
    assert clean_dict_keys(data) == {'title': 'mytitle'}

    data = {
        'title': 'mytitle',
        'authors': [{
            'type': None,
            'date': ''
          }, {
          }]
    }
    assert clean_dict_keys(data) == {'title': 'mytitle'}

    data = {
        'title': 'mytitle',
        'authors': [{
            'type': 'person',
            'date': ''
          }, {
          }]
    }
    assert clean_dict_keys(data) == {
        'title': 'mytitle',
        'authors': [{'type': 'person'}]
    }

    data = {
        'title': 'mytitle',
        'languages': [None],
        'translatedFrom': [''],
        'authors': [{
            'type': 'person',
            'date': ''
          }, {
          }],
        'titlesProper': [None],
        'publishers': [{
            'name': ['', ''],
            'place': ['']
          },
          {
            'name': [None],
            'place': [None]
          }
        ],
        'formats': [None],
        'series': [{}],
        'notes': [None],
        'abstracts': [None],
        'subjects': [None]
    }
    assert clean_dict_keys(data) == {
        'title': 'mytitle',
        'authors': [{'type': 'person'}]
    }
