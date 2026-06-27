import logging
import json

from app.models.product import Product

logger = logging.getLogger(__name__)

class Analytics:
    def __init__(self):
        with open('products.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Convert dictionary data to Product objects
        self.products = [
            Product(art=art, **product_data) for art, product_data in data.items()
        ]

    def top_5_premium(self):
        logger.info('Calculating top 5 premium products...')
        premium_products = sorted(self.products, key=lambda x: x.price, reverse=True)
        return premium_products[:5]

    def top_5_budget(self):
        logger.info('Calculating top 5 budget products...')
        budget_products = sorted(self.products, key=lambda x: x.price)
        return budget_products[:5]