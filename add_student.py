from tkinter import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
import global_data as gdt
from tkinter import ttk
from tkcalendar import *
from tkinter import filedialog
import os
from tkinter import messagebox
import re
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import psycopg2




class AddStudent:

    image_uploaded = False
    is_email_sent = False

    def add_student_window(self, mainloop):
        # width and height of the window
        self.width = 600
        self.height = 400
        self.main_win_loop = mainloop
        student_win = Toplevel()
        self.student_win = student_win

        self.screen_width = int((self.student_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.student_win.winfo_screenheight()) / 6)

        self.student_win.geometry(f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}")
        self.student_win.title("Add Student")
        self.student_win.resizable(FALSE, FALSE)
        self.student_win.configure(bg="#fbedff")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/bg1.png"))
        self.top_label = Label(self.student_win, image=self.photo0, bg="#d0a1ff")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.input_details = ['Name', 'Email Id', 'Gender', 'Contact No.', 'Date of Birth', 'Address']

        inc = -40
        inc_x = 10
        for i in range(6):

            inc += 40

            self.lblstd = Label(self.student_win, text=self.input_details[i], font=("Nirmala UI", 10, 'bold'),
                                      fg='black', bg="#fbedff")
            self.lblstd.place(x=30 + inc_x, y=80 + inc)

            self.lbl = Label(self.student_win, text="*", font=("Nirmala UI", 10, 'bold'),
                             fg='red', bg="#fbedff")
            self.lbl.place(x=22 + inc_x, y=80 + inc)

        inc = 0

        self.name_entery = Entry(self.student_win, font=('times new roman', 15))
        self.name_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.email_entery = Entry(self.student_win, font=('times new roman', 15))
        self.email_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.gender_entery = ttk.Combobox(self.student_win, values=('Male','Female'), font=('times new roman', 15))
        self.gender_entery.set("Select Gender")
        self.gender_entery.config(state='readonly')
        self.gender_entery.place(x=150 + inc_x, y=80 + inc, width=205)
        inc += 40
        self.contact_entery = Entry(self.student_win, font=('times new roman', 15))
        self.contact_entery.place(x=150 + inc_x, y=80 + inc)

        inc += 40
        self.dob_entery = DateEntry(self.student_win, font=('times new roman', 15), date_pattern='yyyy-mm-dd',width=18, state='readonly',fg='#F5F5F5',relief=GROOVE)
        self.dob_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.address_entry = Text(self.student_win, width=20, height=2, font=('times new roman', 15))

        self.address_entry.place(x=150 + inc_x, y=80 + inc)


        #**********************************

        self.submit_btn = Button(self.student_win, text="SUBMIT", bg="orange", font=("Nirmala UI", 12, 'bold'),
                                 fg='black',
                                 command=lambda: self.add_student_query(), cursor='hand2', bd=2,
                                 activebackground="white")
        self.submit_btn.place(x=230, y=350)

        self.upimag_student_button = Button(self.student_win, text='Upload Image', cursor='hand2',
                                            command=lambda: self.show_image(), bg='#F5F5F5', fg='black',
                                            font=('Nirmala UI', 12, 'bold'), bd=2, relief=RIDGE)
        self.upimag_student_button.place(x=400, y=80, width=170)


        self.id_label = Label(self.student_win, relief=GROOVE, bg='lightblue', bd=2)
        self.id_label.place(x=370, y=140, width=225, height=250)

        self.student_win.protocol("WM_DELETE_WINDOW", self.on_closing_student_win)
        self.student_win.mainloop()

    def on_closing_student_win(self):
        self.student_win.destroy()
        self.main_win_loop.deiconify()


    def add_student_query(self):

        if (self.name_entery.get() == '' or
                self.email_entery.get() == '' or
                self.dob_entery.get() == '' or
                self.gender_entery.get() == '' or
                self.gender_entery.get() == 'Select Gender' or
                self.contact_entery.get() == '' or
                self.open_file == '' or
                self.address_entry.get('1.0', END) == ''):
            messagebox.showwarning("Library Management System", "All fields are necessary.")
        elif(self.image_uploaded == False):
            messagebox.showwarning("Library Management System","Please upload image.")
        elif (self.check_email(self.email_entery.get())==0) :
            self.email_entery.delete(0,END)
            messagebox.showwarning("Library Managment System", "Email id is invalid.")

        else:
            self.is_email_sent = False
            os.remove(self.name_entery.get()+".png")
            self.generate_student_id()

            conn = psycopg2.connect(user="postgres",
                                        password="1234",
                                        host="localhost",
                                        port="5432",
                                        database="lms")

            cur = conn.cursor()
            cur.execute(f"select user_email from student where user_email='{self.email_entery.get()}'")
            self.row = cur.fetchone()
            if(self.row==None):
                self.send_student_id(self.email_entery.get())
                if (self.is_email_sent == True):

                    self.resize_img_new_temp.save("Temp1.png")
                    self.drawings = open("Temp1.png",'rb').read()
                    os.remove("Temp1.png")
                    self.SQL = "insert into student (user_email, user_name, user_gender, user_contact, user_dob, user_address, user_image) values(%s, %s, %s, %s, %s, %s, %s)"
                    self.data = (self.email_entery.get(), self.name_entery.get(), self.gender_entery.get(),self.contact_entery.get(), self.dob_entery.get(), self.address_entry.get(1.0, END), psycopg2.Binary(self.drawings))
                    cur.execute(self.SQL,self.data)
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Library Management System","Student added successfully.")

                    self.name_entery.delete(0, END)
                    self.email_entery.delete(0, END)
                    self.gender_entery.delete(0, END)
                    self.contact_entery.delete(0, END)
                    self.dob_entery.delete(0,END)
                    self.address_entry.delete("1.0", 'end-1c')
                    self.open_file=''
                    self.gender_entery.set("Select Gender")




                else:
                    self.email_entery.delete(0, END)
                    conn.commit()
                    conn.close()

            else:
                self.email_entery.delete(0, END)
                conn.commit()
                conn.close()
                messagebox.showerror("Library Management System", "Your email id already exists.")

    def show_image(self):

        if(self.name_entery.get()=='' or
           self.email_entery.get()==''or
           self.dob_entery.get()==''or
           self.gender_entery.get()==''or
           self.gender_entery.get()=='Select Gender'or
           self.contact_entery.get()==''or
           self.address_entry.get('1.0','end-1c')==''):

           messagebox.showwarning("Upload Image","First input the required fields and then upload image.")
        else:

            self.open_file = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select image', filetype=(
            ("jpg file", "*.jpg"), ("png file", "*.png")))


            self.generate_student_id()



    def generate_student_id(self):

        try:

            self.frame = Frame(self.student_win, relief=GROOVE, bg='lightblue', bd=2)
            self.frame.place(x=370, y=140, width=225, height=250)


            self.image_label = Label(self.frame, font=('times new roman', 20, 'bold'), fg='white', bg='lightblue',
                                     relief='flat')
            self.image_label.place(x=60, y=28)

            # loading image and resizing it

            self.igs = Image.open(self.open_file)
            self.resize_igs = self.igs.resize((70,70), Image.ANTIALIAS)

            self.mask1 = Image.new('L', (70, 70), 0)
            self.draw_mask1 = ImageDraw.Draw(self.mask1)
            self.draw_mask1.ellipse((0, 0) + (70, 70), fill=255)
            self.resize_igs.putalpha(self.mask1)

            self.new_igs = ImageTk.PhotoImage(self.resize_igs)
            self.image_label.configure(image=self.new_igs)

            self.ID_label = Label(self.frame, text='ID CARD', font=('times new roman', 12, 'bold'), fg='white',
                                  bg='lightblue', relief='flat')
            self.ID_label.place(x=0, y=0, width=200)

            self.y_pos = 100
            self.name_label = Label(self.frame,
                                 text='Name:- ' + self.name_entery.get(),
                                 font=('times new roman', 8, 'bold'), fg='white', bg='lightblue', relief='flat')
            self.name_label.place(x=5, y=self.y_pos)

            self.email_label = Label(self.frame, text='Email Id:-' + self.email_entery.get(),
                                 font=('times new roman', 8, 'bold'), fg='white', bg='lightblue', relief='flat')
            self.email_label.place(x=5, y=self.y_pos+20)

            self.contact_label = Label(self.frame, text='Contact :- ' + self.contact_entery.get(),
                                  font=('times new roman', 8, 'bold'), fg='white', bg='lightblue', relief='flat')
            self.contact_label.place(x=5, y=self.y_pos+40)

            self.dob_label = Label(self.frame, text='D-O-B:- ' + self.dob_entery.get(),
                                  font=('times new roman', 8, 'bold'), fg='white', bg='lightblue', relief='flat')
            self.dob_label.place(x=5, y=self.y_pos+60)

            self.gender_label = Label(self.frame, text='Gender:- ' + self.gender_entery.get(),
                                  font=('times new roman', 8, 'bold'), fg='white', bg='lightblue', relief='flat')
            self.gender_label.place(x=5, y=self.y_pos+80)

            self.AA_label = Label(self.frame, text='Address:- ' + self.address_entry.get(1.0,END),
                                  font=('times new roman', 8, 'bold'), fg='white', bg='lightblue', relief='flat')
            self.AA_label.place(x=5, y=self.y_pos+100)



            # ============== CREATING IMAGE FOR IDCARD===========================#

            self.idimage = Image.new(mode="RGB", size=(1000, 1550), color=(242, 242, 242))
            self.drawidimage = ImageDraw.Draw(self.idimage)

            (x, y) = (200, 30)
            self.idname = str("ID CARD")
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype(font="arial.ttf", size=140)
            self.drawidimage.text((x, y), self.idname, fill=self.color, font=self.font)

            (x, y) = (250, 230)
            self.im = Image.open(self.open_file)
            self.resize_img_new = self.im.resize((400, 400), Image.ANTIALIAS)
            self.resize_img_new_temp = self.resize_img_new



            self.mask = Image.new('L',(400,400),0)
            self.draw_mask=ImageDraw.Draw(self.mask)
            self.draw_mask.ellipse((0,0)+(400,400), fill=255)
            self.resize_img_new.putalpha(self.mask)
            self.idimage.paste(self.resize_img_new, (x, y), self.resize_img_new)




            (x, y) = (50, 660)
            self.idname = str("Name: " + self.name_entery.get())
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype("arial.ttf", size=50)
            self.drawidimage.text((x, y), self.idname, fill=self.color, font=self.font)

            (x, y) = (50, 790)
            self.idemail = str("Email: " + self.email_entery.get())
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype("arial.ttf", size=50)
            self.drawidimage.text((x, y), self.idemail, fill=self.color, font=self.font)

            (x, y) = (50, 910)
            self.idcontact = str("Contact: " + self.contact_entery.get())
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype("arial.ttf", size=50)
            self.drawidimage.text((x, y), self.idcontact, fill=self.color, font=self.font)

            (x, y) = (50, 1030)
            self.iddob = str("D.O.B: " + self.dob_entery.get())
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype("arial.ttf", size=50)
            self.drawidimage.text((x, y), self.iddob, fill=self.color, font=self.font)

            (x, y) = (50, 1150)
            self.idgender = str("Gender: " + self.gender_entery.get())
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype("arial.ttf", size=50)
            self.drawidimage.text((x, y), self.idgender, fill=self.color, font=self.font)

            (x, y) = (50, 1260)
            self.idaddress = str("Address: " + self.address_entry.get(1.0,END))
            self.color = 'rgb(0,0,0)'
            self.font = ImageFont.truetype("arial.ttf", size=50)
            self.drawidimage.text((x, y), self.idaddress, fill=self.color, font=self.font)


            self.idimage.save(self.name_entery.get()+".png", "PNG")

            self.image_uploaded = True
        except:
            messagebox.showinfo('Library Management System', 'Please Select image')


    def send_student_id(self, email_add):

        gdata = gdt.HostEmailDetails()
        email_address = gdata.host_email_id()
        email_password = gdata.host_email_password()
        send_to_address = email_add

        msg = MIMEMultipart()
        msg['Subject'] = "Registration Successful"
        msg['From'] = 'Library Management System'+'<'+email_address+'>'
        msg['To'] = send_to_address
        msg_ready = MIMEText('Registration successful')
        msg.attach(msg_ready)
        img = open(self.name_entery.get() + ".png", 'rb').read()
        img_ready = MIMEImage(img, 'png', name='Your ID Card')
        msg.attach(img_ready)
        try:
            context_data = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context_data, timeout=10) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
                messagebox.showinfo("Library Management System", "Your Id Card has been sent to your Email Id.")
            self.is_email_sent = True
        except Exception as e:
            messagebox.showerror("Library Management System",
                                 """Either your email id is invalid or you are not connected to internet.""")
            self.is_email_sent = False



    def check_email(self, email_id):

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.match(regex, email_id)):
            return 1
        else:
            return 0

