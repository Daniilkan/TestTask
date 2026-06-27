import requests

from app.config import new

config = new()

class CRMManager:
    def __init__(self):
        self.mock_crm = config.MOCK_CRM
        self.webhook_url = config.BITRIX24_WEBHOOK_URL

    def create_task(self, title, description):
        if self.mock_crm:
            print(title)
            print(description)
            return {"result": "Mock task created successfully."}

        url = f"{self.webhook_url}/tasks.task.add.json"

        data = {
            "fields": {
                "TITLE": title,
                "DESCRIPTION": description,
            }
        }

        response = requests.post(url, json=data)

        response.raise_for_status()

        return response.json()