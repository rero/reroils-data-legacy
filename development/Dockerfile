FROM python:3.5-slim

LABEL maintainer="software@rero.ch"
LABEL description="ILS Data Model by RERO."

RUN apt-get update && apt-get install -y git curl

RUN pip install -U setuptools pip &&\
    pip install -U virtualenv

#Add reroils-data sources to `code` and work there:
WORKDIR  /reroils/reroils/src

# Run container as user `invenio` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' invenio && \
     chown -R invenio:invenio /reroils

USER invenio

SHELL ["/bin/bash", "-c"]
WORKDIR /reroils
RUN virtualenv reroils

RUN source /reroils/reroils/bin/activate && \
    cd reroils/src && \
    git clone https://gitlab.rero.ch/rero21/reroils-data.git && \
    cd reroils-data; pip install .[all]

CMD  /reroils/reroils/src/reroils-data/development/test.sh
