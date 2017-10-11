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

"""DOJSON module tests."""

from __future__ import absolute_import, print_function

from dojson.contrib.marc21.utils import create_record

from reroils_data.dojson.contrib.marc21tojson import marc21tojson


# title: 245$a
# without the punctuaction. If there's a $b, then 245$a : $b without the " /"
def test_marc21totitle():
    """Test dojson marc21totitle."""

    # subfields $a $b $c
    marc21xml = """
    <record>
      <datafield tag="245" ind1="1" ind2="0">
        <subfield code="a">main title :</subfield>
        <subfield code="b">subtitle /</subfield>
        <subfield code="c">responsability</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('title') == 'main title : subtitle'
    # subfields $a $c
    marc21xml = """
    <record>
      <datafield tag="245" ind1="1" ind2="0">
        <subfield code="a">main title</subfield>
        <subfield code="c">responsability</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('title') == 'main title'
    # subfield $a
    marc21xml = """
    <record>
      <datafield tag="245" ind1="1" ind2="0">
        <subfield code="a">main title</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('title') == 'main title'


# titleProper: [730$a repetitive]
def test_marc21totitlesProper():
    """Test dojson marc21titlesProper."""

    marc21xml = """
    <record>
      <datafield tag="730" ind1="1" ind2="0">
        <subfield code="a">proper title</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('titlesProper') == ['proper title']

    marc21xml = """
    <record>
      <datafield tag="730" ind1=" " ind2=" ">
        <subfield code="a">proper title</subfield>
      </datafield>
      <datafield tag="730" ind1=" " ind2=" ">
         <subfield code="a">other proper title</subfield>
       </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('titlesProper') == ['proper title', 'other proper title']


# languages: 008 and 041 [$a, repetitive]
# translatedFrom: 041 [$h repetitive]
def test_marc21languages():
    """Test dojson marc21languages."""

    marc21xml = """
    <record>
      <controlfield tag="008">
        881005s1984    xxu|||||| ||||00|| |ara d
      <controlfield>
      <datafield tag="041" ind1=" " ind2=" ">
        <subfield code="a">eng</subfield>
        <subfield code="h">ita</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('languages') == ['ara', 'eng']
    assert data.get('translatedFrom') == ['ita']

    marc21xml = """
    <record>
      <controlfield tag="008">
        881005s1984    xxu|||||| ||||00|| |ara d
      <controlfield>
      <datafield tag="041" ind1=" " ind2=" ">
        <subfield code="a">eng</subfield>
        <subfield code="a">fra</subfield>
        <subfield code="h">ita</subfield>
        <subfield code="h">ger</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('languages') == ['ara', 'eng', 'fra']
    assert data.get('translatedFrom') == ['ita', 'ger']

    marc21xml = """
    <record>
      <controlfield tag="008">
        881005s1984    xxu|||||| ||||00|| |ara d
      <controlfield>
      <datafield tag="041" ind1=" " ind2=" ">
        <subfield code="a">eng</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('languages') == ['ara', 'eng']
    assert 'translatedFrom' not in data


# authors: loop:
# authors.name: 100$a [+ 100$b if it exists] or
#   [700$a (+$b if it exists) repetitive] or
#   [ 710$a repetitive (+$b if it exists, repetitive)]
# authors.date: 100 $d or 700 $d (facultatif)
# authors.qualifier: 100 $c or 700 $c (facultatif)
# authors.type: if 100 or 700 then person, if 710 then organisation
def test_marc21toauthors():
    """Test dojson marc21toauthors."""

    marc21xml = """
    <record>
      <datafield tag="100" ind1=" " ind2=" ">
        <subfield code="a">Jean-Paul</subfield>
        <subfield code="b">II</subfield>
        <subfield code="c">Pape</subfield>
        <subfield code="d">1954 -</subfield>
      </datafield>
      <datafield tag="700" ind1=" " ind2=" ">
        <subfield code="a">Dumont, Jean</subfield>
        <subfield code="c">Historien</subfield>
        <subfield code="d">1921 - 2014</subfield>
      </datafield>
      <datafield tag="710" ind1=" " ind2=" ">
        <subfield code="a">RERO</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    authors = data.get('authors')
    assert authors == [
        {
            'name': 'Jean-Paul II',
            'type': 'person',
            'date': '1954 -',
            'qualifier': 'Pape'
        },
        {
            'name': 'Dumont, Jean',
            'type': 'person',
            'date': '1921 - 2014',
            'qualifier': 'Historien'
        },
        {
            'name': 'RERO',
            'type': 'organisation'
        }
    ]


# publishers.name: 260 [$b repetitive] (without the , but keep the ;)
# publishers.place: 260 [$a repetitive] (without the : but keep the ;)
# publicationDate: 260 [$c repetitive] (but take only the first one)
def test_marc21publishers_publicationDate():
    """Test dojson publishers publicationDate."""

    marc21xml = """
    <record>
      <datafield tag="260" ind1=" " ind2=" ">
        <subfield code="a">Lausanne :</subfield>
        <subfield code="b">Payot,</subfield>
        <subfield code="c">2015</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('publishers') == [
        {
            'place': ['Lausanne'],
            'name': ['Payot'],
        }
    ]
    assert data.get('publicationDate') == '2015'

    marc21xml = """
    <record>
      <datafield tag="260" ind1=" " ind2=" ">
        <subfield code="a">Paris ;</subfield>
        <subfield code="a">Lausanne :</subfield>
        <subfield code="b">Payot,</subfield>
        <subfield code="c">1920</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('publishers') == [
        {
            'place': ['Paris', 'Lausanne'],
            'name': ['Payot'],
        }
    ]
    assert data.get('publicationDate') == '1920'

    marc21xml = """
    <record>
      <datafield tag="260" ind1=" " ind2=" ">
        <subfield code="a">Paris :</subfield>
        <subfield code="b">Champion ;</subfield>
        <subfield code="a">Genève :</subfield>
        <subfield code="b">Droz,</subfield>
        <subfield code="c">1912-1955</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('publishers') == [
        {
            'place': ['Paris'],
            'name': ['Champion']
        },
        {
            'place': ['Genève'],
            'name': ['Droz']
        }
    ]
    assert data.get('publicationDate') == '1912-1955'


