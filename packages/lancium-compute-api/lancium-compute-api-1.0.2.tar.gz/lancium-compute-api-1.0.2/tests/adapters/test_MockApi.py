import pytest


@pytest.fixture
def mock_api():
    """
    Create requests session with custom adapter.
    """

    from .MockApiAdapter import MockApiAdapter
    import requests

    session = requests.session()
    session.mount('https://', MockApiAdapter())
    return session


def test_mock_api(mock_api):
    response = mock_api.get('https://portal.lancium.com/test')

    assert response.url == 'https://portal.lancium.com/test'
    assert response.json()['test'] == 'test'