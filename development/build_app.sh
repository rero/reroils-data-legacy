#!/bin/bash
# -*- coding: utf-8 -*-
echo "Building version: $1"
source /reroils/reroils/bin/activate && \
cd reroils/src && \
git clone https://github.com/rero/reroils-data.git && \
cd reroils-data; pip install .[all]; pip install git+https://github.com/inveniosoftware/invenio-circulation.git#egg=invenio-circulation


