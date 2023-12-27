import mysql.connector
from tkinter import *
from tkinter import messagebox
import mysql.connector

def on_click(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, END)

def off_click(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)

def find(data, ent_name, lbl_forget, frm_forget):
    name = ent_name.get()
    try:
        data = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Please input your database password here
            database='1a_marba'
        )
        mycursor = data.cursor()
        sql = "SELECT * FROM accounts WHERE username=%s"
        mycursor.execute(sql, (name,))
        result = mycursor.fetchone()

        if result:
            def on_enter1(e):
                ent_pass.delete(0, 'end')

            def on_leave2(e):
                password = ent_pass.get()
                if password == '':
                    ent_pass.insert(0, 'Username')

            lbl_forget.config(text="Change Password")

            ent_pass = Entry(frm_forget, width=20, font=("Goudy Old Style", 11), border=0)
            ent_pass.insert(0, "Change Password:")
            Frame(frm_forget, width=170, height=2, bg='black').place(x=40, y=130)
            ent_pass.bind('<FocusIn>', on_enter1)
            ent_pass.bind('FocusOut', on_leave2)
            ent_pass.place(x=40, y=100)
            ent_pass.bind('<FocusIn>', lambda e: on_click(ent_pass, "Change Password:"))
            ent_pass.bind('<FocusOut>', lambda e: off_click(ent_pass, "Change Password:"))

            btn_info = Button(frm_forget, width=18, pady=7, text="change", bg='blue', fg='white', border=0,
                      font=('Microsoft YaHei UI Light', 9), command=lambda: change_password(data, ent_pass, ent_name, frm_forget))
            btn_info.place(x=60, y=160)
        else:
            messagebox.showerror(title="Invalid choice", message="Account not found")
    except mysql.connector.Error as e:
        messagebox.showerror(title="Database Error", message=f"Error: {e}")
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'data' in locals():
            data.close()

def change_password(data, ent_pass, ent_name, lmain):
    p = ent_pass.get()
    e = ent_name.get()

    try:
        data = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Please input your database password here
            database='1a_marba'
        )
        mycursor = data.cursor()
        sql = "UPDATE accounts SET password = %s WHERE username = %s"
        var = (p, e)
        mycursor.execute(sql, var)
        data.commit()

        messagebox.showinfo(title="Password Changed", message="Done")
        lmain.destroy()


    except mysql.connector.Error as e:
        messagebox.showerror(title="Database Error", message=f"Error: {e}")
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'data' in locals():
            data.close()
def forgot_password():
    from PIL import ImageTk, Image
    lmain = Tk()
    lmain.title("Log In")
    lmain.geometry('925x500+300+200')
    lmain.configure(bg="#fff")
    lmain.resizable(False, False)

    def on_enter(e):
        ent_name.delete(0, 'end')

    def on_leave(e):
        name = ent_name.get()
        if name == '':
            ent_name.insert(0, 'Username')

    img = Image.open(r'C:\Users\USER\Downloads\spaceship.JPG')
    img = img.resize((925, 500))
    image_tk = ImageTk.PhotoImage(img)

    image_label = Label(lmain, image=image_tk)
    image_label.image = image_tk
    image_label.pack()

    frm_forget = Frame(lmain, width=250, height=250, bg="white")
    frm_forget.place(x=35, y=100)

    lbl_forget = Label(frm_forget, text="Find Account Portal", font=("Goudy Old Style", 15), bg="white", fg='blue',
                       cursor="cross")
    lbl_forget.place(x=45, y=20)

    ent_name = Entry(frm_forget, width=20, font=("Goudy Old Style", 11), border=0)
    ent_name.insert(0, "Enter username")
    ent_name.place(x=45, y=100)
    Frame(frm_forget, width=170, height=2, bg='black').place(x=40, y=130)
    ent_name.bind('<FocusIn>', on_enter)
    ent_name.bind('FocusOut', on_leave)

    btn_info = Button(frm_forget, width=18, pady=7, text="Find Account", bg='blue', fg='white', border=0,
                      font=('Microsoft YaHei UI Light', 9),command=lambda: find(None, ent_name, lbl_forget, frm_forget))
    btn_info.place(x=60, y=170)

    lmain.mainloop()

if __name__ == "__main__":
    forgot_password()