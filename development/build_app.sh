#!/bin/bash
# -*- coding: utf-8 -*-
echo "About to source virtual env\n"
source /reroils/reroils/bin/activate && \
echo "Done sourcing\n" && \
cd reroils/src && \
git clone https://gitlab.rero.ch/rero21/reroils-data.git && \
cd reroils-data; pip install .[all]


