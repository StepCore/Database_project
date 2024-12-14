import psycopg2

from src.manager import DBManager


def insert_vacancy(cur, vacancy):
    """Основная функция заполняющая таблицу БД"""
    vacancy_id = vacancy["id"]
    vacancy_name = vacancy["name"]
    vacancy_locate = vacancy["area"]["name"] if vacancy["area"] else None
    salary = (
        vacancy["salary"]["from"]
        if vacancy["salary"] and "from" in vacancy["salary"]
        else None
    )
    employer = vacancy["employer"]["name"] if vacancy["employer"] else None
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
        INSERT INTO vacancy_table (vacancy_id, vacancy_name, vacancy_locate, salary, employer, experience)
        VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (vacancy_id, vacancy_name, vacancy_locate, salary, employer, experience),
    )


def connection(keywords):
    """Подключение к БД и вставка данных в таблицу"""

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
        "employer VARCHAR(255),"
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
