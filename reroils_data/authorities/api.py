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

"""API for manipulating authorities."""

from ..api import IlsRecord
from .fetchers import auth_id_fetcher, bnf_id_fetcher, gnd_id_fetcher, \
    mef_id_fetcher, rero_id_fetcher, viaf_id_fetcher
from .minters import auth_id_minter, bnf_id_minter, gnd_id_minter, \
    mef_id_minter, rero_id_minter, viaf_id_minter
from .providers import AuthorityProvider, BnfProvider, GndProvider, \
    MefProvider, ReroProvider, ViafProvider


class Authority(IlsRecord):
    """Authority class."""

    minter = auth_id_minter
    fetcher = auth_id_fetcher
    provider = AuthorityProvider


class Mef(IlsRecord):
    """Mef Authority class."""

    minter = mef_id_minter
    fetcher = mef_id_fetcher
    provider = MefProvider


class Gnd(IlsRecord):
    """Gnd Authority class."""

    minter = gnd_id_minter
    fetcher = gnd_id_fetcher
    provider = GndProvider


class Rero(IlsRecord):
    """Rero Authority class."""

    minter = rero_id_minter
    fetcher = rero_id_fetcher
    provider = ReroProvider


class Bnf(IlsRecord):
    """Bnf Authority class."""

    minter = bnf_id_minter
    fetcher = bnf_id_fetcher
    provider = BnfProvider


class Viaf(IlsRecord):
    """Viaf Authority class."""

    minter = viaf_id_minter
    fetcher = viaf_id_fetcher
    provider = ViafProvider
