from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import psycopg2
from datetime import date
import smtplib
from email.message import EmailMessage
import global_data as gdt
import re
import main_window as mw




class LoginWindow:
    show_the_password = False


    def create_login_window(self):

        # width and height of the window
        self.width = 600
        self.height = 400

        login_win = Tk()
        self.login_win = login_win

        self.screen_width = int((self.login_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.login_win.winfo_screenheight()) / 4)

        self.login_win.geometry(f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}")
        self.login_win.title("Staff Login")
        self.login_win.resizable(FALSE, FALSE)
        self.login_win.configure(bg = "#E2B188")

        # loading image and resizing it

        self.img = Image.open("images/background_login.jpg")
        self.resized_image = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resized_image)

        # Adding Canvas

        self.canvas = Canvas(self.login_win)
        self.canvas.pack(fill=BOTH, expand=1)

        # Adding Picture to canvas
        self.canvas.create_image(300,200,image=self.new_image)

        #Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/bg1.png"))
        self.img_label = Label(self.canvas, image=self.photo0, bg="#00CED1")
        self.img_label.place(x=0,y=0,width=600,height=65)

        #Add Frame

        self.frame = Frame(self.login_win, height=200, bg="white")
        self.frame.place(x=120,y=100, width=320, height=270)

        # Login Window
        self.imglock = ImageTk.PhotoImage(Image.open("images/lock.png"))
        self.imgforget = ImageTk.PhotoImage(Image.open("images/forget.png"))
        self.imgprofile = ImageTk.PhotoImage(Image.open("images/profile.png"))
        self.imglogin = ImageTk.PhotoImage(Image.open("images/login.png"))
        self.imgpwdhide = ImageTk.PhotoImage(Image.open("images/pwd_hide.png"))
        self.imgpwdshow = ImageTk.PhotoImage(Image.open("images/pwd_show.png"))


        self.labeluser = Label(self.frame, text="Email Id", font=("Nirmala UI",15,'bold'),fg='black',bg="white")
        self.labeluser.place(x=30,y=12)
        self.labeluser.config(image=self.imgprofile, compound= LEFT)

        self.user_entry = Entry(self.frame, font=('times new roman',15),bg="#F0FFFF")
        self.user_entry.place(x=30,y=50,width=250)

        self.labelpwd = Label(self.frame, text="Password", font=("Nirmala UI",15,'bold'),fg='black',bg="white")
        self.labelpwd.place(x=30, y=80)
        self.labelpwd.config(image=self.imglock, compound=LEFT)


        self.password_entry = Entry(self.frame, font=('times new roman', 15),bg="#F0FFFF", show="*")
        self.password_entry.place(x=30, y=120, width=250)

        self.log_button = Button(self.frame,bg="white", image=self.imglogin
                                 , command=lambda: self.admin_login(), cursor='hand2', bd=0, activebackground="white")
        self.log_button.place(x=105, y=170)

        self.forget_button = Button(self.frame, bg="white", text="Forget Password?", command=lambda: self.forget_password(),
                                 font=('times new roman',13,'bold'),fg='black',cursor='hand2',bd=0,activebackground="white")
        self.forget_button.place(x=30, y=230)
        self.forget_button.configure(image=self.imgforget, compound=LEFT)

        self.pwd_show = Button(self.frame, bg="white",
                                 command=lambda: self.show_hide_password(), cursor='hand2', bd=0, activebackground="white")
        self.pwd_show.place(x=285, y=120)
        self.pwd_show.config(image=self.imgpwdhide)

        self.add_librarian_btn = Button(self.canvas, text="Add Librarian", bg="gold", font=("Nirmala UI",12,'bold'),fg='black',
                               command=lambda: self.add_librarian(), cursor='hand2', bd=2,
                               activebackground="white")
        self.add_librarian_btn.place(x=460, y=120)

        self.login_win.mainloop()

