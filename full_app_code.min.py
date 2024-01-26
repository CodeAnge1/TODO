AC='Введите название:'
AB='widget handler'
AA='task_creator'
A9='task_win_task_name_input'
A8='description_input'
A7='UPDATE Tasks SET task_status=? WHERE task_id=?'
A6='new_task_name_box'
A5='DELETE FROM Tasks WHERE task_id=?'
A4='Открыть доску'
A3='Удалить доску'
o='Отмена'
n='task_lists_box'
m='task_full_info'
l='Переименовать доску'
k='SELECT * FROM Desks ORDER BY desk_id DESC LIMIT 1;'
j=enumerate
i=list
c='name_task_modal_id'
b='SELECT desk_id FROM TaskLists WHERE list_id=?'
a='all_desks'
Z='app_data'
Y=len
V='tasks_window'
U='name_list_modal_id'
T='rename_text_box'
S='modal_id'
P='list_name_box'
M='MainWindow'
I=''
E=None
D=False
C=True
import os,sys,pathlib as W,sqlite3,dearpygui_extend as d,dearpygui.dearpygui as A
from PIL import Image as p
import DearPyGui_ImageController as X
Q=0
J=0
N=I
L=0
O=0
R=I
H=0
q=60,188,162
AD=34,249,49
AE=255,213,45
AF=240,55,55
K=750
AG=550
def e(relative_path):
	try:A=sys._MEIPASS
	except Exception:A=os.path.abspath('.')
	return os.path.join(A,relative_path)
A.create_context()
X.set_texture_registry(A.add_texture_registry())
Ae=X.ImageViewer()
Af=e(W.Path(Z,'db'))
AH=e(W.Path(Z,'db','desks.db'))
r=e(I)
s=W.Path(r,Z,'icons','trash_button.png')
AI=W.Path(r,Z,'fonts','SourceCodePro-SemiBold.ttf')
F=sqlite3.connect(AH,check_same_thread=D)
B=F.cursor()
B.execute('CREATE TABLE IF NOT EXISTS "Desks" (\n    "desk_id"\tINTEGER,\n    "desk_internal_id"\tINTEGER,\n    "desk_pos"\tINTEGER,\n    "desk_name"\tTEXT,\n    PRIMARY KEY("desk_id" AUTOINCREMENT)\n);')
B.execute('CREATE TABLE IF NOT EXISTS "TaskLists" (\n    "desk_id"\tINTEGER,\n    "list_id"\tINTEGER NOT NULL UNIQUE,\n    "list_internal_id"\tINTEGER,\n    "list_pos"\tINTEGER,\n    "list_name"\tTEXT,\n    PRIMARY KEY("list_id" AUTOINCREMENT),\n    FOREIGN KEY("desk_id") REFERENCES "Desks"("desk_id")\n);')
B.execute('CREATE TABLE IF NOT EXISTS "Tasks" (\n    "list_id"\tINTEGER,\n    "task_id"\tINTEGER UNIQUE,\n    "task_internal_id"\tINTEGER,\n    "task_pos"\tINTEGER,\n    "task_name"\tTEXT,\n    "task_status"\tINTEGER DEFAULT 0,\n    "task_description"\tTEXT,\n    PRIMARY KEY("task_id" AUTOINCREMENT),\n    FOREIGN KEY("list_id") REFERENCES "TaskLists"("list_id")\n);')
F.commit()
def AJ():A.setup_dearpygui();A.create_viewport(title='ToDo',max_width=K,max_height=AG,resizable=D);A.show_viewport();AK()
def AK():
	B=192;D=223;I=255;E=1040;F=D-B+1;J=E-B
	with A.font_registry():
		with A.font(AI,22)as H:
			A.add_font_range_hint(A.mvFontRangeHint_Default);A.add_font_range_hint(A.mvFontRangeHint_Cyrillic);C=E
			for G in range(B,D+1):A.add_char_remap(G,C);A.add_char_remap(G+F,C+F);C+=1
			A.bind_font(H)
