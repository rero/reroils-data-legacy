# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from conftest import trans_gnd_prep


def _test_gnd_FIELDNAME():
    """Test FIELDNAME DESCRIPTION"""
    xml_part_to_add = """
        <datafield ind1="_A_" ind2="_B_" tag="_CCC_">
            <subfield code="_D_">_SUBFIELDATA_</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_FIELDNAME()
    assert trans.json == {
        "_FIELDNAME_": [
            "_FIELDATA_"
        ]
    }


def test_gnd_gender_female():
    """Test gender 375 $a 1 = male, 2 = female, " " = not known."""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="375">
            <subfield code="a">2</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_gender()
    assert trans.json == {
        "gender": "female"
    }


def test_gnd_gender_male():
    """Test gender 375 $a 1 = male, 2 = female, " " = not known."""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="375">
            <subfield code="a">1</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_gender()
    assert trans.json == {
        "gender": "male"
    }


def test_gnd_gender_missing():
    """Test gender 375 missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_gender()
    assert trans.json == {}


def test_gnd_language_of_person_1():
    """Test language of person 377 $a (langue sur 3 caractères) ISO 639-2b"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="377">
            <subfield code="a">fre</subfield>
            <subfield code="a">eng</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_language_of_person()
    assert trans.json == {
        "language_of_person": [
            "fre",
            "eng"
        ]
    }


def test_gnd_language_of_person_2():
    """Test language of person 377 missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_language_of_person()
    assert trans.json == {}


def test_gnd_identifier_for_person_1():
    """Test identifier for person 001"""
    xml_part_to_add = """
        <controlfield tag="001">118577166</controlfield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_identifier_for_person()
    assert trans.json == {
        "identifier_for_person": "118577166"
    }


def test_gnd_identifier_for_person_2():
    """Test identifier for person 001 missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_identifier_for_person()
    assert trans.json == {}


def test_gnd_birth_and_death_dates_1():
    """Test date of birth 100 $d YYYY-YYYY"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="d">1816-1855</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816",
        "date_of_death": "1855"
    }


def test_gnd_birth_and_death_dates_2():
    """Test date of birth 100 $d YYYY-"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="d">1816-</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "1816"
    }


def test_gnd_birth_and_death_dates_3():
    """Test date of birth 100 $d -YYYY"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="d">-1855</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {
        "date_of_death": "1855"
    }


def test_gnd_birth_and_death_dates_4():
    """Test date of birth 548 $a DD.MM.YYYY-DD.MM.YYYY $4 datx"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="548">
            <subfield code="a">06.06.1875-12.08.1955</subfield>
            <subfield code="4">datx</subfield>
        </datafield>
        <datafield ind1=" " ind2=" " tag="548">
            <subfield code="a">1875-1955</subfield>
            <subfield code="4">datl</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "06.06.1875",
        "date_of_death": "12.08.1955"
    }


def test_gnd_birth_and_death_dates_5():
    """Test date of birth 548 $a DD.MM.YYYY- $4 datx"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="548">
          <subfield code="a">06.06.1875-</subfield>
          <subfield code="4">datx</subfield>
        </datafield>
        <datafield ind1=" " ind2=" " tag="548">
            <subfield code="a">1875-</subfield>
            <subfield code="4">datl</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {
        "date_of_birth": "06.06.1875"
    }


def test_gnd_birth_and_death_dates_6():
    """Test date of birth 548 $a -DD.MM.YYYY $4 datx"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="548">
          <subfield code="a">-12.08.1955</subfield>
          <subfield code="4">datx</subfield>
        </datafield>
        <datafield ind1=" " ind2=" " tag="548">
            <subfield code="a">-1955</subfield>
            <subfield code="4">datl</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {
        "date_of_death": "12.08.1955"
    }


    def test_gnd_birth_and_death_dates_7():
    """Test date of birth 100 AND 548 missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_birth_and_death_dates()
    assert trans.json == {}


def test_gnd_biographical_information_1():
    """Test biographical information 670 $abu"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="670">
            <subfield code="a">Wikipedia</subfield>
            <subfield code="b">Stand: 09.01.2018</subfield>
            <subfield code="u">https://de.wikipedia.org/wiki/Marie_Louise_d%E2%80%99Orl%C3%A9ans</subfield>
        </datafield>
         <datafield ind1=" " ind2=" " tag="670">
            <subfield code="a"Archivio Biogr. Italiano I 52,194</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_biographical_information()
    assert trans.json == {
        "biographical_information": [
            "Wikipedia Stand: 09.01.2018 https://de.wikipedia.org/wiki/Marie_Louise_d%E2%80%99Orl%C3%A9ans",
            "Archivio Biogr. Italiano I 52,194"
        ]
    }


def test_gnd_biographical_information_2():
    """Test biographical information 670 missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_biographical_information()
    assert trans.json == {}


def test_gnd_preferred_name_for_person_1():
    """Test Preferred Name for Person 100 $a"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="a">Bauer, Johann Gottfried</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_preferred_name_for_person()
    assert trans.json == {
        "preferred_name_for_person":
            "Bauer, Johann Gottfried"
    }


def test_gnd_preferred_name_for_person_2():
    """Test Preferred Name for Person 100 $a missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_preferred_name_for_person()
    assert trans.json == {}


def test_gnd_variant_name_for_person_1():
    """Test Variant Name for Person 400 $a"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="400">
            <subfield code="a">Bauer, Johanes Gottfried</subfield>
        </datafield>
         <datafield ind1=" " ind2=" " tag="400">
            <subfield code="a">Bauerus, Johannes Godofredus</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_variant_name_for_person()
    assert trans.json == {
        "variant_name_for_person": [
            "Bauer, Johanes Gottfried",
            "Bauerus, Johannes Godofredus"
        ]
    }


def test_gnd_variant_name_for_person_2():
    """Test Variant Name for Person 400 $a missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_variant_name_for_person()
    assert trans.json == {}


def test_gnd_authorized_access_point_representing_a_person_1():
    """Test Authorized access point representing a person 100 $abcdgt"""
    xml_part_to_add = """
        <datafield ind1=" " ind2=" " tag="100">
            <subfield code="a">Johannes Paul</subfield>
            <subfield code="b">II.</subfield>
            <subfield code="c">Papst</subfield>
            <subfield code="d">1920-2005</subfield>
            <subfield code="g">Sonstige Informationen</subfield>
            <subfield code="t">Ad tuendam fidem</subfield>
        </datafield>
     """
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_authorized_access_point_representing_a_person()
    assert trans.json == {
        "authorized_access_point_representing_a_person":
            "Johannes Paul II. Papst 1920-2005 Sonstige Informationen Ad tuendam fidem"
    }


def test_gnd_authorized_access_point_representing_a_person_2():
    """Test Authorized access point representing a person 100 $abcdgt missing"""
    xml_part_to_add = ""
    trans = trans_gnd_prep(xml_part_to_add)
    trans.trans_gnd_authorized_access_point_representing_a_person()
    assert trans.json == {}
