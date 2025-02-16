import os
from typing import Dict, List, Optional

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
# Константа для конвертации валют
CURRENCY_RATES = {
    "RUB": 1,  # Российский рубль (базовая валюта)
    "KZT": 0.19,  # Казахстанский тенге
    "BYR": 29.41,  # Белорусский рубль (устаревший, сейчас BYN)
    "USD": 0.0101,  # Доллар США
    "EUR": 0.0094,  # Евро
    "UZS": 0.0078,  # Узбекский сум
}


class Database:
    """Класс для подключения к базе данных и вставки данных."""

    def __init__(self):
        """Инициализация подключения к базе данных."""
        self.conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DB"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )
        self._init_schema()

    def _init_schema(self):
        """Создание таблиц, если они не существуют."""
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS vacancy_table")
            cur.execute("DROP TABLE IF EXISTS employer_table")
            cur.execute(
                """
                CREATE TABLE employer_table (
                    employer_id TEXT PRIMARY KEY,
                    employer_name TEXT,
                    employer_url TEXT,
                    vacancy_url TEXT
                );
                CREATE TABLE vacancy_table (
                    vacancy_id TEXT PRIMARY KEY,
                    vacancy_name TEXT,
                    vacancy_locate TEXT,
                    salary NUMERIC,
                    employer_id TEXT REFERENCES employer_table(employer_id),
                    experience TEXT
                );
            """
            )
            self.conn.commit()

    def save_data(self, vacancies: List[Dict]):
        """Сохранение данных о вакансиях и работодателях в базу данных."""
        with self.conn.cursor() as cur:
            for vacancy in vacancies:
                # Сохранение работодателя
                if vacancy.get("employer"):
                    cur.execute(
                        """
                        INSERT INTO employer_table (employer_id, employer_name, employer_url, vacancy_url)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (employer_id) DO NOTHING
                    """,
                        (
                            vacancy["employer"]["id"],
                            vacancy["employer"]["name"],
                            vacancy["employer"]["alternate_url"],
                            vacancy["alternate_url"],
                        ),
                    )

                # Сохранение вакансии
                salary = self._convert_salary(vacancy.get("salary"))
                cur.execute(
                    """
                    INSERT INTO vacancy_table (vacancy_id, vacancy_name, vacancy_locate, salary, employer_id, experience)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                """,
                    (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["area"]["name"] if vacancy.get("area") else None,
                        salary,
                        vacancy["employer"]["id"] if vacancy.get("employer") else None,
                        (
                            vacancy["experience"]["name"]
                            if vacancy.get("experience")
                            else None
                        ),
                    ),
                )
            self.conn.commit()

    def _convert_salary(self, salary: Optional[Dict]) -> float:
        """Конвертация зарплаты в рубли."""
        if not salary:
            return 0
        from_s = salary.get("from", 0) or 0
        to_s = salary.get("to", 0) or 0
        currency = salary.get("currency", "RUB")
        avg = (float(from_s) + float(to_s)) / 2
        return avg * CURRENCY_RATES.get(currency, 1)

    def close(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()