def AL():AZ();Aa();Ab();Ac();Ad();AY();A.start_dearpygui();A.destroy_context()
def t(source,target):E='UPDATE Desks SET desk_pos=? WHERE desk_id=?';D='SELECT desk_id, desk_pos FROM Desks WHERE desk_internal_id=?';A=B.execute(D,(source,)).fetchone();C=B.execute(D,(target,)).fetchone();B.execute(E,(A[1],C[0]));B.execute(E,(C[1],A[0]));F.commit()
def Ag(source,target):I='UPDATE Tasks SET task_id=? WHERE task_id=?';H='SELECT list_id, task_id, task_pos, task_name, task_status, \n    task_description FROM Tasks WHERE task_internal_id=?';A=source;J=B.execute('SELECT desk_id FROM TaskLists WHERE list_id=(\n    SELECT list_id FROM Tasks WHERE task_internal_id=?)',(A,)).fetchone()[0];C=i(B.execute(H,(A,)).fetchone());D=i(B.execute(H,(target,)).fetchone());B.execute(I,(C[1],D[1]));B.execute(I,(D[1],C[1]));F.commit();G(E,E,J)
def u(sender,app_data,user_data):
	A=user_data;C=B.execute('SELECT desk_id FROM Desks WHERE desk_internal_id=?',(A,)).fetchone()[0];D=B.execute('SELECT list_id FROM TaskLists WHERE desk_id=?',(C,)).fetchall()
	for E in D:B.execute('DELETE FROM Tasks WHERE list_id=?',(E[0],))
	B.execute('DELETE FROM Desks WHERE desk_internal_id=?',(A,));B.execute('DELETE FROM TaskLists WHERE desk_id=?;',(C,));F.commit();f()
def AM(sender,app_data,user_data):
	E=B.execute(k).fetchall()
	if Y(E)==0:C=1
	else:C=E[0][0]+1
	D=d.add_movable_group(title=f"Новая_Доска_{C}",parent=a,height=40,drop_callback=t,title_color=q,width=(K-30)/2-17);A.add_button(label=l,parent=D,callback=w,user_data=C);H=A.get_item_info(D)['parent']+1;A.add_button(label=A3,parent=D,user_data=H,callback=u);A.add_button(label=A4,parent=D,callback=G,user_data=C);B.execute('INSERT INTO Desks VALUES(?, ?, ?, ?);',(C,D,C,f"Новая_Доска_{C}"));F.commit();f()
def v(sender,app_data,user_data):
	global Q;C=A.get_value(user_data)
	if C:B.execute('UPDATE Desks SET desk_name=? WHERE desk_id=?',(C,Q));F.commit();E=B.execute('SELECT desk_internal_id FROM Desks WHERE desk_id=?',(Q,)).fetchone()
	f();A.configure_item(S,show=D);A.set_value(T,I)
def AN():v(E,E,T)
def f():A.delete_item(a,children_only=C);D=B.execute(k).fetchall();A2()
def w(sender,app_data,user_data):global Q;A.configure_item(S,show=C);A.focus_item(T);Q=user_data
def Ah(sender,app_data,user_data):global H;A.configure_item(S,show=C);A.focus_item(T);H=user_data
def Ai(sender,app_data,user_data):global H;A.configure_item(U,show=C);A.focus_item(P);H=user_data
def AO():
	global O,H;I=O;D=B.execute('SELECT list_id FROM TaskLists ORDER By list_id DESC LIMIT 1').fetchone()
	if D:D=D[0]+1
	else:D=1
	H=D;J='Новый_лист';B.execute('INSERT INTO TaskLists (desk_id, list_id, list_name) VALUES(?, ?, ?)',(I,D,J));F.commit();A.configure_item(U,show=C);A.focus_item(P);G(E,E,I)
def AP(sender,app_data,user_data):
	A=user_data;C=B.execute(b,(A,)).fetchone()[0];D=B.execute('SELECT task_id FROM Tasks WHERE list_id=?',(A,)).fetchall();B.execute('DELETE FROM TaskLists WHERE list_id=?',(A,))
	for H in D:B.execute(A5,(H[0],))
	F.commit();G(E,E,C)
def AQ(sender,app_data,user_data):
	global J;C=user_data;H=B.execute('SELECT list_internal_id FROM TaskLists \n    WHERE list_id=?',(C,)).fetchone()[0];K=A.add_group(parent=H);L=B.execute('SELECT task_pos FROM Tasks WHERE list_id=?',(C,)).fetchall()
	if Y(L)==0:D=1
	else:D=B.execute('SELECT task_pos FROM Tasks WHERE list_id=? ORDER by task_pos DESC LIMIT 1',(C,)).fetchone()[0]+1
	M=f"Задача_{D}";N=0;O=I;P=C,K,D,M,N,O;B.execute('INSERT INTO Tasks (list_id, task_internal_id,\n    task_pos, task_name, task_status, task_description) VALUES(?, ?, ?, ?, ?, ?)',P);F.commit();J=B.execute('SELECT task_id FROM Tasks ORDER By task_id DESC LIMIT 1').fetchone()[0];AR();Q=B.execute(b,(C,)).fetchone()[0];G(E,E,Q)
def AR():A.configure_item(c,show=C);A.focus_item(A6)
def AS(sender,app_data,user_data):B=user_data;g(E,E,B[0]);y(B[1]);A.configure_item(m,show=D)
def x(sender,app_data,user_data):A=user_data;global J,O;g(E,E,A[0]);y(A[1]);G(E,E,O)
def y(user_data):
	C=user_data;global J;D=A.get_value(C);A.set_value(C,I)
	if D:B.execute('UPDATE Tasks SET task_description=? WHERE task_id=?',(D,J));F.commit()
