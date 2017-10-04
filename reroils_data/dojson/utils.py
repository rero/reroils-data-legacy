# -*- coding: utf-8 -*-
#
# This file is part of DoJSON
# Copyright (C) 2015, 2016 CERN.
#
# DoJSON is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Utility functions."""

import json


def dump(iterator):
    """Dump JSON from iteraror."""
    return json.dumps(list(iterator), indent=2)
