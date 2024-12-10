import requests


class DBManager:
    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"page": 0, "per_page": 100}
        self.vacancies = []
        super().__init__()

    def load_vacancies(self, keywords):
        """Основная функция для фильтрации вакансий"""
        self.__params["page"] = 0
        while self.__params.get("page") < 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            vacancies = response.json()["items"]
            for vacancy in vacancies:
                if any(
                    keyword.lower() in str(vacancy).lower()
                    for keyword in keywords.split(" ")
                ):
                    self.vacancies.append(vacancy)
            self.__params["page"] += 1
        return self.vacancies

    def get_companies_and_vacancies_count(self):
        """Возвращает список компаний и количество вакансий в каждой из них"""
        employer_count = {}
        self.load_vacancies(" ")
        for vacancy in self.vacancies:
            employer_name = vacancy["employer"]["name"]
            if employer_name in employer_count:
                employer_count[employer_name] += 1
            else:
                employer_count[employer_name] = 1

        result = [{employer: count} for employer, count in employer_count.items()]
        return result

    def get_all_vacancies(self):
        """Возвращает список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки"""
        all_vacancies = []
        self.load_vacancies(" ")

        currency_rates = {
            "RUB": 1,
            "KZT": 1 / 5.28,
            "BYR": 1 / 0.034,
            "USD": 99,
            "EUR": 106,
            "UZS": 1 / 129,
        }

        for vacancy in self.vacancies:
            company_name = vacancy.get("employer", {}).get(
                "name", "Неизвестная компания"
            )
            job_title = vacancy.get("name", "Без названия")
            salary = "Не указана"
            salary_info = vacancy.get("salary")
            if salary_info:
                salary_from = salary_info.get("from") or 0
                salary_to = salary_info.get("to") or 0
                currency = salary_info.get("currency", "RUB")

                salary_from = round(
                    float(salary_from) * currency_rates.get(currency, 1)
                )
                salary_to = round(float(salary_to) * currency_rates.get(currency, 1))

                salary = (
                    f"{salary_from} - {salary_to} RUB"
                    if salary_from != "Не указана"
                    else "Не указана"
                )

            vacancy_url = vacancy.get("alternate_url", "Нет ссылки")

            all_vacancies.append(
                {
                    "company": company_name,
                    "vacancy_name": job_title,
                    "salary": salary,
                    "vacancy_url": vacancy_url,
                }
            )

        return all_vacancies

    def get_avg_salary(self):
        """Возвращает среднюю зарплату в рублях по всем вакансиям"""
        total_salary = 0
        count = 0
        self.load_vacancies(" ")

        currency_rates = {
            "RUB": 1,
            "KZT": 1 / 5.28,
            "BYR": 1 / 0.034,
            "USD": 99,
            "EUR": 106,
            "UZS": 1 / 129,
        }

        for vacancy in self.vacancies:
            salary_info = vacancy.get("salary")
            if salary_info:
                salary_from = salary_info.get("from") or 0
                salary_to = salary_info.get("to") or 0
                currency = salary_info.get("currency", "RUB")

                # Преобразуем значения в рубли
                salary_from = float(salary_from) * currency_rates.get(currency, 1)
                salary_to = float(salary_to) * currency_rates.get(currency, 1)

                # Считаем среднюю зарплату для текущей вакансии
                avg_salary = (salary_from + salary_to) / 2
                total_salary += avg_salary
                count += 1

        # Рассчитываем среднюю зарплату по всем вакансиям
        average_salary = total_salary / count if count > 0 else 0

        return round(average_salary, 2)

    def get_vacancies_with_higher_salary(self):
        """Возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        vacancies_list = db_manager.get_all_vacancies()
        all_salaries = []

        for vacancy in vacancies_list:
            salary_str = vacancy.get("salary")

            if salary_str != "Не указана":
                # Извлекаем минимальную и максимальную зарплату
                salary_parts = salary_str.split(" - ")
                # Удаляем ' RUB' и преобразуем в float
                min_salary = (
                    float(salary_parts[0].replace(" RUB", "").replace(" ", ""))
                    if salary_parts[0] != "0"
                    else 0
                )
                max_salary = (
                    float(salary_parts[1].replace(" RUB", "").replace(" ", ""))
                    if salary_parts[1] != "0"
                    else 0
                )

                if min_salary > 0 or max_salary > 0:
                    # Если обе зарплаты не равны нулю, добавляем среднюю
                    salary_avg = (min_salary + max_salary) / 2
                    all_salaries.append(salary_avg)

        if not all_salaries:
            return []

        avg_salary = sum(all_salaries) / len(all_salaries)

        # Собираем вакансии с зарплатой выше средней
        higher_salary_vacancies = []
        for vacancy in vacancies_list:
            salary_str = vacancy.get("salary")

            if salary_str != "Не указана":
                salary_parts = salary_str.split(" - ")
                min_salary = (
                    float(salary_parts[0].replace(" RUB", "").replace(" ", ""))
                    if salary_parts[0] != "0"
                    else 0
                )
                max_salary = (
                    float(salary_parts[1].replace(" RUB", "").replace(" ", ""))
                    if salary_parts[1] != "0"
                    else 0
                )

                if min_salary > avg_salary or max_salary > avg_salary:
                    higher_salary_vacancies.append(vacancy)

        return higher_salary_vacancies

    def vacancies_with_keyword(self, keyword):
        """Функция для получения вакансий по ключевому слову"""
        return self.load_vacancies(keyword)


db_manager = DBManager()
list_and_count_vacancies = db_manager.get_companies_and_vacancies_count()
vacancies_list = db_manager.get_all_vacancies()
avg_salary = db_manager.get_avg_salary()
higher_salary_vacancy = db_manager.get_vacancies_with_higher_salary()
vacancies_keyword = db_manager.vacancies_with_keyword("your_text")

# print(*vacancies_list, sep='\n')
