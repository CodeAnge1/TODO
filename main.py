import os
import sqlite3

import DearPyGui_ImageController as dpg_img
from UI import *

connector = sqlite3.connect(fr'{os.getcwd()}\app_data\db\user.db', check_same_thread=False)
cursor = connector.cursor()


# image_cell = dpg_img.ImageViewer()
# dpg_img.set_texture_registry(dpg.add_texture_registry())
# trash_img = Image.open(r"D:\PycharmProjects\SchoolProject\app_data\icons\trash_button.png")
# trash_img_tag = dpg_img.tools.image_to_dpg_texture(trash_img)
# edit_img = Image.open(r"D:\PycharmProjects\SchoolProject\app_data\icons\edit-button.png")
# edit_img_tag = dpg_img.tools.image_to_dpg_texture(edit_img)


def set_styles():
    dpg.show_style_editor()
    # dpg.style
    # dpg.mvStyleVar_WindowBorderSize = 0
    # print(dpg.mvStyleVar_FrameRounding)
    # dpg.add_theme_style(dpg.mvStyleVar_FrameRounding)


def setup():
    dpg.create_context()
    dpg_img.set_texture_registry(dpg.add_texture_registry())
    dpg.setup_dearpygui()
    dpg.create_viewport(title='TODO', max_width=320, max_height=500, resizable=False)
    dpg.show_viewport()
    set_font()
    # set_styles()


def set_font():
    big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
    big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
    small_let_end = 0x00FF  # small "я" in cyrillic alphabet
    remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
    alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
    alph_shift = remap_big_let - big_let_start  # adds the shift from remapped to non-remapped
    with dpg.font_registry():
        with dpg.font(r".\app_data\fonts\arial.ttf", 20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
            for i1 in range(big_let_start, big_let_end + 1):  # Cycle through big letters in cyrillic alphabet
                dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
                dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Remap the small cyrillic letter
                biglet += 1  # choose next letter
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
