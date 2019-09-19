import pytest
from lib import (db)


@pytest.fixture
def database():
    database = db.database
    database['ready'] = True
    database['stores'] = [
        {'name': 'St_Albans', 'postcode': 'AL1 2RJ'},
        {'name': 'Hatfield', 'postcode': 'AL9 5JP', 'longitude': -0.222034, 'latitude': 51.776142},
        {
            'latitude': 51.506662,
            'longitude': 0.104076,
            'name': 'Thamesmead',
            'postcode': 'SE28 8RD'
        },
        {
            'latitude': 51.741753,
            'longitude': -0.341337,
            'name': 'St_Albans',
            'postcode': 'AL1 2RJ'
        },
    ]
    database['keys'] = ['AL9 5JP', 'SE28 8RD']

    yield database


def test_fetch_geo_data():
    stores = [
        {'name': 'St_Albans', 'postcode': 'AL1 2RJ'},
        {'name': 'Hatfield', 'postcode': 'AL9 5JP'},
        {'name': 'UNKNOWN', 'postcode': 'XX0 0XX'}
    ]

    geo_data, _ = db.fetch_geo_data(stores)

    assert len(geo_data) == 3
    assert geo_data['AL1 2RJ']
    assert geo_data['AL9 5JP']['latitude'] == 51.776142
    assert not geo_data['XX0 0XX']


def test_db_search(database):
    db.database = database

    result = db.search('AL9 5JP', 5)
    assert not result

    result = db.search('AL9 5JP', 55)
    assert len(result) == 2
    assert result[0][db.FLD_LATITUDE] <= result[1][db.FLD_LATITUDE]


def test_postcode_normalize():
    result = ['TW2 5AH', 'AA99 9AA', 'A9 9AA', 'AA9A 9AA']
    for i, postcode in enumerate(['tw25ah', 'AA999AA', ' A9  9A  A', 'AA9A 9AA']):
        assert result[i] == db.postcode_normalize(postcode)
