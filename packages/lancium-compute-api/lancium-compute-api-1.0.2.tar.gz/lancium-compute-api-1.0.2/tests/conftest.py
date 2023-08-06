import pytest
import os

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv('LANCIUM_API_KEY', 'foobar')
    monkeypatch.setenv('LANCIUM_ENV', 'TEST')
    monkeypatch.setenv(
        'LANCIUM_CACHE_PATH',
        os.path.join(
            os.path.dirname(__file__),
            'lancium.conf'))