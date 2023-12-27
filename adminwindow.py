from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="1a_marba"
)
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS settings (id INT AUTO_INCREMENT PRIMARY KEY, vel INT, maxfire INT, firevel INT)")

cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), message TEXT)")

db.commit()

def open_admin_window():
    from PIL import ImageTk, Image
    admin_window = Toplevel()
    admin_window.title("Administrator Window")
    admin_window.geometry('925x500+300+200')
    admin_window.configure(bg='white')
    admin_window.resizable(False, False)
    frame = Frame(admin_window, width=350, height=350, bg='white')
    frame.place(x=520, y=70)

    heading = Label(frame, text='Sign in', fg='blue', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    img = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\spaceship.jpg')
    img = img.resize((450, 425))
    image_tk = ImageTk.PhotoImage(img)

    image_label = Label(admin_window, image=image_tk)
    image_label.image = image_tk
    image_label.place(x=25, y=40)
    def on_entry_click(e):
        if username_entry.get() == "Username:":
            username_entry.delete(0, "end")

    def on_entry_leave(e):
        if username_entry.get() == "":
            username_entry.insert(0, "Username:")

    username_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    username_entry.place(x=30, y=80)
    username_entry.insert(0, 'Username:')
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
    username_entry.bind('<FocusIn>', on_entry_click)
    username_entry.bind('<FocusOut>',on_entry_leave)
    def on_entry_click(e):
        if password_entry.get() == "Password:":
            password_entry.delete(0, "end")
            password_entry.config(show="*")

    def on_entry_leave(e):
        if password_entry.get() == "":
            password_entry.config(show="")
            password_entry.insert(0, "Password:")

    password_entry = Entry(frame, width=25, fg='black', border=0, bg='white',
                           font=('Microsoft YaHei UI Light', 11))
    password_entry.place(x=30, y=145)
    password_entry.insert(0, 'Password:')
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=170)
    password_entry.bind('<FocusIn>', on_entry_click)
    password_entry.bind('<FocusOut>',on_entry_leave)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        # SQL query to fetch the user with provided username and password
        sql = "SELECT `id`, `username`, `password` FROM `game_admin` WHERE `username` = %s AND `password` = %s"
        val = (username, password)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result:
            admin_window.destroy()
            open_admin_dashboard()
        else:
            messagebox.showerror(message="Invalid User Name or Password")

    Button(frame, width=38, pady=7, text='Sign in', bg='blue', fg='white', border=0,command=login).place(x=40,y=204)

    admin_window.mainloop()

