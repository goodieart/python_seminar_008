import sqlite3 as sql

connection = None
cursor = None


def db_connect(file: str):
    global connection, cursor
    connection = sql.connect(file, check_same_thread=False)
    cursor = connection.cursor()


def get_persons(limit: int = 0, offset: int = 0):
    global cursor
    q = 'SELECT * FROM persons'
    l = (f' LIMIT {limit}' if limit != 0 else '')
    o = (f' OFFSET {offset}' if offset != 0 else '')
    return list(cursor.execute(f'{q}{l}{o}'))


def get_accounts(person, limit: int = 0, offset: int = 0):
    global cursor
    q = f'SELECT accounts.id, accounts.number, accounts.balance FROM accounts WHERE accounts.person_id = {person[0]}'
    l = (f' LIMIT {limit}' if limit != 0 else '')
    o = (f' OFFSET {offset}' if offset != 0 else '')
    return list(cursor.execute(f'{q}{l}{o}'))


def get_persons_count():
    return list(cursor.execute('SELECT COUNT (*) FROM persons'))[0][0]

def get_accounts_count(person_id: int):
    return list(cursor.execute(f'SELECT COUNT (*) FROM accounts WHERE person_id = {person_id}'))


def create_account(number: str, person_id: str):
    row = (number, person_id)
    cursor.execute(
        'INSERT INTO accounts (number, person_id) VALUES (?, ?)', row)
    connection.commit()


def create_person(*args):
    cursor.execute(
        'INSERT INTO persons (first_name, second_name, patronymic) VALUES (?, ?, ?)', tuple(args[0]))
    connection.commit()


