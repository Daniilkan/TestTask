import pytest
from app.services.analytics import Analytics
import json
from unittest.mock import mock_open, patch


@pytest.fixture
def analytics():
    mock_data = {
        "1": {
            "name": "Product 1",
            "url": "https://test1.ru",
            "price": 500,
            "category": "Средние",
            "rating": 4.5,
            "reviews": 10,
            "collected_at": "2023-11-01T12:00:00"
        },
        "2": {
            "name": "Product 2",
            "url": "https://test2.ru",
            "price": 1000,
            "category": "Премиум",
            "rating": 4.8,
            "reviews": 20,
            "collected_at": "2023-11-01T12:00:00"
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        return Analytics()


def test_top_5_premium(analytics):
    result = analytics.top_5_premium()
    assert len(result) == 2
    assert result[0].price >= result[1].price


def test_top_5_budget(analytics):
    result = analytics.top_5_budget()
    assert len(result) == 2
    assert result[0].price <= result[1].price