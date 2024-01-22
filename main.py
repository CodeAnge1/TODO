import os
import sqlite3

from dearpygui_ext import themes
# from theme_apply import create_theme_custom_theme

from UI import *

if "user.db" not in os.listdir(f'{os.getcwd()}/app_data/db'):
    connector = sqlite3.connect('app_data/db/user.db', check_same_thread=False)
    cursor = connector.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Desks" (
        "desk_id"	INTEGER,
        "desk_internal_id"	INTEGER,
        "desk_pos"	INTEGER,
        "desk_name"	TEXT,
        PRIMARY KEY("desk_id" AUTOINCREMENT)
    );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS "Tasks" (
        "desk_id"	INTEGER,
        "task_id"	INTEGER UNIQUE,
        "task_internal_id"	INTEGER,
        "task_pos"	INTEGER,
        "task_name"	TEXT,
        "task_is_completed"	INTEGER DEFAULT 0,
        "task_end_date"	TEXT,
        PRIMARY KEY("task_id" AUTOINCREMENT),
        FOREIGN KEY("desk_id") REFERENCES "Desks"("desk_id")
    );""")

    connector.commit()
else:
    connector = sqlite3.connect('app_data/db/user.db', check_same_thread=False)
    cursor = connector.cursor()


def set_style():
    dpg.show_style_editor()
    theme_id = create_theme_custom_theme()
    dpg.bind_theme(theme_id)


def setup():
    dpg.create_context()
    dpg.setup_dearpygui()
    dpg.create_viewport(title='TODO', max_width=320, max_height=500, resizable=False)
    # dpg.create_viewport(title='TODO', resizable=True)
    dpg.show_viewport()
    set_font()
    # set_style()


def set_font():
    big_let_start = 0x00C0
    big_let_end = 0x00DF
    small_let_end = 0x00FF
    remap_big_let = 0x0410
    alph_len = big_let_end - big_let_start + 1
    alph_shift = remap_big_let - big_let_start
    with dpg.font_registry():
        with dpg.font(r".\app_data\fonts\arial.ttf", 20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            biglet = remap_big_let
            for i1 in range(big_let_start, big_let_end + 1):
                dpg.add_char_remap(i1, biglet)
                dpg.add_char_remap(i1 + alph_len, biglet + alph_len)
                biglet += 1
            dpg.bind_font(default_font)


def main():
    rename_popup_window()
    task_window()
    new_task_get_name_window()
    main_window()

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    setup()
    main()
