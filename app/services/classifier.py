from app.config import new
from app.clients.llm import LLM

import logging
import json

logger = logging.getLogger(__name__)
config = new()

class ProductClassifier:
    def __init__(self):
        self.llm = LLM()

    def classify_products(self, products):
        # Load existing data from the file
        try:
            with open('products.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}

        # Build prompts and classify products
        prompts = self._build_prompt(products)
        classified_products = {}
        for prompt in prompts:
            response = self.llm.request_llm(prompt)
            classified_products.update(self._parse_response(response))

        # Update product categories in the existing data
        for product in products:
            if product.art in classified_products:
                product.category = classified_products[product.art]
            existing_data[product.art] = {
                'name': product.name,
                'url': product.url,
                'price': product.price,
                'category': product.category,
                'rating': product.rating,
                'reviews': product.reviews,
                'collected_at': product.collected_at.isoformat()
            }

        # Save the updated data back to the file
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(
                {product.art: {
                    'name': product.name,
                    'url': product.url,
                    'price': product.price,
                    'category': product.category,
                    'rating': product.rating,
                    'reviews': product.reviews,
                    'collected_at': product.collected_at.isoformat()
                } for product in products},
                f,
                ensure_ascii=False,
                indent=4
            )


    def _build_prompt(self, products):
        chunk_size = 15
        prompts = []
        for i in range(0, len(products), chunk_size):
            chunk = products[i:i + chunk_size]
            prompt_lines = []
            for product in chunk:
                prompt_lines.append(
                    f"{product.art}; {product.name}; {product.price}; {product.rating}; {product.reviews}")
            prompts.append("\n".join(prompt_lines))
        return prompts

    def _parse_response(self, response):
        classified_products = {}
        lines = response.strip().split("\n")
        for line in lines:
            if line:
                try:
                    article, category = line.split(";")
                    classified_products[article.strip()] = category.strip()
                except ValueError:
                    continue
        return classified_products