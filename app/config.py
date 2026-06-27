import os
import dotenv

dotenv.load_dotenv()

class Config:
    # Marketplace
    MARKETPLACE_CATEGORY: str
    PRODUCTS_LIMIT: int
    DEMO_MODE: bool

    # LLM
    OPENAI_API_KEY: str
    MOCK_LLM: bool

    # CRM
    BITRIX24_WEBHOOK_URL: str
    MOCK_CRM: bool

    # Parser
    REQUEST_TIMEOUT: int
    MAX_RETRIES: int

    # Logging
    LOG_LEVEL: str

    def __init__(self):
        self.MARKETPLACE_CATEGORY = os.getenv("MARKETPLACE_CATEGORY")
        self.PRODUCTS_LIMIT = int(os.getenv("PRODUCTS_LIMIT"))
        self.DEMO_MODE = bool(os.getenv("DEMO_MODE"))
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.MOCK_LLM = bool(int(os.getenv("MOCK_LLM")))
        self.BITRIX24_WEBHOOK_URL = os.getenv("BITRIX24_WEBHOOK_URL")
        self.MOCK_CRM = bool(os.getenv("MOCK_CRM"))
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES"))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL")

def new() -> Config:
    return Config()