# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from reroils_data.authorities.marctojson.mef_record import MEF_record


def test_mef_record_1(empty_mef_record):
    """Test andding a JSON source data for BNF."""
    mef_record = MEF_record(
        json_data=empty_mef_record,
        logger=None,
        verbose=False
    )
    json_data = {}
    json_data['gender'] = 'female'

    mef_record.update_source(source='bnf', json_data=json_data)
    assert mef_record.json == {
        "md5": [
            {'source': 'bnf', 'value': '875a47ddcf63e33a4d5f65db190e73d0'}
        ],
        "gender": [
            {
                'source': 'bnf',
                'value': 'female'
            }
        ]
    }


def test_mef_record_2(empty_mef_record):
    """Test andding a JSON source data for BNF and GND."""
    mef_record = MEF_record(
        json_data=empty_mef_record,
        logger=None,
        verbose=False
    )
    bnf_json_data = {}
    bnf_json_data['gender'] = 'female'
    gnd_json_data = {}
    gnd_json_data['gender'] = 'female'

    mef_record.update_source(source='bnf', json_data=bnf_json_data)
    mef_record.update_source(source='gnd', json_data=gnd_json_data)
    assert mef_record.json == {
        "md5": [
            {'source': 'bnf', 'value': '875a47ddcf63e33a4d5f65db190e73d0'},
            {'source': 'gnd', 'value': '875a47ddcf63e33a4d5f65db190e73d0'}
        ],
        "gender": [
            {
                'source': 'bnf',
                'value': 'female'
            },
            {
                'source': 'gnd',
                'value': 'female'
            },
        ]
    }
    new_bnf_json_data = {}
    new_bnf_json_data['gender'] = 'male'
    mef_record.update_source(source='bnf', json_data=new_bnf_json_data)
    assert mef_record.json == {
        "md5": [
            {'source': 'gnd', 'value': '875a47ddcf63e33a4d5f65db190e73d0'},
            {'source': 'bnf', 'value': 'fee8baae9d07f5e237693ddd9137b8c8'}
        ],
        "gender": [
            {
                'source': 'gnd',
                'value': 'female'
            },
            {
                'source': 'bnf',
                'value': 'male'
            }
        ]
    }


def test_mef_record_3(empty_mef_record):
    """Test andding and removing source data."""
    mef_record = MEF_record(
        json_data=empty_mef_record,
        logger=None,
        verbose=False
    )
    bnf_json_data = {}
    bnf_json_data['gender'] = 'female'
    gnd_json_data = {}
    gnd_json_data['gender'] = 'female'
    mef_record.update_source(source='bnf', json_data=bnf_json_data)
    mef_record.update_source(source='gnd', json_data=gnd_json_data)
    mef_record.delete_source(source='bnf')
    assert mef_record.json == {
        "md5": [
            {'source': 'gnd', 'value': '875a47ddcf63e33a4d5f65db190e73d0'}
        ],
        "gender": [
            {
                'source': 'gnd',
                'value': 'female'
            },
        ]
    }
