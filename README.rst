..
    This file is part of Invenio.
    Copyright (C) 2017 RERO.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, RERO does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

==============
 REROILS-DATA
==============

.. image:: https://img.shields.io/travis/rero21/reroils-data.svg
        :target: https://travis-ci.org/rero21/reroils-data

.. image:: https://img.shields.io/coveralls/rero21/reroils-data.svg
        :target: https://coveralls.io/r/rero21/reroils-data

.. image:: https://img.shields.io/github/tag/rero21/reroils-data.svg
        :target: https://github.com/rero21/reroils-data/releases

.. image:: https://img.shields.io/pypi/dm/reroils-data.svg
        :target: https://pypi.python.org/pypi/reroils-data

.. image:: https://img.shields.io/github/license/rero21/reroils-data.svg
        :target: https://github.com/rero21/reroils-data/blob/master/LICENSE

rero21 ils data module

*This is an experimental developer preview release.*

TODO: Please provide feature overview of module

Further documentation is available on
https://reroils-data.readthedocs.io/


DOJSON
======

MARC21 to JSON
--------------

MARC21 to MARCXML
.................

.. code:: console

    yaz-marcdump -o marcxml MARC21.mrc > MARCXML.xml

MARCXML to JSON
...............

dojson help
~~~~~~~~~~~

.. code:: console

    dojson --help

create json file
~~~~~~~~~~~~~~~~

.. code:: console

   dojson -l marcxml -i MARCXML.xml do marc21tojson > REROILS.json

show missing tags
~~~~~~~~~~~~~~~~~

.. code:: console

    dojson -l marcxml -i MARCXML.xml missing marc21tojson

validate with json schema
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    dojson -l marcxml -i MARCXML.xml do marc21tojson validate ./reroils_data/jsonschemas/records/record-v0.0.1.json
