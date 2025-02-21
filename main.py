from tkinter import * 
from register_form import registraiton_form
import os
import sqlite3 as sql
from tkinter import messagebox
from PIL import Image, ImageTk
import io

main_window = Tk()
main_window.geometry("375x170+450+200")
main_window.resizable(False,False)
main_window.title("Login System")
main_window.configure(bg="#70e1ef")


con = sql.connect("USERS_INFO.db")
cur = con.cursor()

con = sql.connect("USERS_INFO.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS USERS_INFO (name TEXT, surname TEXT, e_mail TEXT, age INT, department TEXT, sex TEXT, image BLOB, password INT, user_name TEXT)")
con.commit()


def user_dashboard(existing_user):
    dashboard = Toplevel(main_window)
    name = existing_user[0].split("_")[0].capitalize()
    dashboard.title(f"{name} Dashboard")
    dashboard.geometry("750x400+500+250")
    dashboard.configure(bg="#70e1ef")
    dashboard.resizable(False, False)

    frame_info = Frame(dashboard, bg="#70e1ef")
    frame_info.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)

    properties = ["Name", "Surname", "Age", "Department", "Sex"]
    
    for i, property in enumerate(properties):
        Label(frame_info, text=property, anchor="w", font=("Arial", 12, "bold"), bg="#70e1ef").grid(row=i, column=0, sticky="w", pady=5)
        Label(frame_info, text=":", font=("Arial", 12, "bold"), bg="#70e1ef").grid(row=i, column=1, sticky="w", pady=5)
        Label(frame_info, text=existing_user[i], anchor="w", font=("Arial", 12), bg="#70e1ef").grid(row=i, column=2, sticky="w", pady=5)

    # Profil fotoğrafı
    img = existing_user[6]
    image = Image.open(io.BytesIO(img))
    img_resized = image.resize((200, 250))
    img = ImageTk.PhotoImage(img_resized)

    frame_image = Frame(dashboard, bg="#70e1ef")
    frame_image.grid(column=1, row=0, padx=20, pady=20)

    image_label = Label(frame_image, image=img, width=200, height=250)
    image_label.image = img
    image_label.pack()

    # Logout butonu
    Button(dashboard, text="Logout", command=dashboard.destroy, width=15, height=2, font=("Arial", 10, "bold"), bg="red", fg="white").place(x=300, y=300)



def clear():
    entry_name.delete(0,END)
    entry_password.delete(0,END)


def admin_panel():
    name = entry_name.get().strip()
    password = entry_password.get().strip()
    cur.execute("SELECT * FROM USERS_INFO WHERE user_name = ? AND password = ? ",
                    (name, password))
    existing_user = cur.fetchone()

    if name == "admin" and password == "admin.":
        clear()
        os.startfile("USERS_INFO.db")

    elif existing_user :
        clear()
        user_dashboard_delayed(existing_user)
    else :
        messagebox.showinfo("INFO","There is no such a user registration !")

def user_dashboard_delayed(existing_user): 
    main_window.after(500, lambda: user_dashboard(existing_user))


entry_name = Entry(main_window, font = ("Arial 12 bold"), )
entry_name.place(x= 120, y= 20, width=150)
entry_name.focus()

entry_password = Entry(main_window, show="*" , font = ("Arial 12 bold"))
entry_password.place(x=120, y=50, width=150)



name_label = Label(main_window, text="Username  :", font = ("Arial 12 "), bg="#70e1ef")
name_label.place(x=30, y=20)
 
password_label = Label(main_window, text="password  :" , font = ("Arial 12 "), bg="#70e1ef")
password_label.place(x=30, y=50)

registeration = Button(main_window, text="REGISTER",relief="groove",command = lambda : registraiton_form(main_window) )
registeration.place(x=250,y=90,width=100,height=50)

entry_button = Button(main_window, text="LOGIN",relief="groove" , command = admin_panel )
entry_button.place(x=30,y=90,width=100,height=50)

exit_button = Button(main_window, text="EXIT",relief="groove",command=exit )
exit_button.place(x=140,y=90,width=100,height=50)

main_window.mainloop()