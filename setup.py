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

"""rero21 ils data module"""

import os

from setuptools import find_packages, setup
from setuptools.command.egg_info import egg_info

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

class EggInfoWithCompile(egg_info):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog()
        option_dict = self.distribution.get_option_dict('compile_catalog')
        if option_dict.get('domain'):
            compiler.domain = [option_dict['domain'][1]]
        else:
            compiler.domain = ['messages']
        compiler.use_fuzzy = True
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'invenio-pidstore[sqlite]>=1.0.0b2',
    'isort>=4.2.2',
    'jsonschema>=2.5.1',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
    'mock>=2.0.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask-BabelEx>=0.9.2',
    'dojson>=1.3.2',
    'invenio-pidstore>=1.0.0b2',
    'jsonschema>=2.5.1',
    'invenio-db>=1.0.0b6',
    'invenio-jsonschemas>=1.0.0a7',
    'invenio-records>=1.0.0b4',
    'elasticsearch-dsl>=2.0.0,<3.0.0'
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('reroils_data', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    cmdclass={
        'egg_info': EggInfoWithCompile
    },
    name='reroils-data',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio TODO',
    license='GPLv2',
    author='RERO',
    author_email='software@rero.ch',
    url='https://github.com/rero21/reroils-data',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'reroils_data = reroils_data:REROILSDATA',
            'reroils_patron = reroils_data.patrons:REROILSPATRON',
            'reroils_item = reroils_data.items:REROILSITEM',
            'reroils_documents_items = reroils_data.documents_items:REROILSDOCUMENTSITEMS',
        ],
        'invenio_i18n.translations': [
            'messages = reroils_data',
        ],
        'dojson.cli': [
            'reverse = reroils_data.cli:reverse',
            'head = reroils_data.cli:head',
        ],
        'dojson.cli.dump': [
            'pjson = reroils_data.dojson.dump:pretty_json_dump',
        ],
        'dojson.cli.rule': [
            'marc21tojson ='
            'reroils_data.documents.dojson.contrib.marc21tojson:marc21tojson',
            'unimarctojson ='
            'reroils_data.documents.dojson.contrib.unimarctojson:unimarctojson',
        ],
        'flask.commands': [
            'fixtures = reroils_data.cli:fixtures',
            'utils = reroils_data.cli:utils',
        ],
        'invenio_base.blueprints': [
            'organisations = reroils_data.organisations_members.views:blueprint',
            'members = reroils_data.members_locations.views:blueprint',
            'locations = reroils_data.locations.views:blueprint',
            'documents_items = reroils_data.documents_items.views:blueprint',
            'documents = reroils_data.documents.views:blueprint',
            'items = reroils_data.items.views:blueprint',
            'patrons = reroils_data.patrons.views:blueprint',
        ],
        'invenio_db.models': [
            'organisations = reroils_data.organisations.models',
            'organisations_members = reroils_data.organisations_members.models',
            'members = reroils_data.members.models',
            'members_locations = reroils_data.members_locations.models'
            'locations = reroils_data.locations.models',
            'documents = reroils_data.documents.models',
            'documents_items = reroils_data.documents_items.models',
            'items = reroils_data.items.models',
            'patrons = reroils_data.patrons.models',
        ],
        'invenio_pidstore.minters': [
            'organisation_id = reroils_data.organisations.minters:organisation_id_minter',
            'member_id = reroils_data.members.minters:member_id_minter',
            'location_id = reroils_data.locations.minters:location_id_minter',
            'document_id = reroils_data.documents.minters:document_id_minter',
            'item_id = reroils_data.items.minters:item_id_minter',
            'patron_id = reroils_data.patrons.minters:patron_id_minter',
        ],
        'invenio_pidstore.fetchers': [
            'organisation_id = reroils_data.organisations.fetchers:organisation_id_fetcher',
            'member_id = reroils_data.members.fetchers:member_id_fetcher',
            'location_id = reroils_data.locations.fetchers:location_id_fetcher',
            'document_id = reroils_data.documents.fetchers:document_id_fetcher',
            'item_id = reroils_data.items.fetchers:item_id_fetcher',
            'patron_id = reroils_data.patrons.fetchers:patron_id_fetcher',
        ],
        'invenio_jsonschemas.schemas': [
            'organisations = reroils_data.organisations.jsonschemas',
            'members = reroils_data.members.jsonschemas',
            'locations = reroils_data.locations.jsonschemas',
            'documents = reroils_data.documents.jsonschemas',
            'items = reroils_data.items.jsonschemas',
            'patrons = reroils_data.patrons.jsonschemas',
        ],
        'invenio_search.mappings': [
            'organisations = reroils_data.organisations.mappings',
            'members = reroils_data.members.mappings',
            'locations = reroils_data.locations.mappings',
            'documents = reroils_data.documents.mappings',
            'items = reroils_data.items.mappings',
            'patrons = reroils_data.patrons.mappings',
        ],
        'invenio_assets.bundles': [
            'reroils_data_item_editor_js = reroils_data.items.bundles:editor_js',
            'reroils_data_document_editor_js = reroils_data.documents.bundles:editor_js'
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
    ],
)
