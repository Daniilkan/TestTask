from app.models.product import Product
from datetime import datetime


def test_product_creation():
    product = Product(
        art="1",
        name="Phone",
        price=1000,
        rating=5,
        reviews=5,
        url="https://test.ru",
        category="Средние",
        collected_at=datetime.now()
    )
    assert product.name == "Phone"