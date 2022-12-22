from pynput import keyboard
from logger import *
from model import *
from view import *


def start():
    def on_release(key):
        pass

    def on_press(key):
        try:
            k = key.char
            if ui_get_screen() == SCR_PERS_LIST:
                if k == 'c':
                    ui_set_screen(SCR_PERS_ADD)
                    show_new_person_menu()
            elif ui_get_screen() == SCR_PERS_ADD:
                ui_set_person_fcs(k)
                show_new_person_menu()
            elif ui_get_screen() == SCR_PERS_CARD:
                if k == 'n':
                    ui_set_screen(SCR_PERS_CARD_ADD)
                    show_new_account_menu()
            elif ui_get_screen() == SCR_PERS_CARD_ADD:
                if k in [str(i) for i in range(10)]:
                    ui_set_cred_number(k)
                    show_new_account_menu()
        except AttributeError:
            if ui_get_screen() == SCR_PERS_LIST:
                if key == keyboard.Key.down:
                    scroll_persons_list(get_persons_count(), 'down')
                    show_persons_menu(get_persons(
                        PRINT_COUNT, ui_get_row_offset()))
                elif key == keyboard.Key.up:
                    scroll_persons_list(get_persons_count(), 'up')
                    show_persons_menu(get_persons(
                        PRINT_COUNT, ui_get_row_offset()))
                elif key == keyboard.Key.enter:
                    show_person_card(get_accounts(get_person_from_list(
                        True)))
                elif key == keyboard.Key.esc:
                    pass
            elif ui_get_screen() == SCR_PERS_ADD:
                if key == keyboard.Key.space:
                    ui_set_person_fcs(' ')
                elif key == keyboard.Key.backspace:
                    ui_set_person_fcs('\b')
                elif key == keyboard.Key.enter:
                    create_person(ui_get_person_fcs().split())
                    ui_set_person_fcs('', False)
                    ui_set_screen(SCR_PERS_LIST)
                    show_persons_menu(get_persons(
                        PRINT_COUNT, ui_get_row_offset()))
            elif ui_get_screen() == SCR_PERS_CARD_ADD:
                if key == keyboard.Key.enter:
                    p_id = get_person_from_list(True)[0]
                    create_account(ui_get_cred_number(), p_id)
                    ui_set_cred_number('', False)
                    ui_set_screen(SCR_PERS_CARD)
                    show_person_card(get_accounts(get_person_from_list(
                        True)))
            elif ui_get_screen() == SCR_PERS_CARD:
                if key == keyboard.Key.esc:
                    ui_set_screen(SCR_PERS_LIST)
                    show_persons_menu(get_persons(
                        PRINT_COUNT, ui_get_row_offset()))

    db_connect('accounts.db')
    listener = keyboard.Listener(on_press   = on_press, 
                                 on_release = on_release)
    listener.start()

    while True:
        sleep(0.1)
