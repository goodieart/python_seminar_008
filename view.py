from time import sleep
import os


PRINT_COUNT = 10                # Количество отображаемых записей
MAX_STR_LEN = 5                 # Макс. длина столбцов в списке

SCR_PERS_LIST      = 1          # Экран списка клиентов
SCR_PERS_CARD      = 2          # Экран списка счетов выбранного клиента
SCR_PERS_CARD_ADD  = 3          # Экран добавления нового счета в базу
SCR_PERS_CARD_SEND = 4          # Экран перечисления средств со счета на счет
SCR_PERS_ADD       = 5          # Экран добавления нового клиента в базу

current_screen = SCR_PERS_LIST

current_persons      = []
current_accounts     = []
first_row            = 0
current_row          = 0
debt_person          = 0
cred_person          = 0
cred_number_input    = ''
new_client_fcs_input = ''

def clear(): return os.system('cls')

def print_list(values: list):
    j = 0
    for i in values:
        j += 1
        print('   ' if current_row != j else ' > ', '\t|'.join(
            list(map(lambda x: str(x)[0:MAX_STR_LEN] + ('>' if len(str(x)) > MAX_STR_LEN else ''), i))))


def show_persons_menu(persons):
    global current_persons
    clear()
    show_ui('enter - выбор по id')
    current_persons = persons
    print_list(current_persons)
    show_ui('c - добавить | esc - выйти')
    sleep(0.2)


def show_accounts_menu(accounts):
    global current_accounts
    clear()
    p = get_person_from_list(True)
    fcs = ' '.join(p[1:4])
    show_ui(f'Счета клиента {fcs}', 64)
    current_accounts = accounts
    print_list(current_accounts)
    show_ui('n - новый | s - отправить | esc - назад', 64)

def show_new_account_menu():
    clear()
    show_ui(f'Создание нового счета', 64)
    print(f'Номер счета: {cred_number_input}')

def show_new_person_menu():
    clear()
    show_ui('Добавление нового клиента', 64)
    print(f'ФИО клиента: {new_client_fcs_input}')


def show_ui(prompt: str, width: int = 32):
    print('-' * width)
    print(f'| {prompt}' + (width - 3 - len(prompt)) * ' ' + '|')
    print('-' * width)


def show_person_card(accounts):
    p = current_persons[current_row - 1]
    ui_set_screen(SCR_PERS_CARD)
    show_accounts_menu(accounts)


def ui_set_screen(screen: int):
    global current_screen
    current_screen = screen

def ui_get_screen():
    global current_screen
    return current_screen

def ui_set_cred_number(text: str, append: bool = True):
    global cred_number_input
    if append: cred_number_input += text
    else: cred_number_input = text

def ui_get_cred_number():
    global cred_number_input
    return cred_number_input

def ui_set_person_fcs(text: str, append: bool = True):
    global new_client_fcs_input
    if append: new_client_fcs_input += text
    else: new_client_fcs_input = text

def ui_get_person_fcs():
    global new_client_fcs_input
    return new_client_fcs_input   

def ui_get_row_offset():
    global first_row
    return first_row

def scroll_persons_list(persons_count: int, direction: str):
    global current_row, first_row
    gp = persons_count
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



def get_person_from_list(cred: bool):
    global cred_person, debt_person
    if cred:
        cred_person = current_persons[current_row - 1]
        return cred_person
    else:
        debt_person = current_persons[current_row - 1]
        return debt_person