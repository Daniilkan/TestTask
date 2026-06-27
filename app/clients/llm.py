import requests
import json
import logging

from app.config import new

logger = logging.getLogger(__name__)

class LLM:
    def __init__(self):
        logger.info('Initializing LLM client...')
        config = new()
        self.api_key = config.OPENAI_API_KEY
        self.mock_llm = config.MOCK_LLM

    def request_llm(self, prompt):
        if self.mock_llm:
            return """1221821299;Эконом
                        1597378776;Эконом
                        1342977839;Эконом
                        1821859245;Эконом
                        2855177519;Эконом
                        727203698;Эконом
                        727232742;Эконом
                        727173798;Средние
                        727247472;Средние
                        1835427825;Средние
                        626196894;Средние
                        785696783;Средние
                        785674336;Средние
                        389733824;Средние
                        177156061;Премиум
                        191581815;Премиум
                        693320570;Премиум
                        1608359824;Премиум
                        1471942557;Премиум
                        1804655860;Премиум"""

        logger.info('Sending request to LLM...')
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek/deepseek-r1",
            "messages": [
                {"role": "system", "content": "Ты — ассистент-сортировщик товаров."},
                {"role": "user", "content": "Твоя задача из данных в списках рассортировать данные товары на три категории: Эконом, Средние и Премиум. В ответе не должно быть ничего кроме артикула и категории разделенными точкой с запятой, все товары должны быть на отдельных строках. Делай сортировку с расчетом, чтобы при малом количестве товаров распределение было примерно равное.\n" + prompt}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
        )

        if response.status_code == 200:
            try:
                response_json = response.json()
                if "choices" in response_json:
                    content = response_json["choices"][0]["message"].get("content", "")
                    return content
                else:
                    raise Exception("Unexpected response format: 'choices' not found.")
            except json.JSONDecodeError:
                raise Exception("Error decoding JSON response.")
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
