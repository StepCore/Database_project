import psycopg2

from src.manager import DBManager


def insert_vacancy(cur, vacancy):
    """Основная функция заполняющая таблицу vacancy_table"""
    vacancy_id = vacancy["id"]
    vacancy_name = vacancy["name"]
    vacancy_locate = vacancy["area"]["name"] if vacancy["area"] else None
    salary = (
        vacancy["salary"]["from"]
        if vacancy["salary"] and "from" in vacancy["salary"]
        else None
    )
    employer = vacancy["employer"]["id"] if vacancy["employer"] else None
    experience = vacancy["experience"]["name"] if vacancy["experience"] else None

    # Проверка, существует ли уже такая вакансия в базе
    cur.execute(
        "SELECT COUNT(*) FROM vacancy_table WHERE vacancy_id = %s", (vacancy_id,)
    )
    if cur.fetchone()[0] > 0:
        # Если вакансия уже существует, пропустить вставку
        return

    # Выполнение SQL-запроса на вставку
    cur.execute(
        """
        INSERT INTO vacancy_table (vacancy_id, vacancy_name, vacancy_locate, salary, employer_id, experience)
        VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (vacancy_id, vacancy_name, vacancy_locate, salary, employer, experience),
    )


def insert_employer(cur, vacancy):
    """Основная функция заполняющая таблицу employer_table"""
    employer_id = vacancy["employer"]["id"] if vacancy["employer"] else None
    employer_name = vacancy["employer"]["name"]
    employer_url = vacancy["employer"]["alternate_url"]
    vacancy_url = vacancy["alternate_url"]

    # Проверка, существует ли уже такая вакансия в базе
    cur.execute(
        "SELECT COUNT(*) FROM employer_table WHERE employer_id = %s", (employer_id,)
    )
    if cur.fetchone()[0] > 0:
        # Если вакансия уже существует, пропустить вставку
        return

    # Выполнение SQL-запроса на вставку
    cur.execute(
        """
        INSERT INTO employer_table (employer_id, employer_name, employer_url, vacancy_url)
        VALUES (%s, %s, %s, %s)
    """,
        (employer_id, employer_name, employer_url, vacancy_url),
    )


def connection_vacancy(keywords):
    """Создание БД vacancy_table и вставка данных в таблицу"""

    conn = psycopg2.connect(
        host="localhost", database="postgres", user="postgres", password="ZeliBobka789"
    )

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS vacancy_table")
    cur.execute(
        "CREATE TABLE vacancy_table ("
        "vacancy_id SERIAL PRIMARY KEY,"
        "vacancy_name VARCHAR(255),"
        "vacancy_locate VARCHAR(255),"
        "salary NUMERIC(10, 2),"
        "employer_id NUMERIC,"
        "experience VARCHAR(100))"
    )

    vacancies = DBManager().vacancies_with_keyword(keywords)

    for vacancy in vacancies:
        insert_vacancy(cur, vacancy)

    conn.commit()

    # Проверка, что вакансии были добавлены
    cur.execute("SELECT * FROM vacancy_table")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()
    return "Список вакансий сохранен в базе данных"


def connection_employer(keywords):
    """Создание БД employer_table и вставка данных в таблицу"""

    conn = psycopg2.connect(
        host="localhost", database="postgres", user="postgres", password="ZeliBobka789"
    )

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS employer_table")
    cur.execute(
        "CREATE TABLE employer_table ("
        "employer_id SERIAL PRIMARY KEY,"
        "employer_name VARCHAR(255),"
        "employer_url VARCHAR(255),"
        "vacancy_url VARCHAR(100))"
    )

    vacancies = DBManager().vacancies_with_keyword(keywords)

    for vacancy in vacancies:
        insert_employer(cur, vacancy)

    conn.commit()

    # Проверка, что вакансии были добавлены
    cur.execute("SELECT * FROM employer_table")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()
    return "Список вакансий сохранен в базе данных"
