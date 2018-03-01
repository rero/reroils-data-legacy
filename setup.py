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
        ],
        'invenio_i18n.translations': [
            'messages = reroils_data',
        ],
        'invenio_jsonschemas.schemas': [
            'record = reroils_data.jsonschemas'
        ],
        'dojson.cli': [
            'reverse = reroils_data.cli:reverse',
            'head = reroils_data.cli:head'
        ],
        'dojson.cli.dump': [
            'pjson = reroils_data.dojson.utils:dump'
        ],
        'dojson.cli.rule': [
            'marc21tojson ='
            'reroils_data.dojson.contrib.marc21tojson:marc21tojson',
            'unimarctojson ='
            'reroils_data.dojson.contrib.unimarctojson:unimarctojson',
        ],
        'invenio_search.mappings': [
            'records = reroils_data.mappings',
            'items = reroils_data.mappings',
            'institutions = reroils_data.mappings'
        ],
        'flask.commands': [
            'fixtures = reroils_data.cli:fixtures',
        ],
        'invenio_db.models': [
            'reroils_data = reroils_data.models'
        ],
        # TODO: Edit these entry points to fit your needs.
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        'invenio_pidstore.minters': [
            'bibid = reroils_data.minters:bibid_minter',
            'itemid = reroils_data.minters:circulation_itemid_minter',
            'institutionid = reroils_data.minters:institutionid_minter'
        ],
        'invenio_pidstore.fetchers': [
            'bibid = reroils_data.fetchers:bibid_fetcher',
            'itemid = reroils_data.fetchers:circulation_itemid_fetcher',
            'institutionid = reroils_data.fetchers:institutionid_fetcher'
        ],
        # 'invenio_records.jsonresolver': [],
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
