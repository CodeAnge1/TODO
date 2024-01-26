import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge
from PIL import Image

import DearPyGui_ImageController as dpg_img
from constants import *
from main import connector, cursor, path_to_trash_img

renaming_desk = 0
naming_task = 0
new_task_name = ''
current_horizontal_group = 0
current_desk_id = 0
new_list_name = ''
naming_list = 0


# TODO 'desk' naming for desk; 'task_list' for tasks_list; 'task' for tasks


def desk_on_drop(source, target):
    data_1 = cursor.execute("""SELECT desk_id, desk_pos FROM Desks WHERE desk_internal_id=?""", (source,)).fetchone()
    data_2 = cursor.execute("""SELECT desk_id, desk_pos FROM Desks WHERE desk_internal_id=?""", (target,)).fetchone()
    cursor.execute("""UPDATE Desks SET desk_pos=? WHERE desk_id=?""", (data_1[1], data_2[0]))
    cursor.execute("""UPDATE Desks SET desk_pos=? WHERE desk_id=?""", (data_2[1], data_1[0]))
    connector.commit()


def task_on_drop(source, target):
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=(
    SELECT list_id FROM Tasks WHERE task_internal_id=?)""", (source,)).fetchone()[0]
    data_1 = list(cursor.execute("""SELECT list_id, task_id, task_pos, task_name, task_status, 
    task_description FROM Tasks WHERE task_internal_id=?""", (source,)).fetchone())
    data_2 = list(cursor.execute("""SELECT list_id, task_id, task_pos, task_name, task_status, 
    task_description FROM Tasks WHERE task_internal_id=?""", (target,)).fetchone())

    cursor.execute("""UPDATE Tasks SET task_id=? WHERE task_id=?""", (data_1[1], data_2[1]))
    cursor.execute("""UPDATE Tasks SET task_id=? WHERE task_id=?""", (data_2[1], data_1[1]))

    connector.commit()

    start_work_with_desk(None, None, desk_id)


def delete_desk(sender, app_data, user_data):
    desk_internal_id = user_data
    desk_id = cursor.execute("""SELECT desk_id FROM Desks WHERE desk_internal_id=?""", (desk_internal_id,)).fetchone()[
        0]
    list_ids = cursor.execute("""SELECT list_id FROM TaskLists WHERE desk_id=?""", (desk_id,)).fetchall()
    for lid in list_ids:
        cursor.execute("""DELETE FROM Tasks WHERE list_id=?""", (lid[0],))
    cursor.execute("DELETE FROM Desks WHERE desk_internal_id=?", (desk_internal_id,))
    cursor.execute("DELETE FROM TaskLists WHERE desk_id=?;", (desk_id,))
    connector.commit()
    delete_boards_from_view()


def new_board(sender, app_data, user_data):
    req = cursor.execute("""SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;""").fetchall()
    if len(req) == 0:
        desk_count = 1
    else:
        desk_count = req[0][0] + 1
    new_desk = dpge.add_movable_group(title=f'Новая_Доска_{desk_count}', parent='all_desks', height=40,
                                      drop_callback=desk_on_drop, title_color=TITLE_COLOR,
                                      width=((WINDOW_WIDTH - 30) / 2) - 17)
    dpg.add_button(label='Переименовать доску', parent=new_desk,
                   callback=board_rename_callback, user_data=desk_count)

    desk_internal_id = dpg.get_item_info(new_desk)['parent'] + 1

    dpg.add_button(label='Удалить доску', parent=new_desk, user_data=desk_internal_id, callback=delete_desk)
    dpg.add_button(label='Открыть доску', parent=new_desk,
                   callback=start_work_with_desk, user_data=desk_count)

    cursor.execute("""INSERT INTO Desks VALUES(?, ?, ?, ?);""",
                   (desk_count, new_desk, desk_count, f'Новая_Доска_{desk_count}'))
    connector.commit()
    delete_boards_from_view()


def rename_board(sender, app_data, user_data):
    global renaming_desk
    text = dpg.get_value(user_data)
    if text:
        cursor.execute("""UPDATE Desks SET desk_name=? WHERE desk_id=?""", (text, renaming_desk))
        connector.commit()
        internal_id = cursor.execute("""SELECT desk_internal_id FROM Desks WHERE desk_id=?""",
                                     (renaming_desk,)).fetchone()
    delete_boards_from_view()
    dpg.configure_item('modal_id', show=False)
    dpg.set_value('rename_text_box', '')


def rename_board_on_enter():
    rename_board(None, None, 'rename_text_box')


def delete_boards_from_view():
    dpg.delete_item('all_desks', children_only=True)
    req = cursor.execute("""SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;""").fetchall()
    load_boards()


def board_rename_callback(sender, app_data, user_data):
    global renaming_desk
    dpg.configure_item("modal_id", show=True)
    dpg.focus_item('rename_text_box')
    renaming_desk = user_data


def list_rename_callback(sender, app_data, user_data):
    global naming_list
    dpg.configure_item("modal_id", show=True)
    dpg.focus_item('rename_text_box')
    naming_list = user_data


def task_name_callback(sender, app_data, user_data):
    global naming_list
    dpg.configure_item('name_list_modal_id', show=True)
    dpg.focus_item('list_name_box')
    naming_list = user_data


def create_new_list():
    global current_desk_id, naming_list

    desk_id = current_desk_id
    list_id = cursor.execute("""SELECT list_id FROM TaskLists ORDER By list_id DESC LIMIT 1""").fetchone()
    if list_id:
        list_id = list_id[0] + 1
    else:
        list_id = 1
    naming_list = list_id

    list_name = 'Новый_лист'
    cursor.execute("""INSERT INTO TaskLists (desk_id, list_id, list_name) VALUES(?, ?, ?)""",
                   (desk_id, list_id, list_name))
    connector.commit()

    dpg.configure_item('name_list_modal_id', show=True)
    dpg.focus_item('list_name_box')

    start_work_with_desk(None, None, desk_id)


def delete_list(sender, app_data, user_data):
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=?""", (user_data,)).fetchone()[0]
    task_ids = cursor.execute("""SELECT task_id FROM Tasks WHERE list_id=?""", (user_data,)).fetchall()
    cursor.execute("""DELETE FROM TaskLists WHERE list_id=?""", (user_data,))
    for task_id in task_ids:
        cursor.execute("""DELETE FROM Tasks WHERE task_id=?""", (task_id[0],))
    connector.commit()
    start_work_with_desk(None, None, desk_id)


