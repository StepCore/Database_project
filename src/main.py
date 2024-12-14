from src.database import connection
from src.manager import (avg_salary, higher_salary_vacancy,
                         list_and_count_vacancies, vacancies_list)


def main():
    user_input = input(
        "Выберите интересующую вас операцию из предложенных (1-4):\n"
        "1. Поиск вакансий по ключевым словам\n"
        "2. Вывести список компаний и количество вакансий у каждой компании\n"
        "3. Вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты и"
        "ссылки на вакансию\n"
        "4. Вывести среднюю зарплату по вакансиям\n"
        "5. Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
    )
    if user_input == "1":
        user_input = input("Введите слова для поиска: ")
        return connection(user_input)
    if user_input == "2":
        return list_and_count_vacancies
    if user_input == "3":
        return vacancies_list
    if user_input == "4":
        return avg_salary
    if user_input == "5":
        return higher_salary_vacancy


# print(main())