def g(sender,app_data,user_data):
	C=user_data;global N,J;N=A.get_value(C);N=str(N);A.configure_item(c,show=D);A.set_value(C,I)
	if N:B.execute('UPDATE Tasks SET task_name=? WHERE task_id=?',(N,J));F.commit()
	H=B.execute('SELECT desk_id FROM TaskLists WHERE \n    list_id=(SELECT list_id FROM Tasks WHERE task_id=?)',(J,)).fetchone()[0];G(E,E,H)
def Aj():g(E,E,'task_name_box')
def z(sender,app_data,user_data):
	A=user_data;global H
	if isinstance(A,i):H=A[0];h(E,E,A[1])
	else:h(E,E,P)
def h(sender,app_data,user_data):global R,H;R=A.get_value(user_data);R=str(R);A.configure_item(U,show=D);A.set_value(P,I);B.execute('UPDATE TaskLists SET list_name=? WHERE list_id=?',(R,H));F.commit();C=B.execute(b,(H,)).fetchone()[0];G(E,E,C)
def AT(sender,app_data,user_data):A=user_data;C=B.execute('SELECT desk_id FROM TaskLists WHERE list_id=\n    (SELECT list_id FROM Tasks WHERE task_id=?)',(A[1],)).fetchone()[0];B.execute(A5,(A[1],));F.commit();G(E,E,C)
def A0(sender,app_data,user_data):
	A=user_data
	if A[5]==0 or A[5]==1:C=2
	else:C=0
	B.execute(A7,(C,A[1]));F.commit();D=B.execute('SELECT desk_id FROM TaskLists WHERE list_id=(\n    SELECT list_id FROM Tasks WHERE task_id=?)',(A[1],)).fetchone()[0];G(E,E,D)
def AU(sender,app_data,user_data):
	H=app_data;global J;D=B.execute('SELECT * FROM Tasks WHERE task_internal_id=?',(H[1],)).fetchone();J=D[1]
	if H[0]==0 and A.is_key_down(A.mvKey_Control):A.configure_item(m,show=C);A.set_value(A8,D[6]);A.set_value(A9,D[4])
	if H[0]==1:
		K=B.execute(b,(D[0],)).fetchone()[0]
		if D[5]==1:I=0
		else:I=1
		B.execute(A7,(I,D[1]));F.commit();G(E,E,K)
def G(sender,app_data,user_data):
	I=user_data;global O;O=I;A.set_item_user_data(AA,I);A.set_primary_window(M,D);A.configure_item(M,show=D);A.set_primary_window(V,C);A.configure_item(V,show=C);W=B.execute('SELECT * FROM TaskLists WHERE desk_id=? ORDER by list_pos',(I,)).fetchall();A.delete_item(n,children_only=C)
	for(Z,G)in j(W):
		H=A.add_child_window(parent=n,width=K/3-10)
		if Z!=0:A.add_spacer(before=H,width=10)
		R=A.add_group(parent=H,horizontal=C);S=A.add_input_text(default_value=G[4],parent=R,width=185,on_enter=C,callback=z);A.set_item_user_data(S,[G[1],S]);J=p.open(s);L=X.tools.image_to_dpg_texture(J);N=A.add_image_button(L,indent=191,width=17,height=20,background_color=[35,35,35],parent=R,callback=AP,user_data=G[1])
		with A.theme()as P:
			with A.theme_component(0):A.add_theme_color(A.mvThemeCol_Button,(37,37,37,255))
		A.bind_item_theme(N,P);A.add_button(label='Создать задачу',parent=H,height=35,width=217,user_data=G[1],callback=AQ);B.execute('UPDATE TaskLists SET list_internal_id=? WHERE list_id=?',(H,G[1]));F.commit();a=B.execute('SELECT * FROM Tasks WHERE list_id=?',(G[1],)).fetchall()
		for(b,E)in j(a):
			with A.group(parent=H,horizontal=C):
				if E[5]==0:Q=AF
				elif E[5]==1:Q=AE
				else:Q=AD
				if Y(E[4])<=14:T=E[4]
				else:T=f"{E[4][:11]}..."
				U=d.add_movable_group(title=T,title_color=Q,height=1,width=10,user_data=E);B.execute('UPDATE Tasks SET task_internal_id=? WHERE task_id=?',(U,E[1]));A.bind_item_handler_registry(U,AB)
				if E[5]==0 or E[5]==1:A.add_checkbox(indent=K/4-25,user_data=E,default_value=D,callback=A0)
				elif E[5]==2:A.add_checkbox(indent=K/4-25,user_data=E,default_value=C,callback=A0)
				J=p.open(s);L=X.tools.image_to_dpg_texture(J);N=A.add_image_button(L,indent=K/4+5,width=17,height=20,background_color=[35,35,35],callback=AT,user_data=E)
				with A.theme()as P:
					with A.theme_component(0):A.add_theme_color(A.mvThemeCol_Button,(37,37,37,255))
				A.bind_item_theme(N,P)