# ******************** admin login database query *********************************************
    def admin_login(self):
        if self.user_entry.get() =='' or self.password_entry.get() =='':
            messagebox.showwarning("Library Management System ","Please, enter email id and password both. ")
        elif self.check_email(self.user_entry.get())==0:
            messagebox.showwarning("Library Management System ", "Please, enter valid email address.")
            self.user_entry.delete(0,END)
        else:

            # connecting to postgres database
            connection = psycopg2.connect(user="postgres",
                                         password="1234",
                                         host="localhost",
                                         port="5432",
                                         database="lms")
            cursor = connection.cursor()
            cursor.execute("select * from librarian where user_email = %s and user_password = %s",(self.user_entry.get(),self.password_entry.get()))
            self.row = cursor.fetchone()
            if self.row == None:
                ans = messagebox.askquestion('User Not Found', 'Do you want to retry?')
                if ans == 'yes':
                    self.user_entry.delete(0,END)
                    self.password_entry.delete(0,END)
                elif ans == 'no':
                    self.login_win.destroy()
            else:
                cursor.execute(f"select user_name from librarian where user_email = '{self.user_entry.get()}'")
                self.row1= cursor.fetchone()

                connection.commit()
                connection.close()
                self.login_win.destroy()

                main_obj = mw.MainWindow()
                main_obj.create_main_window(self.row1)

                self.login_win.mainloop()




# ******************************** forget password query ****************************************
    def forget_password(self):
        if self.user_entry.get() =='':
            messagebox.showwarning("Library Management System ","Please, enter email id.")
        elif self.check_email(self.user_entry.get()) == 0:
            messagebox.showwarning("Email Not Valid","Please enter valid email address.")
            self.user_entry.delete(0,END)
        else:
            # connecting to postgres database
            connection = psycopg2.connect(user="postgres",
                                         password="1234",
                                         host="localhost",
                                         port="5432",
                                         database="lms")
            cursor = connection.cursor()
            cursor.execute(f"select user_password from librarian where user_email = '{self.user_entry.get()}'")
            self.row = cursor.fetchone()
            if(self.row==None):
                messagebox.showerror("Error","Email Id Not Exists.")
            else:
                self.send_email(self.user_entry.get(), self.row)
            connection.commit()
            connection.close()





# ******************************** Add librarian ************************************************

    def add_librarian(self):

        self.login_win.withdraw()

        # width and height of the window
        self.width = 600
        self.height = 400

        librarian_win = Toplevel()
        self.librarian_win = librarian_win

        self.screen_width = int((self.librarian_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.librarian_win.winfo_screenheight()) / 6)

        self.librarian_win.geometry(f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}")
        self.librarian_win.title("Add Librarian")
        self.librarian_win.resizable(FALSE, FALSE)
        self.librarian_win.configure(bg="#E2B188")


        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/bg1.png"))
        self.top_label = Label(self.librarian_win, image=self.photo0, bg="gold2")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.input_details = ['Name', 'Email Id', 'New Password', 'Contact No.','Address', 'Date']

        inc = -40
        inc_x = 70
        for i in range(6):
            if i == 5:
                inc += 65
            else:
                inc += 40

            self.lblLibrarian = Label(self.librarian_win, text=self.input_details[i], font=("Nirmala UI", 10, 'bold'), fg='black', bg="#E2B188")
            self.lblLibrarian.place(x=30 + inc_x, y=80+inc)

            self.lbl = Label(self.librarian_win, text="*", font=("Nirmala UI", 10, 'bold'),
                                      fg='red', bg="#E2B188")
            self.lbl.place(x=22 + inc_x, y=80 + inc)

        inc = 0

        self.enteryLibrarian1 = Entry(self.librarian_win,font=('times new roman',15),bg="#F0FFFF" )
        self.enteryLibrarian1.place(x=170 + inc_x,y=80+inc)
        inc+=40
        self.enteryLibrarian2 = Entry(self.librarian_win, font=('times new roman', 15), bg="#F0FFFF")
        self.enteryLibrarian2.place(x=170 + inc_x, y=80 + inc)
        inc+=40
        self.enteryLibrarian3 = Entry(self.librarian_win, font=('times new roman', 15), bg="#F0FFFF")
        self.enteryLibrarian3.place(x=170 + inc_x, y=80 + inc)
        inc += 40
        self.enteryLibrarian4 = Entry(self.librarian_win, font=('times new roman', 15), bg="#F0FFFF")
        self.enteryLibrarian4.place(x=170 + inc_x, y=80 + inc)
        inc+=40
        self.txtLibrarian = Text(self.librarian_win, width=20, height=2, font=('times new roman', 15),
                                         bg="#F0FFFF")
        self.txtLibrarian.place(x=170 + inc_x, y=80 + inc)
        inc+=65
        self.tLibrarian = Text(self.librarian_win, width=20, height=1, font=('times new roman', 15), bg="cyan")
        self.tLibrarian.place(x=170 + inc_x, y=80 + inc)
        self.tLibrarian.insert(INSERT, date.today().strftime("%Y-%m-%d"))
        self.tLibrarian.configure(state=DISABLED)

        self.submit_btn = Button(self.librarian_win, text="SUBMIT", bg="green", font=("Nirmala UI", 12, 'bold'),
                                        fg='black',
                                        command=lambda: self.add_librarian_query(), cursor='hand2', bd=2,
                                        activebackground="white")
        self.submit_btn.place(x=230, y=350)

        self.librarian_win.protocol("WM_DELETE_WINDOW", self.on_closing_lib_win)


