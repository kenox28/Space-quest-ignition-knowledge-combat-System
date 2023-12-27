from tkinter import *
from tkinter import messagebox
import mysql.connector

from PIL import ImageTk, Image

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="1a_marba"
)
cursor = db.cursor()

# Create a table for storing user accounts
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

def create_account():
    create_window = Tk()
    create_window.title("Create Account")
    create_window.geometry('925x500+300+200')
    create_window.resizable(False, False)

    img = Image.open(r'C:\Users\USER\Downloads\spaceship.JPG')
    img = img.resize((925, 500))
    image_tk = ImageTk.PhotoImage(img)

    image_label = Label(create_window, image=image_tk)
    image_label.image = image_tk
    image_label.pack()

    frm = Frame(create_window, width=380, height=200, bg='white')
    frm.place(x=270, y=150)

    create = Label(frm, text='Create Account', fg='blue', bg='white', font=('Goudy Old Style', 15))
    create.place(x=130, y=10)

    username_label = Label(frm, text="Username:", bg='white', font=('Microsoft YaHei UI Light', 10, 'bold'))
    username_label.place(x=40, y=60)
    username_entry = Entry(frm, border=0, font=('Microsoft YaHei UI Light', 10))
    username_entry.place(x=120, y=63)

    Frame(frm, width=170, height=2, bg='black').place(x=120, y=83)

    password_label = Label(frm, text="Password:", bg='white', font=('Microsoft YaHei UI Light', 10, 'bold'))
    password_label.place(x=45, y=110)
    password_entry = Entry(frm, border=0, show="*", font=('Microsoft YaHei UI Light', 10))
    password_entry.place(x=120, y=115)

    Frame(frm, width=170, height=2, bg='black').place(x=120, y=133)

    # Create a button to create the account
    def save_account():
        username = username_entry.get()
        password = password_entry.get()
        sql = "SELECT * FROM accounts WHERE username = %s AND password = %s"
        val = (username, password)
        cursor.execute(sql, val)
        result = cursor.fetchone()


        if result:
            messagebox.showerror(message="Account is Taken")

        elif username_entry and password_entry == "":
            messagebox.showerror(message="Fill all requirements needs")

        else:
            # Insert the new account into the database
            sql = "INSERT INTO accounts (username, password) VALUES (%s, %s)"
            val = (username, password)
            cursor.execute(sql, val)
            db.commit()

            messagebox.showinfo(message="Account Created")
            create_window.destroy()

    create_button = Button(frm,width=16,pady=3, text="Create Account", border=0, bg='blue', fg='white', font=('Microsoft YaHei UI Light',10), command=save_account)
    create_button.place(x=130,y=155)
