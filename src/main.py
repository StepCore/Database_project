import os

from dotenv import load_dotenv

from src.database import Database
from src.manager import DBManager, get_vacancies

load_dotenv(override=True)
db = Database()
manager = DBManager(
    dbname=os.getenv("DB"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
)


def main():
    user_input = input(
        "Выберите интересующую вас операцию из предложенных (1-4):\n"
        "1. Поиск вакансий по ключевым словам\n"
        "2. Вывести список компаний и количество вакансий у каждой компании\n"
        "3. Вывести список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на "
        "вакансию\n"
        "4. Вывести среднюю зарплату по вакансиям\n"
        "5. Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
    )
    if user_input == "1":
        user_input = input("Введите слова для поиска: ")
        vacancies = get_vacancies(user_input)
        db.save_data(vacancies)
        db.close()
        return vacancies
    if user_input == "2":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        db.close()
        return manager.get_companies_and_vacancies_count()
    if user_input == "3":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        db.close()
        return manager.get_all_vacancies()
    if user_input == "4":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        db.close()
        return manager.get_avg_salary()
    if user_input == "5":
        vacancies = get_vacancies("")
        db.save_data(vacancies)
        db.close()
        return manager.get_vacancies_with_higher_salary()


print(main())
