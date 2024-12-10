import psycopg2
from src.manager import vacancies_with_keyword


def insert_vacancy(cur, vacancy):
    # Извлечение данных из вакансии
    vacancy_name = vacancy['name']
    vacancy_locate = vacancy['area']['name'] if vacancy['area'] else None
    salary = vacancy['salary']['from'] if vacancy['salary'] and 'from' in vacancy['salary'] else None
    employer = vacancy['employer']['name'] if vacancy['employer'] else None
    experience = vacancy['experience']['name'] if vacancy['experience'] else None

    # Выполнение SQL-запроса на вставку
    cur.execute('''
        INSERT INTO vacancy_table (vacancy_name, vacancy_locate, salary, employer, experience)
        VALUES (%s, %s, %s, %s, %s)
    ''', (vacancy_name, vacancy_locate, salary, employer, experience))


def main():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='StepWinGame7'
    )

    cur = conn.cursor()

    vacancies = vacancies_with_keyword

    for vacancy in vacancies:
        insert_vacancy(cur, vacancy)

    conn.commit()

    cur.execute('SELECT * FROM vacancy_table')
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
