# -*- coding: utf-8 -*-
#
# This file is part of BiblioMedia-Data
# Copyright (C) 2016 RERO.
#
# BiblioMedia-Data is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Bibliomedia MARC21 model definition."""

from dojson import Overdo, utils
from dojson.utils import force_list

marc21tojson = Overdo()


def remove_punctuation(data):
    """Remove punctuation from data."""
    if data[-1:] == ',':
        data = data[:-1]
    if data[-2:] == ' :':
        data = data[:-2]
    if data[-2:] == ' ;':
        data = data[:-2]
    if data[-2:] == ' /':
        data = data[:-2]
    return data


# @marc21tojson.over('__order__', '__order__')
# def order(self, key, value):
#     """Preserve order of datafields."""
#     order = []
#     for field in value:
#         name = marc21tojson.index.query(field)
#         if name:
#             name = name[0]
#         else:
#             name = field
#         order.append(name)
#
#     return order


@marc21tojson.over('title', '^245..')
@utils.ignore_value
def marc21totitle(self, key, value):
    """Get title.

    title: 245$a
    without the punctuaction. If there's a $b, then 245$a : $b without the " /"
    """
    main_title = value.get('a')
    sub_title = value.get('b')
    # responsability = value.get('c')
    if sub_title:
        if type(sub_title) == str:
            main_title += ' ' + remove_punctuation(sub_title)
        else:
            for item in sub_title:
                main_title += ' ' + remove_punctuation(item)
    return main_title


@marc21tojson.over('titlesProper', '^730..')
@utils.for_each_value
@utils.ignore_value
def marc21totitlesProper(self, key, value):
    """Test dojson marc21titlesProper.

    titleProper: 730$a
    """
    return value.get('a')


@marc21tojson.over('languages', '^008')
@utils.ignore_value
def marc21languages(self, key, value):
    """Get languages.

    languages: 008 and 041 [$a, repetitive]
    """
    language = value.strip()[35:38]
    return [language]


@marc21tojson.over('translatedFrom', '^041..')
@utils.ignore_value
def marc21translatedFrom(self, key, value):
    """Get translatedFrom.

    translatedFrom: 041 [$h repetitive]
    languages: 008 and 041 [$a, repetitive]
    """
    languages = self.get('languages', [])
    language = value.get('a')
    if language:
        for lang in utils.force_list(language):
            languages.append(lang)
    translated = value.get('h')
    if translated:
        return list(utils.force_list(translated))
    else:
        return None


@marc21tojson.over('authors', '[17][01]0..')
@utils.for_each_value
@utils.ignore_value
def marc21toauthor(self, key, value):
    """Get author.

    authors: loop:
    authors.name: 100$a [+ 100$b if it exists] or
        [700$a (+$b if it exists) repetitive] or
        [ 710$a repetitive (+$b if it exists, repetitive)]
    authors.date: 100 $d or 700 $d (facultatif)
    authors.qualifier: 100 $c or 700 $c (facultatif)
    authors.type: if 100 or 700 then person, if 710 then organisation
    """
    author = {}
    author['name'] = value.get('a')
    author_sub = value.get('b')
    if author_sub:
        author['name'] += ' ' + ' '.join(utils.force_list(author_sub))
    author['type'] = 'person'
    if key[:3] == '710':
        author['type'] = 'organisation'
    if value.get('c'):
        author['qualifier'] = value.get('c')
    if value.get('d'):
        author['date'] = value.get('d')
    return author


@marc21tojson.over('publishers', '^260..')
@utils.ignore_value
def marc21publishers_publicationDate(self, key, value):
    """Get publisher.

    publisher.name: 260 [$b repetitive] (without the , but keep the ;)
    publisher.place: 260 [$a repetitive] (without the : but keep the ;)
    publicationDate: 260 [$c repetitive] (but take only the first one)
    """
    lasttag = '?'
    publishers = self.get('publishers', [])

    publisher = {}
    indexes = {}
    lasttag = '?'
    for tag in value['__order__']:
        index = indexes.get(tag, 0)
        data = value[tag]
        if type(data) == tuple:
            data = data[index]
        if tag == 'a' and index > 0 and lasttag != 'a':
            publishers.append(publisher)
            publisher = {}
        if tag == 'a':
            place = publisher.get('place', [])
            place.append(remove_punctuation(data))
            publisher['place'] = place
        elif tag == 'b':
            name = publisher.get('name', [])
            name.append(remove_punctuation(data))
            publisher['name'] = name
        elif tag == 'c' and index == 0:
            self['publicationDate'] = data
        indexes[tag] = index + 1
        lasttag = tag
    publishers.append(publisher)
    return publishers


@marc21tojson.over('formats', '^300..')
@utils.ignore_value
def marc21description(self, key, value):
    """Get extent, otherMaterialCharacteristics, formats.

    extent: 300$a (the first one if many)
    otherMaterialCharacteristics: 300$b (the first one if many)
    formats: 300 [$c repetitive]
    """
    if value.get('a'):
        if not self.get('extent', None):
            self['extent'] = value.get('a')
    if value.get('b'):
        if self.get('otherMaterialCharacteristics', []) == []:
            self['otherMaterialCharacteristics'] = value.get('b')
    if value.get('c'):
        formats = self.get('formats', [])
        if formats == []:
            data = value.get('c')
            if data:
                if type(value.get('c')) == str:
                    formats.append(data)
                else:
                    for item in data:
                        formats.append(item)
        return formats
    else:
        return None


@marc21tojson.over('series', '^490..')
@utils.for_each_value
@utils.ignore_value
def marc21series(self, key, value):
    """Get series.

    series.name: [490$a repetitive]
    series.number: [490$v repetitive]
    """
    series = {}
    name = value.get('a')
    if name:
        series['name'] = ', '.join(utils.force_list(name))
    number = value.get('v')
    if number:
        series['number'] = ', '.join(utils.force_list(number))
    return series


@marc21tojson.over('abstracts', '^520..')
@utils.for_each_value
@utils.ignore_value
def marc21abstracts(self, key, value):
    """Get abstracts.

    abstract: [520$a repetitive]
    """
    return ', '.join(utils.force_list(value.get('a')))


@marc21tojson.over('identifiers', '^020..')
@utils.ignore_value
def marc21identifier_isbn(self, key, value):
    """Get identifier isbn.

    identifiers:isbn: 020$a
    """
    if value.get('a'):
        identifiers = self.get('identifiers', {})
        identifiers['isbn'] = value.get('a')
        return identifiers
    else:
        return None


@marc21tojson.over('identifiers', '^035..')
@utils.ignore_value
def marc21identifier_reroID(self, key, value):
    """Get identifier reroId.

    identifiers:reroID: 035$a
    """
    identifiers = self.get('identifiers', {})
    identifiers['reroID'] = value.get('a')
    return identifiers


@marc21tojson.over('notes', '^500..')
@utils.for_each_value
@utils.ignore_value
def marc21notes(self, key, value):
    """Get  notes.

    note: [500$a repetitive]
    """
    return value.get('a')


@marc21tojson.over('subjects', '^6....')
@utils.for_each_value
@utils.ignore_value
def marc21subjects(self, key, value):
    """Get subjects.

    subjects: 6xx [duplicates could exist between several vocabularies,
        if possible deduplicate]
    """
    return value.get('a')
