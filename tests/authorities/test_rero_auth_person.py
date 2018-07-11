# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from conftest import trans_prep


def _test_FIELDNAME():
    """Test FIELDNAME DESCRIPTION"""
    xml_part_to_add = """
        <datafield ind1="_A_" ind2="_B_" tag="_CCC_">
            <subfield code="_D_">_SUBFIELDATA_</subfield>
        </datafield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_FIELDNAME()
    assert trans.json == {
        "_FIELDNAME_": [
            "_FIELDATA_"
        ]
    }


def test_rero_identifier_for_person():
    """Test identifier for person 001"""
    xml_part_to_add = """
        <controlfield tag="001">vtls020260472</controlfield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_identifier_for_person()
    assert trans.json == {
        "identifier_for_person": "020260472"
    }


def test_rero_birth_and_death_dates():
    """Test date of birth 100 $d pos. 1-4 YYYY"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="d">1816 1855</subfield>
        </datafield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816",
        "date_of_death": "1855"
    }


def test_rero_biographical_information():
    """Test biographical information 680 $a"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="680">
            <subfield code="a">Romancière. - Charlotte Brontë.</subfield>
        </datafield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_biographical_information()
    assert trans.json == {
        "biographical_information": [
            "Romancière. - Charlotte Brontë."
        ]
    }


def test_rero_preferred_name_for_person():
    """Test Preferred Name for Person 100 $a"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="a">Brontë, Charlotte</subfield>
        </datafield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_preferred_name_for_person()
    assert trans.json == {
        "preferred_name_for_person":
            "Brontë, Charlotte"
    }


def test_rero_variant_name_for_person():
    """Test Variant Name for Person 400 $a"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="400">
            <subfield code="a">Bell, Currer</subfield>
        </datafield>
         <datafield ind1=" " ind2=" " tag="400">
            <subfield code="a">Brontë, Carlotta</subfield>
        </datafield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_variant_name_for_person()
    assert trans.json == {
        "variant_name_for_person": [
            "Bell, Currer",
            "Brontë, Carlotta"
        ]
    }


def test_rero_authorized_access_point_representing_a_person():
    """Test Authorized access point representing a person 100 $adc"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="a">Brontë, Charlotte</subfield>
            <subfield code="d">1816-1855</subfield>
            <subfield code="c">écrivain</subfield>
        </datafield>
     """
    trans = trans_prep('rero', xml_part_to_add)
    trans.trans_rero_authorized_access_point_representing_a_person()
    assert trans.json == {
        "authorized_access_point_representing_a_person":
            "Brontë, Charlotte, 1816-1855, écrivain"

    }
