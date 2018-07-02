# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os

import pytest
from marctojson.do_bnf_auth_person import Transformation
from pymarc import MARCReader, marcxml


def trans_bnf_prep(xml_part_to_add):
    """Prepare transformation."""
    build_xml_bnf_record_file(xml_part_to_add)
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(
        current_dir, 'examples/xml_minimal_record.xml')
    records = marcxml.parse_xml_to_array(
        file_name, strict=False, normalize_form=None)
    trans = Transformation(
        marc=records[0],
        logger=None,
        verbose=False,
        transform=False
    )
    return trans


def build_xml_bnf_record_file(xml_part_to_add):
    """Build_xml_record_file."""
    xml_record_as_text = """
        <record>
            <leader>00589nx  a2200193   45  </leader> """ + \
        xml_part_to_add + \
        '</record>'
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(
        current_dir, 'examples/xml_minimal_record.xml')
    with open(file_name, 'w', encoding='utf-8') as out:
        out.write(xml_record_as_text)


@pytest.fixture(scope='session')
def empty_mef_record():
    """empty MEF record."""
    json_mef_record = {}
    return json_mef_record


@pytest.fixture(scope='session')
def marc_record():
    """marc record."""
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(current_dir, 'examples/one_record.mrc')
    records = MARCReader(
        open(file_name, 'rb'),
        to_unicode=True,
        force_utf8=True,
        utf8_handling='ignore'
    )
    for record in records:
        return record


@pytest.fixture(scope='session')
def minimal_marcxml_record():
    """marc record."""
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(
        current_dir, 'examples/bnf_auth_person_minimal.xml')
    records = marcxml.parse_xml_to_array(
        file_name, strict=False, normalize_form=None)
    for record in records:
        return record


@pytest.fixture(scope='session')
def one_marcxml_record():
    """marc record."""
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(
        current_dir, 'examples/bnf_auth_person_complete.xml')

    records = marcxml.parse_xml_to_array(
        file_name, strict=False, normalize_form=None)
    # records = MARCReader(
    #     open(file_name, 'rb'),
    #     to_unicode=True,
    #     force_utf8=True,
    #     utf8_handling='ignore'
    # )
    for record in records:
        return record


@pytest.fixture(scope='session')
def all_marcxml_records():
    """marc record."""
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(
        current_dir, '../data/bnf_auth_person_P1486_20.mrc')
    records = MARCReader(
        open(file_name, 'rb'),
        to_unicode=True,
        force_utf8=True,
        utf8_handling='ignore'
    )
    return records


@pytest.fixture(scope='session')
def ten_marcxml_records():
    """marc record."""
    current_dir = os.path.dirname(__file__)
    file_name = os.path.join(
        current_dir, 'examples/ten_xml_record.xml')

    records = marcxml.parse_xml_to_array(
        file_name, strict=False, normalize_form=None)
    # records = MARCReader(
    #     open(file_name, 'rb'),
    #     to_unicode=True,
    #     force_utf8=True,
    #     utf8_handling='ignore'
    # )
    # for record in records:
    #     print('print_log', records)
    return records
