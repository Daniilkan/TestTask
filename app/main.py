import logging

logging.basicConfig(level=logging.INFO)

from app.services.parser import OzonParser
from app.services.classifier import ProductClassifier
from app.services.crm_tasks import CRMTasks
from app.services.analytics import Analytics
from app.config import new


config = new()

parser = OzonParser()
products = parser.get_products(config.MARKETPLACE_CATEGORY)

classifier = ProductClassifier()
classifier.classify_products(products)

analytics = Analytics()
crm_tasks = CRMTasks()

premium_products = analytics.top_5_premium()
crm_tasks.send_premium(premium_products)
budget_products = analytics.top_5_budget()
crm_tasks.send_budget(budget_products)