def create_new_task(sender, app_data, user_data):
    global naming_task

    list_id = user_data
    list_internal_id = cursor.execute("""SELECT list_internal_id FROM TaskLists 
    WHERE list_id=?""", (list_id,)).fetchone()[0]
    task_internal_id = dpg.add_group(parent=list_internal_id)

    req = cursor.execute("""SELECT task_pos FROM Tasks WHERE list_id=?""", (list_id,)).fetchall()
    if len(req) == 0:
        task_pos = 1
    else:
        task_pos = cursor.execute("""SELECT task_pos FROM Tasks WHERE list_id=? ORDER by task_pos DESC LIMIT 1""",
                                  (list_id,)).fetchone()[0] + 1

    task_name = f'Задача_{task_pos}'
    task_status = 0
    task_description = ''
    task_info = (list_id, task_internal_id, task_pos, task_name, task_status, task_description)

    cursor.execute("""INSERT INTO Tasks (list_id, task_internal_id,
    task_pos, task_name, task_status, task_description) VALUES(?, ?, ?, ?, ?, ?)""", task_info)
    connector.commit()
    naming_task = cursor.execute("""SELECT task_id FROM Tasks ORDER By task_id DESC LIMIT 1""").fetchone()[0]
    show_task_name()
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=?""", (list_id,)).fetchone()[0]
    start_work_with_desk(None, None, desk_id)


def show_task_name():
    dpg.configure_item('name_task_modal_id', show=True)
    dpg.focus_item('new_task_name_box')


def task_win_callback(sender, app_data, user_data):
    rename_task(None, None, user_data[0])
    add_description(user_data[1])
    dpg.configure_item('task_full_info', show=False)


def new_task_win_callback(sender, app_data, user_data):
    global naming_task

    rename_task(None, None, user_data[0])
    add_description(user_data[1])


def add_description(user_data):
    global naming_task
    new_desc = dpg.get_value(user_data)
    dpg.set_value(user_data, '')
    cursor.execute("""UPDATE Tasks SET task_description=? WHERE task_id=?""", (new_desc, naming_task))
    connector.commit()


def rename_task(sender, app_data, user_data):
    global new_task_name, naming_task

    new_task_name = dpg.get_value(user_data)
    new_task_name = str(new_task_name)
    dpg.configure_item('name_task_modal_id', show=False)
    dpg.set_value(user_data, '')
    if new_task_name:
        cursor.execute("""UPDATE Tasks SET task_name=? WHERE task_id=?""", (new_task_name, naming_task))
        connector.commit()
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE 
    list_id=(SELECT list_id FROM Tasks WHERE task_id=?)""", (naming_task,)).fetchone()[0]
    start_work_with_desk(None, None, desk_id)


