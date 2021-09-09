from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import *
from tkinter import filedialog
import os
from tkinter import messagebox
import psycopg2
import cv2
from pyzbar.pyzbar import decode
from isbntools.app import *
from datetime import datetime
import urllib.request
import random




class AddBook:

    image_uploaded1 = False

    def add_book_window(self, mainloop):
        # width and height of the window
        self.width = 600
        self.height = 400
        self.main_win_loop = mainloop

        book_win = Toplevel()
        self.book_win = book_win

        self.screen_width = int((self.book_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.book_win.winfo_screenheight()) / 6)

        self.book_win.geometry(f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}")
        self.book_win.title("Add Book")
        self.book_win.resizable(FALSE, FALSE)
        self.book_win.configure(bg="#fbedff")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/bg1.png"))
        self.top_label = Label(self.book_win, image=self.photo0, bg="#d0a1ff")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.input_details = ['ISBN Number', 'Book Title', 'Category', 'Author Name', 'Publisher', 'Date of Publiction', 'Quantity']

        inc = -40
        inc_x = 10
        for i in range(7):

            inc += 40

            self.lbldetails = Label(self.book_win, text=self.input_details[i], font=("Nirmala UI", 10, 'bold'),
                                      fg='black', bg="#fbedff")
            self.lbldetails.place(x=30 + inc_x, y=80 + inc)

            self.lbl = Label(self.book_win, text="*", font=("Nirmala UI", 10, 'bold'),
                             fg='red', bg="#fbedff")
            self.lbl.place(x=20 + inc_x, y=80 + inc)

        inc = 0

        self.isbn_entery = Entry(self.book_win, font=('times new roman', 15))
        self.isbn_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.title_entery = Entry(self.book_win, font=('times new roman', 15))
        self.title_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.cvalues = ("Arts & Music", "Biographies", "Business", "Comics", "Computers & Tech", "History", "Kids", "Medical", "Engeneering", "Others")
        self.category_entery = ttk.Combobox(self.book_win, values=self.cvalues, font=('times new roman', 15))
        self.category_entery.set("Select Category")
        self.category_entery.config(state='readonly')
        self.category_entery.place(x=150 + inc_x, y=80 + inc, width=205)
        inc += 40
        self.author_entery = Entry(self.book_win, font=('times new roman', 15))
        self.author_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.publisher_entery = Entry(self.book_win, font=('times new roman', 15))
        self.publisher_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.dop_entery = DateEntry(self.book_win, font=('times new roman', 15), date_pattern='yyyy-mm-dd',width=18, state='readonly',fg='#F5F5F5',relief=GROOVE)
        self.dop_entery.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.quantity_entery = Entry(self.book_win, font=('times new roman', 15))
        self.quantity_entery.place(x=150 + inc_x, y=80 + inc)

        #**********************************

        self.submit_btn = Button(self.book_win, text="SAVE", bg="orange", font=("Nirmala UI", 10, 'bold'),
                                 fg='black',
                                 command=lambda: self.add_book_query(), cursor='hand2', bd=2,
                                 activebackground="white")
        self.submit_btn.place(x=100, y=355, width=70)

        self.update_btn = Button(self.book_win, text="UPDATE", bg="orange", font=("Nirmala UI", 10, 'bold'),
                                 fg='black',
                                 command=lambda: self.update_book_query(), cursor='hand2', bd=2,
                                 activebackground="white")
        self.update_btn.place(x=10, y=355, width=70)

        self.search_btn = Button(self.book_win, text="SEARCH", bg="orange", font=("Nirmala UI", 10, 'bold'),
                                 fg='black',
                                 command=lambda: self.search_book_query(), cursor='hand2', bd=2,
                                 activebackground="white")
        self.search_btn.place(x=200, y=355, width=70)

        self.delete_btn = Button(self.book_win, text="DELETE", bg="orange", font=("Nirmala UI", 10, 'bold'),
                                 fg='black',
                                 command=lambda: self.delete_book_query(), cursor='hand2', bd=2,
                                 activebackground="white")
        self.delete_btn.place(x=290, y=355, width=70)

        self.clear_btn = Button(self.book_win, text="CLEAR", bg="orange", font=("Nirmala UI", 10, 'bold'),
                                 fg='black',
                                 command=lambda: self.clear(), cursor='hand2', bd=2,
                                 activebackground="white")
        self.clear_btn.place(x=380, y=355, width=70)

        self.scan_button = Button(self.book_win, text='Scan QR Code', cursor='hand2',
                                    command=lambda: self.scan_QR_Code(), bg='#F5F5F5', fg='black',
                                    font=('Nirmala UI', 9, 'bold'), bd=2, relief=RIDGE)
        self.scan_button.place(x=420, y=80, width=120)

        self.getdetails_button = Button(self.book_win, text='Online \n Search', cursor='hand2',
                                  command=lambda: self.searchbook(), bg='#F5F5F5', fg='black',
                                  font=('Nirmala UI', 6, 'bold'), bd=2)
        self.getdetails_button.place(x=366, y=80, height=25)

        self.radio_var = IntVar()

        self.image_radio = Radiobutton(self.book_win, text = "Image", variable = self.radio_var, value=1,font=('Nirmala UI', 9, 'bold'),bg='#fbedff', fg='black')
        self.image_radio.place(x=380, y=110)
        self.image_radio.select()

        self.image_label = Label(self.book_win, relief=GROOVE, bg='lightblue', bd=2)
        self.image_label.place(x=470, y=270, width=120, height=120)

        self.scan_label = Label(self.book_win, relief=GROOVE, bg='lightgreen', bd=2)
        self.scan_label.place(x=380, y=135, width=215, height=130)

        self.camera_radio = Radiobutton(self.book_win, text="Camera", variable = self.radio_var, value=2, font=('Nirmala UI', 9, 'bold'),
                                       bg='#fbedff', fg='black')
        self.camera_radio.place(x=480, y=110)

        self.upimag_button = Button(self.book_win, text='Upload Image', cursor='hand2',
                                            command=lambda: self.upload_image(), bg='#F5F5F5', fg='black',
                                            font=('Nirmala UI', 9, 'bold'), bd=2, relief=RIDGE)
        self.upimag_button.place(x=380, y=320, width=85)


        self.delete_btn.configure(state='disabled')
        self.update_btn.configure(state='disabled')

        self.book_win.protocol("WM_DELETE_WINDOW", self.on_closing_book_win)

        self.book_win.mainloop()

    def on_closing_book_win(self):
        self.book_win.destroy()
        self.main_win_loop.deiconify()


    def update_book_query(self):
        if (self.isbn_entery.get() == '' or
                self.title_entery.get() == '' or
                self.dop_entery.get() == '' or
                self.category_entery.get() == '' or
                self.category_entery.get() == 'Select Category' or
                self.author_entery.get() == '' or
                self.quantity_entery.get() == '' or
                self.publisher_entery.get() == ''):
            messagebox.showwarning("Library Management System", "All fields are necessary.")
        elif self.image_uploaded1 == False:
            messagebox.showwarning("Library Management System","Please upload image.")
        else:

            conn = psycopg2.connect(user="postgres",
                                        password="1234",
                                        host="localhost",
                                        port="5432",
                                        database="lms")

            cur = conn.cursor()
            cur.execute(f"select book_isbn from book where book_isbn='{self.isbn_entery.get()}'")
            self.row1 = cur.fetchone()
            if(self.row1==None):
                messagebox.showerror("Library Management System", "Book not exists in the inventory.")
                self.clear()
                conn.close()
            else:
                self.resize_imgbar1.save("Temp2.png")
                self.drawings1 = open("Temp2.png",'rb').read()
                os.remove("Temp2.png")
                SQL = "update book set book_title=%s, book_category=%s, book_author=%s, book_publisher=%s, book_dop=%s, book_quantity=%s, book_image=%s where book_isbn=%s"
                data = (self.title_entery.get(), self.category_entery.get(),self.author_entery.get(), self.publisher_entery.get(), self.dop_entery.get(), self.quantity_entery.get(), psycopg2.Binary(self.drawings1), self.isbn_entery.get())
                cur.execute(SQL, data)
                conn.commit()
                conn.close()

                messagebox.showinfo("Library Management System","Book updated successfully.")

                self.clear()








    def delete_book_query(self):
        if self.isbn_entery.get() !='':
            # connecting to postgres database
            connection = psycopg2.connect(user="postgres",
                                      password="1234",
                                      host="localhost",
                                      port="5432",
                                      database="lms")
            cursor = connection.cursor()

            cursor.execute(f"delete from book where book_isbn = '{self.isbn_entery.get()}'")
            connection.commit()
            connection.close()
            messagebox.showinfo("Library Management System","Book removed successfully.")
            self.clear()
        else:
            messagebox.showerror("Error","Please enter isbn number.")

    def search_book_query(self):

        if self.isbn_entery.get() == '':
            messagebox.showerror("Error", "Please input isbn number.")

        else:

            conn = psycopg2.connect(user="postgres",
                                        password="1234",
                                        host="localhost",
                                        port="5432",
                                        database="lms")

            cur = conn.cursor()
            cur.execute(f"select * from book where book_isbn='{self.isbn_entery.get()}'")
            self.row1 = cur.fetchone()

            if(self.row1):
                self.clear()
                self.isbn_entery.insert(0, self.row1[0])
                self.title_entery.insert(0, self.row1[1])
                self.category_entery.set(self.row1[2])
                self.author_entery.insert(0, self.row1[3])
                self.publisher_entery.insert(0, self.row1[4])
                self.dop_entery.set_date(self.row1[5])
                self.quantity_entery.insert(0, self.row1[6])

                # writing binary data to file

                self.picimg = open("Test.png", 'wb')
                self.picimg.write((self.row1[7]))
                self.picimg.close()
                self.img_picimg = Image.open("Test.png")

                self.resize_image = self.img_picimg.resize((120, 120), Image.ANTIALIAS)
                self.pic = ImageTk.PhotoImage(self.resize_image)

                self.image_label.config(image=self.pic)
                self.image_uploaded1 = True
                self.resize_imgbar1 = self.resize_image
                os.remove("Test.png")
                self.delete_btn.configure(state='normal')
                self.update_btn.configure(state='normal')

                conn.commit()
                conn.close()
            else:
                messagebox.showerror("Library management system", "No record found.")


    def searchbook(self):
        if self.isbn_entery.get()!='':
            try:
                bookinfo = meta (self.isbn_entery.get())
                self.title_entery.insert(0,bookinfo['Title'])
                self.author_entery.insert(0, bookinfo['Authors'])
                self.publisher_entery.insert(0, bookinfo['Publisher'])
                self.byear =datetime.strptime(f"{bookinfo['Year']}-01-01", '%Y-%m-%d')
                self.dop_entery.set_date(self.byear)

                # Get cover image
                self.choose = random.randrange(1,5)
                if self.choose == 1:
                    urllib.request.urlretrieve("https://1.bp.blogspot.com/-s_55k00VPNk/YRIm2LNOS3I/AAAAAAAABGs/CHSFn_xWpJgNH3pKRYqBFZBp3lfAaQBjQCLcBGAsYHQ/s424/BOOK%2BCOVER.jpg", "cover.jpg")
                elif self.choose == 2:
                    urllib.request.urlretrieve(
                        "https://1.bp.blogspot.com/-h1iF0navcaw/YRIs4VlQIkI/AAAAAAAABG0/JgE7BR8DW0IQCrBeC3rR_8PIkR1lAUS-ACLcBGAsYHQ/s423/C1.jpg",
                        "cover.jpg")
                elif self.choose == 3:
                    urllib.request.urlretrieve(
                        "https://1.bp.blogspot.com/-ya_z-y2zWwg/YRIv5N_CCDI/AAAAAAAABG8/GBoDP22i1iEdi-uSEsmoTKOPCK8kyF4vgCLcBGAsYHQ/s425/C2.jpg",
                        "cover.jpg")
                else:
                    urllib.request.urlretrieve(
                        "https://1.bp.blogspot.com/-8JC4lH-u5IE/YRIw37VBJcI/AAAAAAAABHE/HVLo2V0uUbA1ciU_9kyejcgELhqvNqoSACLcBGAsYHQ/s426/C3.jpg",
                        "cover.jpg")
                self.file_add = "cover.jpg"
                self.imgbar1 = Image.open(self.file_add)
                self.resize_imgbar1 = self.imgbar1.resize((120, 120), Image.ANTIALIAS)
                self.new_img1 = ImageTk.PhotoImage(self.resize_imgbar1)
                self.image_label.configure(image=self.new_img1)
                self.image_uploaded1 = True
                os.remove("cover.jpg")

            except:
                messagebox.showerror("Error", "No result found.")


    def upload_image(self):
        self.file_add = self.show_image()
        if self.file_add:
            self.imgbar1 = Image.open(self.file_add)
            self.resize_imgbar1 = self.imgbar1.resize((120, 120), Image.ANTIALIAS)
            self.new_img1 = ImageTk.PhotoImage(self.resize_imgbar1)
            self.image_label.configure(image=self.new_img1)
            self.image_uploaded1 = True
        else:
            messagebox.showerror("Error","Please select image.")

    def scan_QR_Code(self):
        if self.radio_var.get() == 1:
            #image
            self.file_loc = self.show_image()
            if self.file_loc:
                self.imgbar = Image.open(self.file_loc)
                self.testimg = self.imgbar
                self.resize_imgbar = self.imgbar.resize((215,130), Image.ANTIALIAS)
                self.new_img = ImageTk.PhotoImage(self.resize_imgbar)

                # read barcode or QR code
                barcode = decode(self.testimg)
                if not barcode:
                    messagebox.showwarning("Error","This is not a valid barcode/QR code image.")
                else:
                    self.scan_label.configure(image=self.new_img)
                    for code in barcode:
                        self.isbn_entery.delete(0, END)
                        self.isbn_entery.insert(0, code.data.decode('utf-8'))

        else:
            #Camera

            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,215)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,130)
            if self.capture.isOpened():
                self.show_frames()
            else:
                messagebox.showerror("Library Management System", "Unable to open camera.")


    def show_frames(self):

        if self.radio_var.get() == 1:
            self.capture.release()
            cv2.destroyAllWindows()

        else:
            success, frame = self.capture.read()
            #frame = cv2.flip(frame,0)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgresize = img.resize((215, 130), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=imgresize)
            self.scan_label.imgtk = imgtk
            self.scan_label.configure(image=imgtk)
            # read barcode or QR code
            bar_code = decode(frame)
            if not bar_code:
                pass
            else:
                for c in bar_code:
                    self.isbn_entery.delete(0,END)
                    self.isbn_entery.insert(0, c.data.decode('utf-8'))

            self.scan_label.after(1, self.show_frames)

    def clear(self):
        self.isbn_entery.delete(0, END)
        self.title_entery.delete(0, END)
        self.category_entery.delete(0, END)
        self.author_entery.delete(0, END)
        self.dop_entery.delete(0, END)
        self.publisher_entery.delete(0, END)
        self.quantity_entery.delete(0, END)
        self.file_add = ''
        self.image_uploaded1 = False
        self.category_entery.set("Select Category")
        self.scan_label.configure(image='')
        self.image_label.configure(image='')
        self.delete_btn.configure(state='disabled')
        self.update_btn.configure(state='disabled')

    def add_book_query(self):

        if (self.isbn_entery.get() == '' or
                self.title_entery.get() == '' or
                self.dop_entery.get() == '' or
                self.category_entery.get() == '' or
                self.category_entery.get() == 'Select Category' or
                self.author_entery.get() == '' or
                self.quantity_entery.get() == '' or
                self.publisher_entery.get() == ''):
            messagebox.showwarning("Library Management System", "All fields are necessary.")
        elif self.image_uploaded1 == False:
            messagebox.showwarning("Library Management System","Please upload image.")
        else:

            conn = psycopg2.connect(user="postgres",
                                        password="1234",
                                        host="localhost",
                                        port="5432",
                                        database="lms")

            cur = conn.cursor()
            cur.execute(f"select book_isbn from book where book_isbn='{self.isbn_entery.get()}'")
            self.row1 = cur.fetchone()
            if(self.row1==None):

                self.resize_imgbar1.save("Temp1.png")
                self.drawings1 = open("Temp1.png",'rb').read()
                os.remove("Temp1.png")
                SQL = "insert into book (book_isbn, book_title, book_category, book_author, book_publisher, book_dop, book_quantity, book_image) values(%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (self.isbn_entery.get(), self.title_entery.get(), self.category_entery.get(),self.author_entery.get(), self.publisher_entery.get(), self.dop_entery.get(), self.quantity_entery.get(), psycopg2.Binary(self.drawings1))
                cur.execute(SQL, data)
                conn.commit()
                conn.close()

                messagebox.showinfo("Library Management System","Book added successfully.")

                self.clear()

            else:

                conn.commit()
                conn.close()
                messagebox.showerror("Library Management System", "Book already exists in the inventory.")
                self.clear()

    def show_image(self):

        img_address = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select image', filetype=(
            ("jpg file", "*.jpg"), ("png file", "*.png")))

        return img_address