def open_admin_dashboard():
    dashboard_window = Tk()
    dashboard_window.title("Admin Dashboard")
    dashboard_window.geometry('1500x800')
    dashboard_window.configure(bg='gray')
    FONT = ('cooper black',11)


    def search_in_treeview(treeview, search_entry):
        query = search_entry.get().lower()
        if query:
            found_items = []
            for item in treeview.get_children():
                values = treeview.item(item, 'values')
                if any(query in str(value).lower() for value in values):
                    found_items.append(item)
            treeview.selection_set(found_items)
        else:
            treeview.selection_remove(treeview.selection())


    def load_nameplayer_data():
        cursor.execute("SELECT * FROM nameplayer")
        rows = cursor.fetchall()
        for row in rows:
            nameplayer_treeview.insert('', 'end', values=row)


    def load_settings():
        cursor.execute("SELECT * FROM settings")
        rows = cursor.fetchall()
        for row in rows:
            settings.insert('', 'end', values=row)

    def add_settings():
        vel_val = int(vel_entry.get())
        maxfire_val = int(maxfire_entry.get())

        firevel_input = firevel_entry.get()
        try:
            firevel_val = int(firevel_input)
        except ValueError:
            messagebox.showerror("Error", "FireVel must be a valid integer")
            return

        cursor.execute("INSERT INTO settings (vel, maxfire, firevel) VALUES (%s, %s, %s)",
                       (vel_val, maxfire_val, firevel_val))
        db.commit()
        settings.delete(*settings.get_children())
        load_settings()

    def delete_settings():
        selected = settings.selection()
        if selected:
            for item in selected:
                item_id = settings.item(item, 'values')[0]
                cursor.execute("DELETE FROM settings WHERE id = %s", (item_id,))
                db.commit()
                settings.delete(item)

    def edit_settings():
        selected = settings.selection()
        if selected:
            for item in selected:
                item_id = settings.item(item, 'values')[0]
                vel_val = int(vel_entry.get())
                maxfire_val = int(maxfire_entry.get())
                firevel_val = int(firevel_entry.get())  # Get FireVel value from entry

                # Delete existing data from the treeview
                settings.delete(*settings.get_children())

                cursor.execute("UPDATE settings SET vel = %s, maxfire = %s, firevel = %s WHERE id = %s",
                               (vel_val, maxfire_val, firevel_val, item_id))
                db.commit()
                load_settings()

    def delete(display):
        selected_item = display.focus()
        if selected_item:
            username = display.item(selected_item)['values'][1]
            sql = "DELETE FROM accounts WHERE username = %s"
            val = (username,)
            cursor.execute(sql, val)
            db.commit()
            show(display)
    def add_account():
        username_val = username_entry.get()
        password_val = password_entry.get()

        cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username_val, password_val))
        db.commit()
        show(display)

    def edit_account():
        selected_item = display.focus()
        if selected_item:
            current_username = display.item(selected_item)['values'][1]
            current_password = display.item(selected_item)['values'][2]

            new_username = username_entry.get()
            new_password = password_entry.get()

            cursor.execute("UPDATE accounts SET username = %s, password = %s WHERE username = %s AND password = %s",
                           (new_username, new_password, current_username, current_password))
            db.commit()

            show(display)
    def show(display):
        display.delete(*display.get_children())
        sql = "SELECT * FROM accounts"
        cursor.execute(sql)
        data_list = cursor.fetchall()
        for data in data_list:
            display.insert("", END, values=data)
    def load_questions():
        cursor.execute("SELECT * FROM game_question")
        rows = cursor.fetchall()
        for row in rows:
            question.insert('', 'end', values=row)

    def add_question():
        question_text = questionentry.get()
        answer_text = answerentry.get()

        cursor.execute("INSERT INTO game_question (question, answer) VALUES (%s, %s)",
                       (question_text, answer_text))
        db.commit()

        question.delete(*question.get_children())
        load_questions()

    def delete_question():
        selected_item = question.focus()
        if selected_item:
            question_id = question.item(selected_item, 'values')[0]
            cursor.execute("DELETE FROM game_question WHERE id = %s", (question_id,))
            db.commit()
            question.delete(selected_item)

    def edit_question():
        selected_item = question.focus()
        if selected_item:
            question_id = question.item(selected_item, 'values')[0]
            updated_question = questionentry.get()
            updated_answer = answerentry.get()
            cursor.execute("UPDATE game_question SET question = %s, answer = %s WHERE id = %s",
                           (updated_question, updated_answer, question_id))
            db.commit()
            question.delete(*question.get_children())
            load_questions()


    #treeview og entry sa name og player

    nameplayer_frame = Frame(dashboard_window, bg='green')
    nameplayer_frame.place(width=700, height=250, x=700, y=300)

    nameplayer_treeview = ttk.Treeview(nameplayer_frame, columns=("id", "playerentername1", "playerentername2", "winner"), show="headings")
    nameplayer_treeview.heading("id", text="ID")
    nameplayer_treeview.heading("playerentername1", text="Player Name 1")
    nameplayer_treeview.heading("playerentername2", text="Player Name 2")
    nameplayer_treeview.heading("winner", text="Winner")

    nameplayer_treeview.column("id", width=50, anchor=CENTER)
    nameplayer_treeview.column("playerentername1", width=120, anchor=CENTER)
    nameplayer_treeview.column("playerentername2", width=120, anchor=CENTER)
    nameplayer_treeview.column("winner", width=120, anchor=CENTER)
    nameplayer_treeview.pack(fill=BOTH, expand=1)
    load_nameplayer_data()
    searchname=Label(dashboard_window,text="Search player name",font=FONT,fg='red',bg='black')
    searchname.place(x=850,y=610)
    search_entry_nameplayer = Entry(dashboard_window)
    search_entry_nameplayer.place(x=1010, y=610)
    searchlabel=Label(dashboard_window,text="GAME HISTORY",font=FONT,fg='red',bg='gray')
    searchlabel.place(x=950,y=550)

    #treeview og entry sa settings sa game

    settings = ttk.Treeview(dashboard_window, columns=('ID', 'Velocity', 'MaxFire', 'FireVel'), show='headings')
    settings.heading('ID', text='ID')
    settings.heading('Velocity', text='Velocity')
    settings.heading('MaxFire', text='MaxFire')
    settings.heading('FireVel', text='FireVel')
    load_settings()

    settings.column("ID", width=50, anchor=CENTER)
    settings.column("Velocity", width=50, anchor=CENTER)
    settings.column("MaxFire", width=50, anchor=CENTER)
    settings.column("FireVel", width=50, anchor=CENTER)
    settings.place(width=600, height=100, x=50, y=20)

        # Add Settings Frame

    vel_label = Label(dashboard_window, text="Velocity:",font=FONT,fg='red',bg='black')
    vel_label.place(x=50, y=150)
    vel_entry = Entry(dashboard_window)
    vel_entry.place(x=50, y=120)

    maxfire_label = Label(dashboard_window, text="Max Fire:",font=FONT,fg='red',bg='black')
    maxfire_label.place(x=200, y=150)
    maxfire_entry = Entry(dashboard_window)
    maxfire_entry.place(x=200, y=120)

    firevel_label = Label(dashboard_window, text="FireVel:",font=FONT,fg='red',bg='black')
    firevel_label.place(x=350, y=150)
    firevel_entry = Entry(dashboard_window)
    firevel_entry.place(x=350, y=120)
    searchlabel=Label(dashboard_window,text="Search",font=FONT,fg='red',bg='black')
    searchlabel.place(x=500,y=150)
    search_entry_settings = Entry(dashboard_window)
    search_entry_settings.place(x=500, y=120)


    #treeview and entry sa question og answer

    questionframe = Frame(dashboard_window,bg='blue')
    questionframe.place(width=700,height=300,x=20,y=300)

    question = ttk.Treeview(questionframe, columns=('id','question','answer','date'),show="headings")
    question.heading("id", text="ID")
    question.heading("question",text="Questions")
    question.heading("answer",text="Answer")
    question.heading("date",text="Date")


    question.column("id",width=10,anchor=CENTER)
    question.column("question",width=40,anchor=CENTER)
    question.column("answer",width=30,anchor=CENTER)
    question.column("date",width=30,anchor=CENTER)
    question.pack(fill=BOTH,expand=1)


    questionlabel = Label(dashboard_window,text="Question Game",font=FONT,fg='red',bg='black')
    questionlabel.place(x=20,y=610)
    questionentry = Entry(dashboard_window)
    questionentry.place(x=140,y=610)

    answerlabel = Label(dashboard_window, text="answer",font=FONT,fg='red',bg='black')
    answerlabel.place(x=270, y=610)
    answerentry = Entry(dashboard_window)
    answerentry.place(x=340, y=610)
    searchquestion = Label (dashboard_window,text="search qeustion",font=FONT,fg='red',bg='black')
    searchquestion.place(x=465,y=610)
    search_entry_question = Entry(dashboard_window)
    search_entry_question.place(x=600, y=610)
    load_questions()


    #treeview og entry sa username and passowrd



    root_frame = Frame(dashboard_window, bg='orange')
    root_frame.place(width=300, height=250, x=720, y=20)

    display = ttk.Treeview(root_frame, columns=("id", "username", "password"), show="headings")
    display.heading("id", text="ID")
    display.heading("username", text="Username")
    display.heading("password", text="Password")

    display.column("id", width=40, anchor=CENTER)
    display.column("username", width=80, anchor=CENTER)
    display.column("password", width=70, anchor=CENTER)
    display.pack(fill=BOTH, expand=1)
    show(display)

    username_label = Label(dashboard_window, text="Username:",font=FONT,fg='red',bg='black')
    username_label.place(x=1020, y=20)
    username_entry = Entry(dashboard_window)
    username_entry.place(x=1110, y=20)

    password_label = Label(dashboard_window, text="Password:",font=FONT,fg='red',bg='black')
    password_label.place(x=1020, y=60)
    password_entry = Entry(dashboard_window, show="*")
    password_entry.place(x=1110, y=60)
    searchdisplay=Label(dashboard_window,text="Search Account",font=FONT,fg='red',bg='black')
    searchdisplay.place(x=1240,y=20)
    search_entry_display = Entry(dashboard_window)
    search_entry_display.place(x=1370, y=20)


    #buttons



    questionAddbutton = Button(dashboard_window, font=FONT, text="Add Question",fg='red',bg='black', command=add_question)
    questionAddbutton.place(x=20, y=640)

    delete_question_button = Button(dashboard_window,font=FONT, text="Delete Question",fg='red',bg='black', command=delete_question)
    delete_question_button.place(x=150, y=640)

    edit_question_button = Button(dashboard_window,font=FONT ,text="Edit Question",fg='red',bg='black', command=edit_question)
    edit_question_button.place(x=300, y=640)

    search_button_question = Button(dashboard_window, text="Search",font=FONT,fg='red',bg='black',
                                    command=lambda: search_in_treeview(question, search_entry_question))
    search_button_question.place(x=500, y=640)

    game=Label(dashboard_window,bg='gray',text="GAME QUESTION",font=FONT,fg='red')
    game.place(x=300,y=680)

    add_button = Button(dashboard_window, text="Add settings", font=FONT,fg='red',bg='black',command=add_settings)
    add_button.place(x=50, y=200)

    delete_button_1 = Button(dashboard_window, text="Delete Settings", font=FONT,fg='red',bg='black',command=delete_settings)
    delete_button_1.place(x=180, y=200)

    edit_button = Button(dashboard_window, text="Edit Settings",font=FONT ,fg='red',bg='black',command=edit_settings)
    edit_button.place(x=370, y=200)

    gamesettings=Label(dashboard_window,text="GAMES SETTINGS",font=FONT ,fg='red',bg='gray')
    gamesettings.place(x=280,y=250)

    search_button_settings = Button(dashboard_window, text="Search settings",font=FONT,fg='red',bg='black',
                                    command=lambda: search_in_treeview(settings, search_entry_settings))
    search_button_settings.place(x=500, y=200)

    delete_account = Button(dashboard_window, text='Delete',font=FONT,fg='red',bg='black' ,command=lambda: delete(display))
    delete_account.place(x=1050, y=100)

    edit_button_2 = Button(dashboard_window, text="Edit Account",font=FONT,fg='red',bg='black' ,command=edit_account)
    edit_button_2.place(x=1130, y=100)

    add_button_2 = Button(dashboard_window, text="Add Account",font=FONT,fg='red',bg='black' ,command=add_account)
    add_button_2.place(x=1250, y=100)

    gameacc=Label(dashboard_window,text="USERS ACCOUNT",font=FONT ,fg='red',bg='gray')
    gameacc.place(x=1130,y=230)

    search_button_display = Button(dashboard_window, text="Search",font=FONT,fg='red',bg='black',
                                   command=lambda: search_in_treeview(display, search_entry_display))
    search_button_display.place(x=1370, y=100)

    search_button_nameplayer = Button(dashboard_window, text="Search",font=FONT,fg='red',bg='black',
                                      command=lambda: search_in_treeview(nameplayer_treeview, search_entry_nameplayer))
    search_button_nameplayer.place(x=1150, y=610)




    dashboard_window.mainloop()

open_admin_window()




