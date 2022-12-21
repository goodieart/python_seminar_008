import sqlite3 as sql
import keyboard
import os
from time import sleep


def clear(): return os.system('cls')


PRINT_COUNT = 10
MAX_STR_LEN = 5
SCR_PERS_LIST = 1
SCR_PERS_CARD = 2

current_screen = SCR_PERS_LIST

connection = None
cursor = None

first_row = 0
current_row = 0

current_persons = []
current_accounts = []

debt_person = 0
cred_person = 0


def db_connect(file: str):
    global connection, cursor
    connection = sql.connect(file)
    cursor = connection.cursor()


def get_persons(limit: int = 0, offset: int = 0):
    global cursor
    l = (f' LIMIT {limit}' if limit != 0 else '')
    o = (f' OFFSET {offset}' if offset != 0 else '')
    return list(cursor.execute(f'SELECT * FROM persons{l}{o}'))


def get_accounts(person, limit: int = 0, offset: int = 0):
    global cursor
    q = f'SELECT accounts.id, accounts.number, accounts.balance FROM accounts WHERE accounts.person_id = {person[0]}'
    l = (f' LIMIT {limit}' if limit != 0 else '')
    o = (f' OFFSET {offset}' if offset != 0 else '')
    #print(f'{q}{l}{o}')
    return list(cursor.execute(f'{q}{l}{o}'))


def get_persons_count():
    return list(cursor.execute('SELECT COUNT (*) FROM persons'))[0][0]


def print_list(values: list):
    j = 0
    for i in values:
        j += 1
        print('   ' if current_row != j else ' > ', '\t|'.join(
            list(map(lambda x: str(x)[0:MAX_STR_LEN] + ('>' if len(str(x)) > MAX_STR_LEN else ''), i))))


def show_persons_menu():
    global current_persons
    clear()
    show_ui('enter - выбор по id')
    current_persons = get_persons(PRINT_COUNT, first_row)
    print_list(current_persons)
    show_ui(f'{first_row},{current_row}')
    sleep(0.2)


def show_accounts_menu():
    global current_accounts
    clear()
    p = get_person_from_list(True)
    fcs = ' '.join(p[1:4])
    show_ui(f'Счета клиента {fcs}', 64)
    current_accounts = get_accounts(get_person_from_list(True))
    print_list(current_accounts)
    show_ui('n - новый | s - отправить | esc - назад', 64)


def show_ui(prompt: str, width: int = 32):
    print('-' * width)
    print(f'| {prompt}' + (width - 3 - len(prompt)) * ' ' + '|')
    print('-' * width)


def show_person_card():
    p = current_persons[current_row - 1]
    #print(p)
    change_screen(SCR_PERS_CARD)
    show_accounts_menu()


def change_screen(screen: int):
    global current_screen, first_row, current_row
    #first_row, current_row = 0, 0
    current_screen = screen


def get_person_from_list(cred: bool):
    global cred_person, debt_person
    if cred:
        cred_person = current_persons[current_row - 1]
        #print(cred_person)
        return cred_person
    else:
        debt_person = current_persons[current_row - 1]
        return debt_person


def draw_screen():
    pass


def scroll_persons_list(direction: str):
    global current_row, first_row
    gp = get_persons_count()
    if direction == 'down':
        if gp > 10:
            current_row += 1
            if current_row > PRINT_COUNT:
                first_row += 1 if first_row < gp else 0
                current_row -= 1
    elif direction == 'up':
        if gp > 10:
            current_row -= 1
            if current_row <= 0:
                first_row -= 1 if first_row > 0 else 0
                current_row += 1


db_connect('accounts.db')
show_persons_menu()
while True:
    if keyboard.is_pressed('down'):

        if current_screen == SCR_PERS_LIST:
            scroll_persons_list('down')
            show_persons_menu()
        elif current_screen == SCR_PERS_CARD:
            show_accounts_menu()
    elif keyboard.is_pressed('up'):
        if current_screen == SCR_PERS_LIST:
            scroll_persons_list('up')
            show_persons_menu()
        elif current_screen == SCR_PERS_CARD:
            show_accounts_menu()
    elif keyboard.is_pressed('esc'):
        if current_screen == SCR_PERS_LIST:
            break
        elif current_screen == SCR_PERS_CARD:
            change_screen(SCR_PERS_LIST)
            show_persons_menu()
        sleep(0.2)
    elif keyboard.is_pressed('enter'):
        if current_screen == SCR_PERS_LIST:
            show_person_card()
        sleep(0.2)
