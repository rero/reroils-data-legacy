# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from conftest import trans_bnf_prep


def _test_bnf_FIELDNAME():
    """Test FIELDNAME DESCRIPTION"""
    xml_part_to_add = """
        <datafield ind1="_A_" ind2="_B_" tag="_CCC_">
            <subfield code="_D_">_SUBFIELDATA_</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_FIELDNAME()
    assert trans.json == {
        "_FIELDNAME_": [
            "_FIELDATA_"
        ]
    }


def test_bnf_gender_female():
    """Test gender 120 $a a = female, b = male, - = not known."""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="120">
            <subfield code="a">a</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_gender()
    assert trans.json == {
        "gender": "female"
    }


def test_bnf_gender_male():
    """Test gender 120 $a a = female, b = male, - = not known."""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="120">
            <subfield code="a">b</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_gender()
    assert trans.json == {
        "gender": "male"
    }


def test_bnf_gender_missing():
    """Test gender 120 missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_gender()
    assert trans.json == {}


def test_bnf_language_of_person_1():
    """Test language of person 101 $a (langue sur 3 caractères) ISO 639-2"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="101">
            <subfield code="a">fre</subfield>
            <subfield code="a">eng</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_language_of_person()
    assert trans.json == {
        "language_of_person": [
            "fre",
            "eng"
        ]
    }


def test_bnf_language_of_person_2():
    """Test language of person 101 missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_language_of_person()
    assert trans.json == {}


def test_bnf_identifier_for_person_1():
    """Test identifier for person 001"""
    xml_part_to_add = """
        <controlfield tag="001">FRBNF170842162</controlfield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_identifier_for_person()
    assert trans.json == {
        "identifier_for_person": "17084216"
    }


def test_bnf_identifier_for_person_2():
    """Test identifier for person 001 missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_identifier_for_person()
    assert trans.json == {}


def test_bnf_birth_and_death_dates_1():
    """Test date of birth 103 $a pos. 1-8 YYYYMMDD"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="103">
            <subfield code="a">18160421 18550331</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816-04-21",
        "date_of_death": "1855-03-31"
    }


def test_bnf_birth_and_death_dates_2():
    """Test date of birth 103 $a pos. 1-8 YYYYMMDD"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="103">
            <subfield code="a">1816           </subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816"
    }


def test_bnf_birth_and_death_dates_3():
    """Test date of birth 200 $f pos. 1-4"""
    xml_part_to_add = """
          <datafield ind1=" " ind2=" " tag="200">
            <subfield code="f">1816-1855</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816",
        "date_of_death": "1855"
    }


def test_bnf_birth_and_death_dates_4():
    """Test date of birth 103 $a pos. 1-8 YYYYMMDD AND 200 $f pos. 1-4"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="103">
            <subfield code="a">18160421 18550331</subfield>
        </datafield>
          <datafield ind1=" " ind2=" " tag="200">
            <subfield code="f">1816-1855</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816-04-21",
        "date_of_death": "1855-03-31"
    }


def test_bnf_birth_and_death_dates_5():
    """Test date of birth 103 AND 200 missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_birth_and_death_dates()
    assert trans.json == {}


def test_bnf_biographical_information_1():
    """Test biographical information 300 $a 34x $a"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="300">
            <subfield code="a">Giacomo Nicolini da Sabbio.</subfield>
        </datafield>
        <datafield ind1=" " ind2=" " tag="341">
            <subfield code="a">Venezia</subfield>
            <subfield code="a">Italia</subfield>
        </datafield>
        <datafield ind1=" " ind2=" " tag="350">
            <subfield code="a">ignorer</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_biographical_information()
    assert trans.json == {
        "biographical_information": [
            "Giacomo Nicolini da Sabbio.",
            "Venezia, Italia"
        ]
    }


def test_bnf_biographical_information_2():
    """Test biographical information 300 $a 34x $a. missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_biographical_information()
    assert trans.json == {}


def test_bnf_preferred_name_for_person_1():
    """Test Preferred Name for Person 200 $ab"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="200">
            <subfield code="a">Brontë</subfield>
            <subfield code="b">Charlotte</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_preferred_name_for_person()
    assert trans.json == {
        "preferred_name_for_person":
            "Brontë, Charlotte"
    }


def test_bnf_preferred_name_for_person_2():
    """Test Preferred Name for Person 200 $ab missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_preferred_name_for_person()
    assert trans.json == {}


def test_bnf_variant_name_for_person_1():
    """Test Variant Name for Person 400 $ab"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="400">
            <subfield code="a">Bell</subfield>
            <subfield code="b">Currer</subfield>
        </datafield>
         <datafield ind1=" " ind2=" " tag="400">
            <subfield code="a">Brontë</subfield>
            <subfield code="b">Carlotta</subfield>
        </datafield>
     """
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_variant_name_for_person()
    assert trans.json == {
        "variant_name_for_person": [
            "Bell, Currer",
            "Brontë, Carlotta"
        ]
    }


def test_bnf_variant_name_for_person_2():
    """Test Variant Name for Person 400 $ab missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_variant_name_for_person()
    assert trans.json == {}

def test_authorized_access_point_representing_a_person_diff_order():
    """Test Authorized access point representing a person 200 $abdfc"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="200">
            <subfield code="f">1816-1855</subfield>
            <subfield code="b">Charlotte</subfield>
            <subfield code="a">Brontë</subfield>
            <subfield code="e">ignorer le texte</subfield>
            <subfield code="c">écrivain</subfield>
        </datafield>
     """
    trans = trans_prep(xml_part_to_add)
    trans.trans_authorized_access_point_representing_a_person()
    assert trans.json == {
        "authorized_access_point_representing_a_person":
            "1816-1855, Charlotte, Brontë, écrivain"
    }

def test_authorized_access_point_representing_a_person_general_order():
    """Test Authorized access point representing a person 200 $abdfc"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="200">
            <subfield code="a">Brontë</subfield>
            <subfield code="b">Charlotte</subfield>
            <subfield code="f">1816-1855</subfield>
            <subfield code="c">écrivain</subfield>
            <subfield code="e">ignorer le texte</subfield>
        </datafield>
     """
    trans = trans_prep(xml_part_to_add)
    trans.trans_authorized_access_point_representing_a_person()
    assert trans.json == {
        "authorized_access_point_representing_a_person":
            "Brontë, Charlotte, 1816-1855, écrivain"
    }


def test_bnf_authorized_access_point_representing_a_person_missing_field():
    """Test Authorized access point representing a person 200 $abdfc missing"""
    xml_part_to_add = ""
    trans = trans_bnf_prep(xml_part_to_add)
    trans.trans_bnf_authorized_access_point_representing_a_person()
assert trans.json == {}