def rename_task_on_enter():
    rename_task(None, None, 'task_name_box')


def rename_list_on_enter(sender, app_data, user_data):
    global naming_list
    if isinstance(user_data, list):
        naming_list = user_data[0]
        rename_list(None, None, user_data[1])
    else:
        rename_list(None, None, 'list_name_box')


def rename_list(sender, app_data, user_data):
    global new_list_name, naming_list

    new_list_name = dpg.get_value(user_data)
    new_list_name = str(new_list_name)
    dpg.configure_item('name_list_modal_id', show=False)
    dpg.set_value('list_name_box', '')
    cursor.execute("""UPDATE TaskLists SET list_name=? WHERE list_id=?""", (new_list_name, naming_list))
    connector.commit()
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=?""", (naming_list,)).fetchone()[0]
    start_work_with_desk(None, None, desk_id)


def delete_task(sender, app_data, user_data):
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=
    (SELECT list_id FROM Tasks WHERE task_id=?)""", (user_data[1],)).fetchone()[0]
    cursor.execute("""DELETE FROM Tasks WHERE task_id=?""", (user_data[1],))
    connector.commit()
    start_work_with_desk(None, None, desk_id)


def change_task_status(sender, app_data, user_data):
    if user_data[5] == 0 or user_data[5] == 1:
        new_task_status = 2
    else:
        new_task_status = 0
    cursor.execute("""UPDATE Tasks SET task_status=? WHERE task_id=?""", (new_task_status, user_data[1]))
    connector.commit()
    desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=(
    SELECT list_id FROM Tasks WHERE task_id=?)""", (user_data[1],)).fetchone()[0]
    start_work_with_desk(None, None, desk_id)


def in_progress_status(sender, app_data, user_data):
    global naming_task

    task = cursor.execute("""SELECT * FROM Tasks WHERE task_internal_id=?""", (app_data[1],)).fetchone()
    naming_task = task[1]

    if app_data[0] == 0 and dpg.is_key_down(dpg.mvKey_Control):
        dpg.configure_item('task_full_info', show=True)
        dpg.set_value('description_input', task[6])
        dpg.set_value('task_win_task_name_input', task[4])
    if app_data[0] == 1:
        desk_id = cursor.execute("""SELECT desk_id FROM TaskLists WHERE list_id=?""", (task[0],)).fetchone()[0]
        if task[5] == 1:
            new_status = 0
        else:
            new_status = 1
        cursor.execute("""UPDATE Tasks SET task_status=? WHERE task_id=?""", (new_status, task[1]))
        connector.commit()
        start_work_with_desk(None, None, desk_id)


def start_work_with_desk(sender, app_data, user_data):
    global current_desk_id
    current_desk_id = user_data

    dpg.set_item_user_data('task_creator', user_data)
    dpg.set_primary_window('MainWindow', False)
    dpg.configure_item('MainWindow', show=False)
    dpg.set_primary_window('tasks_window', True)
    dpg.configure_item('tasks_window', show=True)
    req = cursor.execute("""SELECT * FROM TaskLists WHERE desk_id=? ORDER by list_pos""", (user_data,)).fetchall()

    dpg.delete_item('task_lists_box', children_only=True)
    for k, task_list in enumerate(req):
        task_group = dpg.add_child_window(parent='task_lists_box', width=WINDOW_WIDTH / 3 - 10)
        if k != 0:
            dpg.add_spacer(before=task_group, width=10)

        name_and_delete = dpg.add_group(parent=task_group, horizontal=True)
        inp_text = dpg.add_input_text(default_value=task_list[4], parent=name_and_delete, width=185,
                                      on_enter=True, callback=rename_list_on_enter)
        dpg.set_item_user_data(inp_text, [task_list[1], inp_text])

        img2 = Image.open(path_to_trash_img)
        tag2 = dpg_img.tools.image_to_dpg_texture(img2)
        img_btn_2 = dpg.add_image_button(tag2, indent=191, width=17, height=20, background_color=[35, 35, 35],
                                         parent=name_and_delete, callback=delete_list, user_data=task_list[1])
        with dpg.theme() as theme_id:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (37, 37, 37, 255))
        dpg.bind_item_theme(img_btn_2, theme_id)

        dpg.add_button(label='Создать задачу', parent=task_group, height=35, width=217,
                       user_data=task_list[1], callback=create_new_task)
        cursor.execute("""UPDATE TaskLists SET list_internal_id=? WHERE list_id=?""", (task_group, task_list[1]))
        connector.commit()
        req_2 = cursor.execute("""SELECT * FROM Tasks WHERE list_id=?""", (task_list[1],)).fetchall()
        for n, task in enumerate(req_2):
            with dpg.group(parent=task_group, horizontal=True):
                if task[5] == 0:
                    task_color = TITLE_COLOR_UNCOMPLETED
                elif task[5] == 1:
                    task_color = TITLE_COLOR_IN_PROGRESS
                else:
                    task_color = TITLE_COLOR_COMPLETED
                if len(task[4]) <= 14:
                    task_name = task[4]
                else:
                    task_name = f"{task[4][:11]}..."
                mov = dpge.add_movable_group(title=task_name, title_color=task_color,
                                             height=1, width=10, user_data=task)
                cursor.execute("""UPDATE Tasks SET task_internal_id=? WHERE task_id=?""",
                               (mov, task[1]))
                dpg.bind_item_handler_registry(mov, 'widget handler')
                if task[5] == 0 or task[5] == 1:
                    dpg.add_checkbox(indent=WINDOW_WIDTH / 4 - 25, user_data=task, default_value=False,
                                     callback=change_task_status)
                elif task[5] == 2:
                    dpg.add_checkbox(indent=WINDOW_WIDTH / 4 - 25, user_data=task, default_value=True,
                                     callback=change_task_status)

                img2 = Image.open(path_to_trash_img)
                tag2 = dpg_img.tools.image_to_dpg_texture(img2)
                img_btn_2 = dpg.add_image_button(tag2, indent=WINDOW_WIDTH / 4 + 5, width=17, height=20,
                                                 background_color=[35, 35, 35],
                                                 callback=delete_task, user_data=task)
                with dpg.theme() as theme_id:
                    with dpg.theme_component(0):
                        dpg.add_theme_color(dpg.mvThemeCol_Button, (37, 37, 37, 255))
                dpg.bind_item_theme(img_btn_2, theme_id)
                # if n != 0:
                #     dpg.add_separator()


def end_work_with_desk():
    dpg.set_primary_window('MainWindow', True)
    dpg.configure_item('MainWindow', show=True)
    dpg.set_primary_window('tasks_window', False)
    dpg.configure_item('tasks_window', show=False)


def create_horizontal_group():
    global current_horizontal_group

    current_horizontal_group = dpg.add_group(horizontal=True, parent='all_desks')


def load_boards():
    global current_horizontal_group
    req = cursor.execute("""SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;""").fetchall()
    if len(req) != 0:
        req_2 = cursor.execute("""SELECT * FROM Desks ORDER BY desk_pos;""").fetchall()
        for k, i in enumerate(req_2):
            if k % 2 == 0:
                create_horizontal_group()
            if k != 0 and k % 2 == 0:
                dpg.add_spacer(before=current_horizontal_group, height=40)
            dpg.add_spacer(parent=current_horizontal_group)
            load_board(i[0], i[3])


def create_movable_group(desk_name, desk_id):
    global current_horizontal_group

    new_desk = dpge.add_movable_group(title=desk_name, parent=current_horizontal_group, height=40,
                                      drop_callback=desk_on_drop, title_color=TITLE_COLOR,
                                      width=((WINDOW_WIDTH - 30) / 2) - 17)
    desk_internal_id = new_desk
    cursor.execute("""UPDATE Desks SET desk_internal_id=? WHERE desk_id=?""", (desk_internal_id, desk_id))
    connector.commit()

    dpg.add_button(label='Переименовать доску', parent=new_desk,
                   callback=board_rename_callback, user_data=desk_id)
    dpg.add_button(label='Удалить доску', parent=new_desk, user_data=desk_internal_id, callback=delete_desk)
    dpg.add_button(label='Открыть доску', parent=new_desk,
                   callback=start_work_with_desk, user_data=desk_id)


def load_board(desk_id, desk_name):
    create_movable_group(desk_name, desk_id)


def main_window():
    with dpg.item_handler_registry(tag="widget handler") as handler:
        dpg.add_item_clicked_handler(callback=in_progress_status)
    with dpg.window(label='MainWindow', tag='MainWindow', no_scrollbar=False,
                    horizontal_scrollbar=True, no_resize=True, no_close=True):
        dpg.set_primary_window('MainWindow', True)
        dpg.add_button(label='Создать доску', callback=new_board, width=WINDOW_WIDTH - 30, height=35)
        with dpg.child_window(border=False, height=10):
            dpg.add_separator()
        with dpg.group(tag='all_desks', indent=0):
            create_horizontal_group()
            load_boards()


def rename_popup_window():
    with dpg.window(label="Переименовать доску", modal=True, show=False, tag="modal_id", no_title_bar=False,
                    width=300, height=140, no_close=False, no_resize=True):
        with dpg.group():
            dpg.add_spacer(height=7)
            text_box = dpg.add_input_text(tag='rename_text_box', default_value='', callback=rename_board_on_enter,
                                          hint='Введите новое название:', width=280, on_enter=True)
            dpg.add_spacer(height=7)
            with dpg.group(horizontal=True):
                dpg.add_button(label='Переименовать', width=180,
                               user_data=text_box, callback=rename_board)
                dpg.add_button(label='Отмена', indent=190, width=89,
                               callback=lambda: dpg.configure_item('modal_id', show=False))


def task_window():
    with dpg.window(label="Ваши задачи", show=False, tag='tasks_window',
                    no_scrollbar=False, horizontal_scrollbar=True):
        dpg.add_button(label='На главную', callback=end_work_with_desk, width=WINDOW_WIDTH - 30, height=35)
        dpg.add_child_window(height=2, border=False)
        dpg.add_button(label='Новый лист', width=WINDOW_WIDTH - 30, height=35, callback=create_new_list,
                       tag='task_creator')
        child = dpg.add_child_window(horizontal_scrollbar=True, no_scrollbar=False)
        dpg.add_group(tag='task_lists_box', horizontal=True, parent=child)


def new_task_get_name_window():
    with dpg.window(label="Введите название заддачи", modal=True, show=False, tag="name_task_modal_id",
                    no_title_bar=False, width=300, height=250, no_close=False, no_resize=True):
        with dpg.group():
            task_text_box = dpg.add_input_text(tag='new_task_name_box', default_value='', hint='Введите название:',
                                               width=283, on_enter=True)
            description_field = dpg.add_input_text(height=140, width=283, hint='Введите описание',
                                                   multiline=True, tag='new_description_input')
            dpg.set_item_user_data(task_text_box, [task_text_box, description_field])
            dpg.set_item_callback(task_text_box, new_task_win_callback)
            with dpg.group(horizontal=True):
                dpg.add_button(label='Ок', width=100,
                               user_data=[task_text_box, description_field], callback=new_task_win_callback)
                dpg.add_button(label='Отмена', indent=110, width=173,
                               callback=lambda: dpg.configure_item('name_task_modal_id', show=False))


def new_list_get_name_window():
    with dpg.window(label="Новая задача", modal=True, show=False, tag="name_list_modal_id",
                    no_title_bar=False, width=300, height=120, no_close=False, no_resize=True):
        with dpg.group():
            list_name_box = dpg.add_input_text(tag='list_name_box', default_value='', hint='Введите название:',
                                               width=280, on_enter=True, user_data='list_name_box',
                                               callback=rename_list_on_enter)
            with dpg.group(horizontal=True, pos=[0, 75]):
                dpg.add_button(label='Ок', width=100, indent=8,
                               user_data=list_name_box, callback=rename_list)
                # callback=rename_board
                dpg.add_button(label='Отмена', indent=118, width=170,
                               callback=lambda: dpg.configure_item('name_list_modal_id', show=False))


def task_full_info_window():
    with dpg.window(label="О задаче", modal=True, show=False, tag="task_full_info",
                    no_title_bar=False, width=300, height=250, no_close=False, no_resize=True):
        task_field = dpg.add_input_text(tag='task_win_task_name_input', width=283)
        description_field = dpg.add_input_text(height=140, width=283,
                                               multiline=True, tag='description_input')
        dpg.add_button(label='Применить', user_data=[task_field, description_field], tag='task_edit_apply',
                       callback=task_win_callback, width=283)
