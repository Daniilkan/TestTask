# app/clients/marketplace.py

from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

class OzonClient:
    def __init__(self):
        self.driver = get_driver()

    def open_category(self, category: str):
        self.driver.get(f"https://www.ozon.ru/category/{category}/")

    def get_page(self, url: str):
        self.driver.get(url)

    def close(self):
        self.driver.quit()