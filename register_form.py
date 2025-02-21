from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import sqlite3 as sql
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def registraiton_form(main_window):
    main_window.withdraw()
    root = Toplevel()
    root.title("Register Form")
    root.geometry("600x350+450+200")
    root.resizable(False, False)
    root.configure(bg="#70e1ef")
    
    con = sql.connect("USERS_INFO.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS USERS_INFO (name TEXT, surname TEXT, e_mail TEXT, age INT, department TEXT, sex TEXT, image BLOB, password INT, user_name TEXT)")  

    global img_data  
    img_data = None

    # Functions
    def send_email(user_name, passwordd, name):
    
        sender = EMAIL_SENDER
        password = EMAIL_PASSWORD
        to = e_mail_entry.get()
        subject = "User Information"
        
        message = f"""
        <html>
        <head>
          <style>
            body {{
              font-family: Arial, sans-serif;
              background-color: #f4f4f4;
            }}
            .container {{
              padding: 20px;
              background-color: #ffffff;
              border-radius: 8px;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            h1 {{
              color: #4CAF50;
            }}
            p {{
              font-size: 16px;
            }}
            .bold {{
              font-weight: bold;
              color: #333333;
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <h1>WELCOME {name}</h1>
            <h1>Registration is successful!</h1>
            <p>User Name : <span class="bold">{user_name}</span></p>
            <p>Password : <span class="bold">{passwordd}</span></p>
          </div>
        </body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'html'))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())
        server.close()
        
            
    def warning_():
        if messagebox.askquestion("WARNING", "Are you sure you want to clear all fields?") == "yes":
            clear_entries()
    
    def clear_entries():
        name_entry.delete(0, END)
        surname_entry.delete(0, END)
        e_mail_entry.delete(0,END)
        spinbox.delete(0, END)
        spinbox.insert(0, 1)
        sval.set("DEPARTMENTS")
        ival.set(0)
        ivar.set(0)
        button_save.config(state="disabled")
        button_image.config(image=photoResized)
    
    def selected():
        if ival.get() == 1:
            button_save.config(state="normal")
        else:
            button_save.config(state="disabled")
    
    def resim_yukle():
        global img_data
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.gif")])
        
        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            button_image.config(image=img_tk)
            button_image.image = img_tk
            
            # BINARY FORM
            with open(file_path, 'rb') as file:
                img_data = file.read()
    
    def save_():
        global img_data
        name = name_entry.get().upper().strip()
        surname = surname_entry.get().upper().strip()
        e_mail = e_mail_entry.get()
        age = spinbox.get()
        department = sval.get()
        sex = "Male" if ivar.get() == 1 else "Female"
        
        # check data
        cur.execute("SELECT * FROM USERS_INFO WHERE name = ? AND surname = ? AND e_mail = ? AND age = ? AND department = ? AND sex = ? AND image = ? ",
                    (name, surname, e_mail, age, department, sex, img_data))
        existing_user = cur.fetchone()
        
        if existing_user:
            messagebox.showwarning("Duplicate Entry", "This user is already registered!")
            clear_entries()
        else:
            passwordd = random.randint(1000,10000)
            user_name = (f"{name}_{surname}").lower()
            cur.execute("INSERT INTO USERS_INFO (name, surname, e_mail, age, department, sex, image, password, user_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (name, surname, e_mail, age, department, sex, img_data, passwordd, user_name))
            con.commit()
            messagebox.showinfo("INFORMATION", "SAVED! \n Check your e-mail !")
            send_email(user_name,passwordd,name)

    def back():
        messagebox.showinfo("GO BACK", "You are going back to the previous window.")
        root.destroy()
        main_window.deiconify()

    # Frames
    frame1 = Frame(root, bg="#70e1ef")
    frame1.grid(row=0, column=0)
    frame2 = Frame(root, bg="#70e1ef")
    frame2.grid(row=0, column=1)
    frame3 = Frame(root, bg="#70e1ef")
    frame3.grid(row=0, column=2)
    frame4 = Frame(root, bg="#70e1ef")
    frame4.grid(row=1, column=2)

    # Labels and Entries
    properties = [
        "Name",
        "Surname",
        "E-Mail",
        "Age",
        "Department",
        "Sex"
    ]
    
    for property in properties:
        Label(frame1, text=property, font=("Arial 14 bold"), bg="#70e1ef", pady=5, padx=5).pack(anchor="w")
    
    for i in range(6):
        Label(frame2, text=":", font=("Arial 14 bold"), padx=5, pady=5, bg="#70e1ef").pack()
    
    name_entry = Entry(frame3, relief="flat", font="Arial 14", justify="center")
    name_entry.pack(padx=5, pady=5)
    
    surname_entry = Entry(frame3, relief="flat", font="Arial 14", justify="center")
    surname_entry.pack(padx=5, pady=5)

    e_mail_entry = Entry(frame3, relief="flat", font="Arial 14", justify="center")
    e_mail_entry.pack(padx=5, pady=5)
    
    spinbox = Spinbox(frame3, relief="flat", font="Arial 14 bold", width=19, from_=1, to=99, justify="center")
    spinbox.pack(padx=5, pady=5)

    
    departments = [
        "Computer Engineering",
        "Electrical and Electronic Engineering",
        "Aerospace Engineering",
        "Civil Engineering",
        "Industrial Engineering",
        "Environmental Engineering",
        "Geological Engineering",
        "Pharmacy",
        "Audiology"
    ]
    sval = StringVar(value="DEPARTMENTS")
    option = OptionMenu(frame3, sval, *departments)
    option.config(font=("Arial 7 bold"), width=37, height=1, pady=4, padx=3, relief="flat")
    option.pack(padx=5, pady=5)
    
    # Radio buttons
    ivar = IntVar()
    male_button = Radiobutton(frame3, text="Male", variable=ivar, value=1, bg="#70e1ef", font="Arial 12", activebackground="#70e1ef", relief="flat")
    male_button.pack(padx=5, pady=5, side="left")
    
    female_button = Radiobutton(frame3, text="Female", variable=ivar, value=2, bg="#70e1ef", font="Arial 12", activebackground="#70e1ef", relief="flat")
    female_button.pack(padx=3, pady=5, side="bottom")
    
    # Checkbutton (initially unchecked)
    ival = IntVar(value=0)
    check = Checkbutton(frame4, variable=ival, text='I have hit "agree" to that', font=("Arial 12"), width=22, command=selected)
    check.pack()
    
    # Buttons
    button_save = Button(root, text="SAVE", relief="flat", font=("Arial 12 bold"), bg="GREEN", width=12, height=1, command=save_, state="disabled")
    button_save.place(x=100, y=275)
    
    button_clear = Button(root, text="CLEAR", relief="flat", font=("Arial 12 bold"), bg="yellow", width=12, height=1, command=warning_)
    button_clear.place(x=250, y=275)
    
    photo = PhotoImage(file="Profile.png")
    photoResized = photo.subsample(6, 6)

    button_image = Button(root, text="Upload", compound="top", relief="flat", font=("Arial 12 bold"), image=photoResized, command=resim_yukle)
    button_image.place(x=415, y=5, width=150, height=175)
    
    button_return = Button(root, text="RETURN", relief="flat", font=("Arial 12 bold"), bg="red", width=12, height=1, command=back)
    button_return.place(x=400, y=275)
    
    root.mainloop()
    con.close()
