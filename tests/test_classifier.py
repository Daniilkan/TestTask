import pytest
from app.services.parser import OzonParser


@pytest.fixture
def parser():
    return OzonParser()


def test_get_products(parser, monkeypatch):
    def mock_get_products(*args, **kwargs):
        return []

    monkeypatch.setattr(parser, "get_products", mock_get_products)
    result = parser.get_products("test_category")
    assert isinstance(result, list)
    assert len(result) == 0