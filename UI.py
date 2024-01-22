import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge

from constants import *
from main import connector, cursor

renaming_desk = 0
naming_task = 0
new_task_name = ''


def on_drop(source, target):
    data_1 = cursor.execute("""SELECT desk_id, desk_pos FROM Desks WHERE desk_internal_id=?""", (source,)).fetchone()
    data_2 = cursor.execute("""SELECT desk_id, desk_pos FROM Desks WHERE desk_internal_id=?""", (target,)).fetchone()
    cursor.execute("""UPDATE Desks SET desk_pos=? WHERE desk_id=?""", (data_1[1], data_2[0]))
    cursor.execute("""UPDATE Desks SET desk_pos=? WHERE desk_id=?""", (data_2[1], data_1[0]))
    connector.commit()


# TODO
def task_on_drop(source, target):
    print(source, target)


def delete_desk(sender, app_data, user_data):
    desk_id = cursor.execute("""SELECT desk_id FROM Desks WHERE desk_internal_id=?""", (user_data,)).fetchone()[0]
    cursor.execute("DELETE FROM Desks WHERE desk_internal_id=?", (user_data,))
    cursor.execute("DELETE FROM Tasks WHERE desk_id=?;", (desk_id,))
    connector.commit()
    delete_boards_from_view()


def new_board(sender, app_data, user_data):
    req = cursor.execute("""SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;""").fetchall()
    if len(req) == 0:
        desk_count = 1
    else:
        desk_count = req[0][0] + 1
    new_desk = dpge.add_movable_group(title=f'Новая_Доска_{desk_count}', parent='desks', height=30,
                                      drop_callback=on_drop, title_color=TITLE_COLOR, width=290)
    dpg.add_button(label='Переименовать доску', parent=new_desk,
                   callback=board_rename_callback, user_data=desk_count)

    desk_internal_id = dpg.get_item_info(new_desk)['parent'] + 1

    dpg.add_button(label='Удалить доску', parent=new_desk, user_data=desk_internal_id, callback=delete_desk)
    dpg.add_button(label='Открыть доску', parent=new_desk,
                   callback=start_work_with_desk, user_data=desk_count)

    cursor.execute("""INSERT INTO Desks VALUES(?, ?, ?, ?);""",
                   (desk_count, new_desk, desk_count, f'Новая_Доска_{desk_count}'))
    connector.commit()


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


def delete_boards_from_view():
    dpg.delete_item('desks', children_only=True)
    req = cursor.execute("""SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;""").fetchall()
    if len(req) == 0:
        pass
    else:
        req_2 = cursor.execute("""SELECT * FROM Desks ORDER BY desk_pos;""").fetchall()
        for i in req_2:
            load_board(i[0], i[3])


def board_rename_callback(sender, app_data, user_data):
    global renaming_desk
    dpg.configure_item("modal_id", show=True)
    renaming_desk = user_data


def task_name_callback(sender, app_data, user_data):
    global naming_task
    dpg.configure_item('name_task_modal_id', show=True)
    naming_task = user_data


def create_new_task(sender, app_data, user_data):
    global naming_task

    desk_id = user_data
    task_internal_id = dpg.add_group(horizontal=True, parent='task_box')

    req = cursor.execute("""SELECT task_pos FROM Tasks WHERE desk_id=?""", (desk_id,)).fetchall()
    if len(req) == 0:
        task_pos = 1
    else:
        task_pos = cursor.execute("""SELECT task_pos FROM Tasks WHERE desk_id=? ORDER by task_pos DESC LIMIT 1""",
                                  (desk_id,)).fetchone()[0] + 1

    task_name = f'Задача_{task_pos}'
    task_is_completed = 0
    task_end_date = None
    task_info = (desk_id, task_internal_id, task_pos, task_name, task_is_completed, task_end_date)

    cursor.execute("""INSERT INTO Tasks (desk_id, task_internal_id,
    task_pos, task_name, task_is_completed, task_end_date) VALUES(?, ?, ?, ?, ?, ?)""", task_info)
    connector.commit()
    naming_task = cursor.execute("""SELECT task_id FROM Tasks ORDER By task_id DESC LIMIT 1""").fetchone()[0]
    show_task_name()
    start_work_with_desk(None, None, desk_id)


def show_task_name():
    dpg.configure_item('name_task_modal_id', show=True)


def rename_task(sender, app_data, user_data):
    global new_task_name, naming_task

    # TODO fix bug with long task name
    new_task_name = dpg.get_value(user_data)
    dpg.configure_item('name_task_modal_id', show=False)
    cursor.execute("""UPDATE Tasks SET task_name=? WHERE task_id=?""", (new_task_name, naming_task))
    connector.commit()
    desk_id = cursor.execute("""SELECT desk_id FROM Tasks WHERE task_id=?""", (naming_task,)).fetchone()[0]
    start_work_with_desk(None, None, desk_id)


def delete_task(sender, app_data, user_data):
    cursor.execute("""DELETE FROM Tasks WHERE task_id=?""", (user_data[1],))
    connector.commit()
    start_work_with_desk(None, None, user_data[0])


