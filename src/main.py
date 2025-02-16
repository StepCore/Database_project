import os

from dotenv import load_dotenv

from src.api import get_vacancies
from src.database import Database
from src.manager import DBManager

load_dotenv(override=True)


def main():
    db = Database()
    manager = DBManager(
        dbname=os.getenv("DB"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
    )

    user_input = input(
        "Выберите интересующую вас операцию из предложенных (1-5):\n"
        "1. Поиск вакансий по ключевым словам\n"
        "2. Вывести список компаний и количество вакансий у каждой компании\n"
        "3. Вывести список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию\n"
        "4. Вывести среднюю зарплату по вакансиям\n"
        "5. Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
    )

    if user_input == "1":
        keyword = input("Введите слова для поиска: ")
        vacancies = get_vacancies(keyword)
        db.save_data(vacancies)
        print(f"Найдено {len(vacancies)} вакансий.")
    elif user_input == "2":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        print(manager.get_companies_and_vacancies_count())
    elif user_input == "3":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        print(manager.get_all_vacancies())
    elif user_input == "4":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        print(f"Средняя зарплата: {manager.get_avg_salary()}")
    elif user_input == "5":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        print(manager.get_vacancies_with_higher_salary())
    else:
        print("Неверный ввод.")

    db.close()
    manager.close()


if __name__ == "__main__":
    main()
