import os
import pathlib
# TODO path module instead directory path
import sqlite3

from UI import *
from constants import *

dpg.create_context()
dpg_img.set_texture_registry(dpg.add_texture_registry())
image_cell = dpg_img.ImageViewer()
path_to_db_folder = pathlib.Path(pathlib.Path.cwd(), 'app_data', 'db')
path_to_db_file = pathlib.Path(pathlib.Path.cwd(), 'app_data', 'db', 'desks.db')

# from theme_apply import create_theme_custom_theme

if "desks.db" not in os.listdir(path_to_db_folder):
    connector = sqlite3.connect(path_to_db_file, check_same_thread=False)
    cursor = connector.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS "Desks" (
        "desk_id"	INTEGER,
        "desk_internal_id"	INTEGER,
        "desk_pos"	INTEGER,
        "desk_name"	TEXT,
        PRIMARY KEY("desk_id" AUTOINCREMENT)
    );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS "TaskLists" (
        "desk_id"	INTEGER,
        "list_id"	INTEGER NOT NULL UNIQUE,
        "list_internal_id"	INTEGER,
        "list_pos"	INTEGER,
        "list_name"	TEXT,
        PRIMARY KEY("list_id" AUTOINCREMENT),
        FOREIGN KEY("desk_id") REFERENCES "Desks"("desk_id")
    );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS "Tasks" (
        "list_id"	INTEGER,
        "task_id"	INTEGER UNIQUE,
        "task_internal_id"	INTEGER,
        "task_pos"	INTEGER,
        "task_name"	TEXT,
        "task_status"	INTEGER DEFAULT 0,
        "task_description"	TEXT,
        PRIMARY KEY("task_id" AUTOINCREMENT),
        FOREIGN KEY("list_id") REFERENCES "TaskLists"("list_id")
    );""")

    connector.commit()
else:
    connector = sqlite3.connect(path_to_db_file, check_same_thread=False)
    cursor = connector.cursor()


def set_style():
    dpg.show_style_editor()
    # theme_id = create_theme_custom_theme()
    # dpg.bind_theme(theme_id)


def setup():
    dpg.setup_dearpygui()
    dpg.create_viewport(title='ToDo', max_width=WINDOW_WIDTH, max_height=WINDOW_HEIGHT, resizable=False)
    # dpg.create_viewport(title='ToDo')
    dpg.show_viewport()
    set_font()
    set_style()


def set_font():
    big_let_start = 0x00C0
    big_let_end = 0x00DF
    small_let_end = 0x00FF
    remap_big_let = 0x0410
    alph_len = big_let_end - big_let_start + 1
    alph_shift = remap_big_let - big_let_start
    with dpg.font_registry():
        font_path = pathlib.Path(pathlib.Path.cwd(), 'app_data', 'fonts', 'SourceCodePro-SemiBold.ttf')
        with dpg.font(font_path, 22) as default_font:
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
    new_list_get_name_window()
    task_full_info_window()
    main_window()

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    setup()
    main()