def change_task_status(sender, app_data, user_data):
    current_task_status = bool(user_data[5])
    new_task_status = int(not current_task_status)
    cursor.execute("""UPDATE Tasks SET task_is_completed=? WHERE task_id=?""", (new_task_status, user_data[1]))
    connector.commit()
    start_work_with_desk(None, None, user_data[0])


def start_work_with_desk(sender, app_data, user_data):
    dpg.set_item_user_data('task_creator', user_data)
    dpg.set_primary_window('MainWindow', False)
    dpg.configure_item('MainWindow', show=False)
    dpg.set_primary_window('tasks_window', True)
    dpg.configure_item('tasks_window', show=True)
    req = cursor.execute("""SELECT * FROM Tasks WHERE desk_id=? ORDER by task_pos""", (user_data,)).fetchall()

    dpg.delete_item('task_box', children_only=True)
    for k, task in enumerate(req):
        with dpg.group(horizontal=True, parent='task_box'):
            if task[5] == 0:
                task_color = TITLE_COLOR_UNCOMPLETED
            else:
                task_color = TITLE_COLOR_COMPLETED
            dpge.add_movable_group(title=f"{k + 1}. {task[4]}", title_color=task_color, drop_callback=task_on_drop)
            if task[5] == 0:
                dpg.add_checkbox(indent=157, user_data=task, default_value=False, callback=change_task_status)
            else:
                dpg.add_checkbox(indent=157, user_data=task, default_value=True, callback=change_task_status)
            dpg.add_button(label='Удалить', indent=188, user_data=task, callback=delete_task)
        dpg.add_separator(parent='task_box')


def end_work_with_desk():
    dpg.set_primary_window('MainWindow', True)
    dpg.configure_item('MainWindow', show=True)
    dpg.set_primary_window('tasks_window', False)
    dpg.configure_item('tasks_window', show=False)


def load_board(desk_id, desk_name):
    new_desk = dpge.add_movable_group(title=desk_name, parent='desks', height=30,
                                      drop_callback=on_drop, title_color=TITLE_COLOR, width=290)

    desk_internal_id = dpg.get_item_info(new_desk)['parent'] + 1
    cursor.execute("""UPDATE Desks SET desk_internal_id=? WHERE desk_id=?""", (desk_internal_id, desk_id))
    connector.commit()

    dpg.add_button(label='Переименовать доску', parent=new_desk,
                   callback=board_rename_callback, user_data=desk_id)
    dpg.add_button(label='Удалить доску', parent=new_desk, user_data=desk_internal_id, callback=delete_desk)
    dpg.add_button(label='Открыть доску', parent=new_desk,
                   callback=start_work_with_desk, user_data=desk_id)


def main_window():
    with dpg.window(label='MainWindow', tag='MainWindow', no_scrollbar=False,
                    horizontal_scrollbar=True, no_resize=True, no_close=True):
        dpg.set_primary_window('MainWindow', True)
        with dpg.tab_bar():
            with dpg.tab(label='Доски'):
                dpg.add_button(label='Создать доску', callback=new_board, width=290)
                with dpg.group(horizontal=False, tag='desks', indent=0):
                    req = cursor.execute("""SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;""").fetchall()
                    if len(req) == 0:
                        pass
                    else:
                        req_2 = cursor.execute("""SELECT * FROM Desks ORDER BY desk_pos;""").fetchall()
                        for i in req_2:
                            load_board(i[0], i[3])
            # with dpg.tab(label='Календарь'):
            #     DatePicker()


def rename_popup_window():
    with dpg.window(label="Переименовать доску", modal=True, show=False, tag="modal_id", no_title_bar=False,
                    width=300, height=40, no_close=False, no_resize=False):
        with dpg.group():
            text_box = dpg.add_input_text(default_value='', hint='Введите новое название:', width=280)
            with dpg.group(horizontal=True, pos=[0, 65]):
                dpg.add_button(label='Переименовать', indent=25,
                               user_data=text_box, callback=rename_board)
                dpg.add_button(label='Отмена', indent=190,
                               callback=lambda: dpg.configure_item('modal_id', show=False))


def task_window():
    with dpg.window(label="Ваши задачи", show=False, tag='tasks_window',
                    no_scrollbar=False, horizontal_scrollbar=True):
        dpg.add_button(label='На главную', callback=end_work_with_desk, width=290)
        dpg.add_child_window(height=2, border=False)
        dpg.add_button(label='Создать задачу', width=290, callback=create_new_task,
                       tag='task_creator')
        dpg.add_separator()
        dpg.add_child_window(tag='task_box')


def new_task_get_name_window():
    with dpg.window(label="Введите название заддачи", modal=True, show=False, tag="name_task_modal_id",
                    no_title_bar=False,
                    width=300, height=40, no_close=False, no_resize=False):
        with dpg.group():
            task_text_box = dpg.add_input_text(default_value='', hint='Введите название:', width=280)
            with dpg.group(horizontal=True, pos=[0, 65]):
                dpg.add_button(label='Ок', indent=25,
                               user_data=task_text_box, callback=rename_task)
                # callback=rename_board
                dpg.add_button(label='Отмена', indent=190,
                               callback=lambda: dpg.configure_item('name_task_modal_id', show=False))
