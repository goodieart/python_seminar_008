import sqlite3 as sql
import keyboard
import os
from time import sleep

clear = lambda: os.system('cls')

PRINT_COUNT = 10

KEY_DOWN = 40

connection = None
cursor = None

first_row = 0


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
    clear()
    for i in values:
        print('\t|'.join(list(map(str, i))))

def show_persons_menu():
    pass


db_connect('accounts.db')
# print_persons(get_persons(2, 1))
# print(get_persons_count())
print_persons(get_persons(10, first_row))
while True:
    if keyboard.is_pressed('down'):
        gp = get_persons_count()
        if gp > 10:
            first_row += 1 if first_row < gp else 0
            print_persons(get_persons(10, first_row))
            sleep(0.2)
    elif keyboard.is_pressed('up'):
        gp = get_persons_count()
        if gp > 10:
            first_row -= 1 if first_row > 0 else 0
            print_persons(get_persons(10, first_row))
            sleep(0.2)


# import keyboard  # using module keyboard
# while True:  # making a loop
#     try:  # used try so that if user pressed other than the given key error will not be shown
#         if keyboard.is_pressed('q'):  # if key 'q' is pressed 
#             print('You Pressed A Key!')
#             break  # finishing the loop
#     except:
#         break  # if user pressed a key