from typing import Dict, List

import psycopg2
import requests


def get_vacancies(keyword: str) -> List[Dict]:
    url = "https://api.hh.ru/vacancies"
    params = {"text": keyword, "per_page": 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    return []


class DBManager:
    """Класс для работы с данными в базе данных PostgreSQL."""

    def __init__(self, dbname: str, user: str, password: str, host: str):
        """Инициализация подключения к базе данных."""
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host
        )

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.employer_name, COUNT(v.vacancy_id) as vacancies_count
                FROM employer_table e
                LEFT JOIN vacancy_table v ON e.employer_id = v.employer_id
                GROUP BY e.employer_name
            """
            )
            return [
                {"company": row[0], "vacancies_count": row[1]} for row in cur.fetchall()
            ]

    def get_all_vacancies(self) -> List[Dict]:
        """Получает список всех вакансий с указанием компании, названия, зарплаты и ссылки."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.employer_name, v.vacancy_name, v.salary, e.vacancy_url
                FROM vacancy_table v
                JOIN employer_table e ON v.employer_id = e.employer_id
            """
            )
            return [
                {
                    "company": row[0],
                    "vacancy_name": row[1],
                    "salary": row[2],
                    "url": row[3],
                }
                for row in cur.fetchall()
            ]

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancy_table WHERE salary > 0")
            return round(cur.fetchone()[0], 2)

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Получает список вакансий с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.employer_name, v.vacancy_name, v.salary, e.vacancy_url
                FROM vacancy_table v
                JOIN employer_table e ON v.employer_id = e.employer_id
                WHERE v.salary > %s
            """,
                (avg_salary,),
            )
            return [
                {
                    "company": row[0],
                    "vacancy_name": row[1],
                    "salary": row[2],
                    "url": row[3],
                }
                for row in cur.fetchall()
            ]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Получает список вакансий, в названии которых содержится ключевое слово."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.employer_name, v.vacancy_name, v.salary, e.vacancy_url
                FROM vacancy_table v
                JOIN employer_table e ON v.employer_id = e.employer_id
                WHERE LOWER(v.vacancy_name) LIKE %s
            """,
                (f"%{keyword.lower()}%",),
            )
            return [
                {
                    "company": row[0],
                    "vacancy_name": row[1],
                    "salary": row[2],
                    "url": row[3],
                }
                for row in cur.fetchall()
            ]

    def close(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()
