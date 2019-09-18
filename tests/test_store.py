import json
import pytest
import api
import lib.db


@pytest.fixture
def database():
    yield {
        'ready': True,
        'loading': False,
        'stores': [
            {
                "latitude": 51.741753,
                "longitude": -0.341337,
                "name": "St_Albans",
                "postcode": "AL1 2RJ"
            },
        ],
        'keys': ['AL1 2RJ'],
    }


@pytest.fixture
def client():
    app = api.create_app({'TESTING': True})
    client = app.test_client()

    yield client


def test_stores(client):
    health_rsp = client.get('/stores')
    assert '202' in health_rsp.status


def test_stores_with_data(client, database):
    api.store.database = database
    rsp = client.get('/stores')
    data = json.loads(rsp.data.decode())

    assert '200' in rsp.status
    assert len(data)
    assert data[0][lib.db.FLD_POSTCODE] == "AL1 2RJ"


def test_search_postcode_not_found(client, database):
    lib.db.database = database
    rsp = client.get('/stores/X/circle?q=0')

    assert '404' in rsp.status


def test_search_postcode_found(client, database):
    lib.db.database = database
    rsp = client.get('/stores/al1%202rj/circle?q=10m')

    assert '200' in rsp.status

    data = json.loads(rsp.data.decode())
    assert not data['result']
    assert data['radius'] == 10
