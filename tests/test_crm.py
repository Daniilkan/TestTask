import pytest
from app.services.crm_tasks import CRMTasks
from app.models.product import Product
from datetime import datetime


@pytest.fixture
def crm_tasks():
    return CRMTasks()

@pytest.fixture
def sample_products():
    return [
        Product(art="1", name="Product 1", price=500, rating=4.5, reviews=10, url="https://test1.ru", category="Средние", collected_at=datetime.now()),
        Product(art="2", name="Product 2", price=1000, rating=4.8, reviews=20, url="https://test2.ru", category="Премиум", collected_at=datetime.now()),
    ]


def test_send_premium(crm_tasks, sample_products):
    result = crm_tasks.send_premium(sample_products)
    assert "result" in result
    assert result["result"] == "Mock task created successfully."


def test_send_budget(crm_tasks, sample_products):
    result = crm_tasks.send_budget(sample_products)
    assert "result" in result
    assert result["result"] == "Mock task created successfully."