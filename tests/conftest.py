import pytest

from app.models.product import Product


@pytest.fixture
def product():
    return Product(
        art="123",
        name="iPhone",
        price=120000,
        rating=4.9,
        reviews=100,
        url="https://test.ru",
        category="Премиум"
    )

def test_price(product):
    assert product.price == 120000