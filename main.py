import sqlite3 as sql
import keyboard
import os
from time import sleep


def clear(): return os.system('cls')


PRINT_COUNT = 10

connection = None
cursor = None

first_row = 0
current_row = 0

current_persons = []


def db_connect(file: str):
    global connection, cursor
    connection = sql.connect(file)
    cursor = connection.cursor()


def get_persons(limit: int = 0, offset: int = 0):
    l = (f' LIMIT {limit}' if limit != 0 else '')
    o = (f' OFFSET {offset}' if offset != 0 else '')
    return list(cursor.execute(f'SELECT * FROM persons{l}{o}'))


def get_persons_count():
    return list(cursor.execute('SELECT COUNT (*) FROM persons'))[0][0]


def print_persons(values: list):
    j = 0
    for i in values:
        j += 1
        print('   ' if current_row != j else ' > ', '\t|'.join(
            list(map(lambda x: str(x)[0:5] + ('>' if len(str(x)) > 5 else ''), i))))


def show_persons_menu():
    global current_persons
    clear()
    show_ui('enter - выбор по id')
    current_persons = get_persons(PRINT_COUNT, first_row)
    print_persons(current_persons)
    show_ui(f'{first_row},{current_row}')
    sleep(0.2)


def show_ui(prompt: str):
    print(f'--------------------------------')
    print(f'| {prompt}' + (29 - len(prompt)) * ' ' + '|')
    print(f'--------------------------------')


def show_person_card():
    print(current_persons[current_row - 1])


db_connect('accounts.db')
show_persons_menu()
while True:
    if keyboard.is_pressed('down'):
        gp = get_persons_count()
        if gp > 10:
            current_row += 1
            if current_row > PRINT_COUNT:
                first_row += 1 if first_row < gp else 0
                current_row -= 1
            show_persons_menu()
    elif keyboard.is_pressed('up'):
        gp = get_persons_count()
        if gp > 10:
            current_row -= 1
            if current_row <= 0:
                first_row -= 1 if first_row > 0 else 0
                current_row += 1
            show_persons_menu()
    elif keyboard.is_pressed('esc'):
        break
    elif keyboard.is_pressed('enter'):
        show_person_card()
        sleep(0.2)