# extent: 300$a (the first one if many)
# otherMaterialCharacteristics: 300$b (the first one if many)
# formats: 300 [$c repetitive]
def test_marc21description():
    """Test dojson extent, otherMaterialCharacteristics, formats."""

    marc21xml = """
    <record>
      <datafield tag="300" ind1=" " ind2=" ">
        <subfield code="a">116 p.</subfield>
        <subfield code="b">ill.</subfield>
        <subfield code="c">22 cm</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('extent') == '116 p.'
    assert data.get('otherMaterialCharacteristics') == 'ill.'
    assert data.get('formats') == ['22 cm']

    marc21xml = """
    <record>
      <datafield tag="300" ind1=" " ind2=" ">
        <subfield code="a">116 p.</subfield>
        <subfield code="b">ill.</subfield>
        <subfield code="c">22 cm</subfield>
        <subfield code="c">12 x 15</subfield>
      </datafield>
      <datafield tag="300" ind1=" " ind2=" ">
        <subfield code="a">200 p.</subfield>
        <subfield code="b">ill.</subfield>
        <subfield code="c">19 cm</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('extent') == '116 p.'
    assert data.get('otherMaterialCharacteristics') == 'ill.'
    assert data.get('formats') == ['22 cm', '12 x 15']


# series.name: [490$a repetitive]
# series.number: [490$v repetitive]
def test_marc21series():
    """Test dojson series."""

    marc21xml = """
    <record>
      <datafield tag="490" ind1=" " ind2=" ">
        <subfield code="a">Collection One</subfield>
        <subfield code="v">5</subfield>
      </datafield>
      <datafield tag="490" ind1=" " ind2=" ">
        <subfield code="a">Collection Two</subfield>
        <subfield code="v">123</subfield>
      </datafield>    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('series') == [
        {
            'name': 'Collection One',
            'number': '5'
        },
        {
            'name': 'Collection Two',
            'number': '123'
        }
    ]


# abstract: [520$a repetitive]
def test_marc21abstract():
    """Test dojson abstract."""

    marc21xml = """
    <record>
      <datafield tag="520" ind1=" " ind2=" ">
        <subfield code="a">This book is about</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('abstracts') == ["This book is about"]


# identifiers:reroID: 035$a
# identifiers:isbn: 020$a
def test_marc21identifiers():
    """Test dojson identifiers."""

    marc21xml = """
    <record>
      <datafield tag="035" ind1=" " ind2=" ">
        <subfield code="a">R123456789</subfield>
      </datafield>
      <datafield tag="020" ind1=" " ind2=" ">
        <subfield code="a">ISBN123456789</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('identifiers') == {
        'reroID': 'R123456789',
        'isbn': 'ISBN123456789'
    }


# notes: [500$a repetitive]
def test_marc21notes():
    """Test dojson notes."""

    marc21xml = """
    <record>
      <datafield tag="500" ind1=" " ind2=" ">
        <subfield code="a">note 1</subfield>
      </datafield>
      <datafield tag="500" ind1=" " ind2=" ">
        <subfield code="a">note 2</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('notes') == ['note 1', 'note 2']


# subjects: 6xx [duplicates could exist between several vocabularies,
# if possible deduplicate]
def test_marc21subjects():
    """Test dojson subjects."""

    marc21xml = """
    <record>
      <datafield tag="600" ind1=" " ind2=" ">
        <subfield code="a">subjects 600</subfield>
      </datafield>
      <datafield tag="666" ind1=" " ind2=" ">
        <subfield code="a">subjects 666</subfield>
      </datafield>
    </record>
    """
    marc21json = create_record(marc21xml)
    data = marc21tojson.do(marc21json)
    assert data.get('subjects') == ['subjects 600', 'subjects 666']