def AV():A.set_primary_window(M,C);A.configure_item(M,show=C);A.set_primary_window(V,D);A.configure_item(V,show=D)
def A1():global L;L=A.add_group(horizontal=C,parent=a)
def A2():
	global L;E=B.execute(k).fetchall()
	if Y(E)!=0:
		F=B.execute('SELECT * FROM Desks ORDER BY desk_pos;').fetchall()
		for(C,D)in j(F):
			if C%2==0:A1()
			if C!=0 and C%2==0:A.add_spacer(before=L,height=40)
			A.add_spacer(parent=L);AX(D[0],D[3])
def AW(desk_name,desk_id):D=desk_id;global L;C=d.add_movable_group(title=desk_name,parent=L,height=40,drop_callback=t,title_color=q,width=(K-30)/2-17);E=C;B.execute('UPDATE Desks SET desk_internal_id=? WHERE desk_id=?',(E,D));F.commit();A.add_button(label=l,parent=C,callback=w,user_data=D);A.add_button(label=A3,parent=C,user_data=E,callback=u);A.add_button(label=A4,parent=C,callback=G,user_data=D)
def AX(desk_id,desk_name):AW(desk_name,desk_id)
def AY():
	with A.item_handler_registry(tag=AB)as B:A.add_item_clicked_handler(callback=AU)
	with A.window(label=M,tag=M,no_scrollbar=D,horizontal_scrollbar=C,no_resize=C,no_close=C):
		A.set_primary_window(M,C);A.add_button(label='Создать доску',callback=AM,width=K-30,height=35)
		with A.child_window(border=D,height=10):A.add_separator()
		with A.group(tag=a,indent=0):A1();A2()
def AZ():
	with A.window(label=l,modal=C,show=D,tag=S,no_title_bar=D,width=300,height=140,no_close=D,no_resize=C):
		with A.group():
			A.add_spacer(height=7);B=A.add_input_text(tag=T,default_value=I,callback=AN,hint='Введите новое название:',width=280,on_enter=C);A.add_spacer(height=7)
			with A.group(horizontal=C):A.add_button(label='Переименовать',width=180,user_data=B,callback=v);A.add_button(label=o,indent=190,width=89,callback=lambda:A.configure_item(S,show=D))
def Aa():
	with A.window(label='Ваши задачи',show=D,tag=V,no_scrollbar=D,horizontal_scrollbar=C):A.add_button(label='На главную',callback=AV,width=K-30,height=35);A.add_child_window(height=2,border=D);A.add_button(label='Новый лист',width=K-30,height=35,callback=AO,tag=AA);B=A.add_child_window(horizontal_scrollbar=C,no_scrollbar=D);A.add_group(tag=n,horizontal=C,parent=B)
def Ab():
	with A.window(label='Введите название заддачи',modal=C,show=D,tag=c,no_title_bar=D,width=300,height=250,no_close=D,no_resize=C):
		with A.group():
			B=A.add_input_text(tag=A6,default_value=I,hint=AC,width=283,on_enter=C);E=A.add_input_text(height=140,width=283,hint='Введите описание',multiline=C,tag='new_description_input');A.set_item_user_data(B,[B,E]);A.set_item_callback(B,x)
			with A.group(horizontal=C):A.add_button(label='Ок',width=100,user_data=[B,E],callback=x);A.add_button(label=o,indent=110,width=173,callback=lambda:A.configure_item(c,show=D))
def Ac():
	with A.window(label='Новая задача',modal=C,show=D,tag=U,no_title_bar=D,width=300,height=120,no_close=D,no_resize=C):
		with A.group():
			B=A.add_input_text(tag=P,default_value=I,hint=AC,width=280,on_enter=C,user_data=P,callback=z)
			with A.group(horizontal=C,pos=[0,75]):A.add_button(label='Ок',width=100,indent=8,user_data=B,callback=h);A.add_button(label=o,indent=118,width=170,callback=lambda:A.configure_item(U,show=D))
def Ad():
	with A.window(label='О задаче',modal=C,show=D,tag=m,no_title_bar=D,width=300,height=250,no_close=D,no_resize=C):B=A.add_input_text(tag=A9,width=283);E=A.add_input_text(height=140,width=283,multiline=C,tag=A8);A.add_button(label='Применить',user_data=[B,E],tag='task_edit_apply',callback=AS,width=283)
if __name__=='__main__':AJ();AL()
