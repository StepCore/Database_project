from typing import Dict, List

import requests


def get_vacancies(keyword: str) -> List[Dict]:
    """Получает вакансии с API hh.ru."""
    url = "https://api.hh.ru/vacancies"
    params = {"text": keyword, "per_page": 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    return []