#*************************** on closing librarian window ********************
    def on_closing_lib_win(self):
        self.librarian_win.destroy()
        self.login_win.deiconify()


# ************************* add librarian query ****************************

    def add_librarian_query(self):

        if (self.enteryLibrarian1.get() == '' or
            self.enteryLibrarian2.get() == '' or
            self.enteryLibrarian3.get() == '' or
            self.enteryLibrarian4.get() == '' or
            self.txtLibrarian.get("1.0", 'end-1c') == '' or
            self.tLibrarian.get('1.0',END) == ''):
            messagebox.showwarning("Library Management System ","All fields Are Required")
        elif self.check_email(self.enteryLibrarian2.get()) == 0:
            messagebox.showwarning("Email Not Valid", "Please Enter valid email id.")
        elif self.send_email(self.enteryLibrarian2.get(), self.enteryLibrarian3.get())==0:
            self.enteryLibrarian2.delete(0,END)
        else:
            # connecting to postgres database
            connection = psycopg2.connect(user="postgres",
                                         password="1234",
                                         host="localhost",
                                         port="5432",
                                         database="lms")
            cursor = connection.cursor()

            cursor.execute(f"select user_email from librarian where user_email='{self.enteryLibrarian2.get()}'")
            self.email_s = cursor.fetchone()

            if self.email_s == None:
                cursor.execute("insert into librarian(user_email, user_password, user_name, user_contact, user_address, user_doj) values ('%s','%s','%s','%s','%s','%s')"%(self.enteryLibrarian2.get(),self.enteryLibrarian3.get(),self.enteryLibrarian1.get(),self.enteryLibrarian4.get(),self.txtLibrarian.get("1.0", END),self.tLibrarian.get('1.0',END)))

                connection.commit()
                connection.close()

                messagebox.showinfo("Library Management System","Librarian Added Successfully")


                self.enteryLibrarian1.delete(0,END)
                self.enteryLibrarian2.delete(0,END)
                self.enteryLibrarian3.delete(0,END)
                self.enteryLibrarian4.delete(0,END)
                self.txtLibrarian.delete("1.0", 'end-1c')


            else:
                messagebox.showerror("Error", "Email id already exists.")

# **************************** show or hide password method **************************************
    def show_hide_password(self):


        if self.show_the_password == False:
            self.show_the_password=True
        else:
            self.show_the_password=False

        if self.show_the_password == False:
            self.pwd_show.config(image=self.imgpwdhide)
            self.password_entry.config(show="*")
        else:
            self.pwd_show.config(image=self.imgpwdshow)
            self.password_entry.config(show="")

    # *********************Email Validator******************************************

    def check_email(self, email_id):

        '''is_valid = validate_email(email_id)

        if is_valid == True:

            return 1
        else:

            return 0'''
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.match(regex, email_id)):
            return 1
        else:
            return 0



    # ******************* Send Email ****************************

    def send_email(self, email_add, email_pwd):

        gdata = gdt.HostEmailDetails()
        email_address = gdata.host_email_id()
        email_password = gdata.host_email_password()
        send_to_address = email_add

        msg = EmailMessage()
        msg['Subject']= "Do not reply"
        msg['From']= email_address
        msg['To']=send_to_address
        msg.set_content('Dear user your password for library management software is %s' % email_pwd)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
                messagebox.showinfo("Library Management System", "Your password has been sent to your email id.")
            return 1
        except Exception as e:
            messagebox.showerror("Library Management System",
                                 """Either your email id is invalid or you are not connected to internet.""")
            return 0



