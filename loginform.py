from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from PIL import ImageTk, Image

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="1a_marba"
)

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")




window = Tk()
window.title("Log In")
window.geometry('1540x900')
window.configure(bg="black")

titlegame=Label (window,text="Space quest ignition:\n knowledge combat System",font=('cooper black',20),bg='black',fg='white')
titlegame.place(x=600,y=40)

frame1 = tk.Frame(window, bg='white', highlightbackground='black', highlightthickness=1)
frame1.place(x=530, y=150)
frame1.configure(width=500, height=350)

img2 = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\spaceship.jpg')
img2 = img2.resize((525, 900))
image_tk = ImageTk.PhotoImage(img2)


image_label = Label(window, image=image_tk)
image_label.image = image_tk
image_label.place(x=0, y=0)

img2 = Image.open(r'C:\Users\USER\PycharmProjects\pythonProject5\gameimage\spaceship.jpg')
img2 = img2.resize((525, 900))
image_tk = ImageTk.PhotoImage(img2)


image_label = Label(window, image=image_tk)
image_label.image = image_tk
image_label.place(x=1030, y=0)


def on_entry_click(e):
    if username_entry.get() == "Username:":
        username_entry.delete(0, "end")


def on_entry_leave(e):
    if username_entry.get() == "":
        username_entry.insert(0, "Username:")


username_entry = tk.Entry(window, width=35, border=0, bg='white', font=('mircosoft yahei ui light', 11))
username_entry.place(x=640, y=230)
username_entry.insert(0, "Username:")
username_entry.bind('<FocusIn>', on_entry_click)
username_entry.bind('<FocusOut>', on_entry_leave)
Frame(window, width=285, height=2, bg='black').place(x=640, y=250)



def on_entry_click(e):
    if password_entry.get() == "Password:":
        password_entry.delete(0, "end")
        password_entry.config(show="*")


def on_entry_leave(e):
    if password_entry.get() == "":
        password_entry.config(show="")
        password_entry.insert(0, "Password:")


password_entry = tk.Entry(window, width=35, border=0, bg='white', font=('mircosoft yahei ui light', 11))
password_entry.place(x=640, y=290)
password_entry.insert(0, "Password:")
password_entry.bind('<FocusIn>', on_entry_click)
password_entry.bind('<FocusOut>', on_entry_leave)
Frame(window, width=285, height=2, bg='black').place(x=640, y=310)

def log_in():
    username = username_entry.get()
    password = password_entry.get()


    sql = "SELECT * FROM accounts WHERE username = %s AND password = %s"
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:

        open_main_window(username)

    else:
        messagebox.showerror(message="Invalid User Name or Password")
log_in_button = tk.Button(window, padx=50, text='LOGIN', bg='black', fg='white', border=3, font=('cooper black', 11), command=log_in)
log_in_button.place(x=690, y=350)




def forgot_password():
    window.destroy()
    import FORGOTPASS
    FORGOTPASS.forgot_password()





forgotbtn = tk.Button(window, padx=5, text='FORGOT PASSWORD', bg='white', fg='black', border=0, font=('cooper black', 7),command=forgot_password)
forgotbtn.place(x=540, y=473)
Frame(window, width=110, height=2, bg='black').place(x=540, y=485)




def create_account():
    window.destroy()
    import create
    create.create_account()



createlabel = tk.Label(window, text='New user?', bg='white', font=('cooper black', 8))
createlabel.place(x=690, y=448)
create_account_button = tk.Button(window, padx=5, text='CREATE ACCOUNT', bg='white', fg='black', border=0, font=('cooper black', 8), command=create_account)
create_account_button.place(x=685, y=430)
Frame(window, width=115, height=2, bg='black').place(x=693, y=445)



def open_admin_window():
    window.withdraw()  # Hide the login window
    import adminwindow
    adminwindow.open_admin_window()

image_tk = None

# Create the 'Administrator' button
admin_button = tk.Button(window, text="Administrator", border=0, bg="white", fg="black", font=('cooper black', 9),command=open_admin_window)
admin_button.place(x=910, y=470)
Frame(window, width=100, height=2, bg='black').place(x=910, y=485)


def open_main_window(username):
    window.withdraw()

    import main
    main.window(username)










window.mainloop()