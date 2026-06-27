import json
import time
from datetime import datetime
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.services.functions import page_down
from app.config import new
from app.clients.marketplace import OzonClient
from app.models.product import Product

config = new()

logger = logging.getLogger(__name__)

class OzonParser:
    def __init__(self):
        logger.info('Initializing OzonParser...')
        self.client = OzonClient()

    def get_products(self, category_name=None):
        logger.info(f'Starting product collection for category: {category_name}')
        self.client.open_category(category_name)
        time.sleep(3)

        # Sorting by rating
        current_url = self.client.driver.current_url + '&sorting=rating'
        self.client.get_page(current_url)

        time.sleep(3)

        if config.DEMO_MODE:
            count = 20
        else:
            count = config.PRODUCTS_LIMIT

        products = []
        retries = 0
        max_retries = config.MAX_RETRIES
        page = 1
        wait = WebDriverWait(self.client.driver, config.REQUEST_TIMEOUT)

        while len(products) < count:
            try:
                paginated_url = f'{current_url}&page={page}'
                self.client.get_page(paginated_url)
                time.sleep(2)

                page_down(self.client.driver)
                time.sleep(2)

                logger.info('Waiting for product elements to load...')
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.q4b1_5_2-a.tile-clickable-element.rg3_20')))
                find_links = self.client.driver.find_elements(By.CSS_SELECTOR, '.q4b1_5_2-a.tile-clickable-element.rg3_20')
                find_names = self.client.driver.find_elements(By.CSS_SELECTOR, '.q4b1_5_2-a.tile-clickable-element.rg3_20')
                find_prices = self.client.driver.find_elements(By.CSS_SELECTOR, '.c35_3_17-a1.tsHeadline500Medium.c35_3_17-b1.c35_3_17-a6')
                find_ratings = self.client.driver.find_elements(By.CSS_SELECTOR, '.tsBodyControl300XSmall')
                find_reviews = self.client.driver.find_elements(By.CSS_SELECTOR, '.c7w1_6_1-a0.tsBodyControl300XSmall')

                logger.info(f'Found {len(find_links)} products on the page.')

                for i in range(len(find_links)):
                    try:
                        name = find_names[i].text
                        price = float(
                            find_prices[i].text.replace('₽', '').replace('\u2009', '').replace(' ', '')) if i < len(
                            find_prices) else 0.0
                        rating = float(find_ratings[i].text.split()[0]) if i < len(find_ratings) else 0.0
                        if rating > 5.0:
                            rating = 5.0
                        reviews = int(find_reviews[i].text.split()[0]) if i < len(find_reviews) else 0

                        product = Product(
                            art=find_links[i].get_attribute("href").split('-')[-1].split('/')[0],
                            name=name,
                            url=find_links[i].get_attribute("href"),
                            price=price,
                            category='NS',
                            rating=rating,
                            reviews=reviews,
                            collected_at=datetime.now(),
                        )
                        products.append(product)
                    except Exception:
                        pass

                page += 1

            except Exception as e:
                if "429" in str(e):  # Handle rate-limiting
                    wait_time = 2 ** retries
                    logger.warning(f'[!] Rate limit hit. Retrying in {wait_time} seconds...')
                    time.sleep(wait_time)
                    retries += 1
                    if retries > max_retries:
                        logger.fatal('Max retries reached. Exiting...')
                        break
                else:
                    logger.error(f'Error occurred: {e}')
                    break

        self.client.close()
        logger.info(f'Total products collected: {len(products)}')
        data = {}
        for product in products:
            data[product.art] = {
                'name': product.name,
                'url': product.url,
                'price': product.price,
                'category': product.category,
                'rating': product.rating,
                'reviews': product.reviews,
                'collected_at': product.collected_at.isoformat()
            }
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return products