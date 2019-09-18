import pytest
import api


@pytest.fixture
def client():
    app = api.create_app({'TESTING': True})
    client = app.test_client()

    yield client


def test_health(client):
    health_rsp = client.get('health')
    assert '200' in health_rsp.status
    assert b'OK' in health_rsp.data
