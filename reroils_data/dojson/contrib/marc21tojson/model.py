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


@marc21tojson.over('__order__', '__order__')
def order(self, key, value):
    """Preserve order of datafields."""
    order = []
    for field in value:
        name = marc21tojson.index.query(field)
        if name:
            name = name[0]
        else:
            name = field
        order.append(name)

    return order


@marc21tojson.over('title', '^245..')
# @utils.for_each_value
# @utils.filter_values
def marc21totitle(self, key, value):
    """Get title from 245 $a."""
    return value.get('a')


@marc21tojson.over('author', '100..')
# @utils.for_each_value
# @utils.filter_values
def marc21toauthor(self, key, value):
    """Get author from 100 $a."""
    return value.get('a')
