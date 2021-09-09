from tkinter import *
from tkinter.tix import *
from PIL import Image, ImageTk
from datetime import date

import add_book as ab
import book_details as bd
import add_student as ast
import student_details as sd
import return_book as rb
import issue_book as ib
import login_window as lw


class MainWindow:
    def create_main_window(self, username):
        main_win = Tk()
        self.main_win = main_win

        self.width = 600
        self.height = 400

        self.screen_width = int(self.main_win.winfo_screenwidth()/4)
        self.screen_height = int(self.main_win.winfo_screenheight()/6)

        self.main_win.geometry(f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}")
        self.main_win.title("Main Window")
        self.main_win.resizable(FALSE, FALSE)
        self.main_win.configure(bg="white")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/bg1.png"))
        self.img_label = Label(self.main_win, bg="gold")
        self.img_label.place(x=0, y=0, width=600, height=65)
        self.img_label.configure(image=self.photo0, anchor='w')

        self.resize_width=110
        self.resize_height=85
        # Load images
        self.pic1 = ImageTk.PhotoImage(Image.open("images/add_studentA.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))
        self.pic2 = ImageTk.PhotoImage(Image.open("images/show_student.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))
        self.pic3 = ImageTk.PhotoImage(Image.open("images/add_book.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))
        self.pic4 = ImageTk.PhotoImage(Image.open("images/show_book.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))
        self.pic5 = ImageTk.PhotoImage(Image.open("images/issue_book.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))
        self.pic6 = ImageTk.PhotoImage(Image.open("images/return_book.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))
        self.pic7 = ImageTk.PhotoImage(Image.open("images/logout.png").resize((self.resize_width,self.resize_height),Image.ANTIALIAS))


        # show user name and date
        self.lbl_name = Label(self.main_win, bg="gold", fg="green",font=("Nirmala UI", 10, 'bold'))
        self.lbl_name.place(x=400,y=10)

        self.lbl_date = Label(self.main_win, bg="gold", fg="green",font=("Nirmala UI", 10, 'bold'))
        self.lbl_date.place(x=400,y=30)


        self.lbl_name.configure(text="Librarian  : %s" % username)
        self.lbl_date.configure(text= "Date        : %s"%(date.today().strftime("%d/%m/%Y")))

        #******** ********


        self.add_student_btn = Button(self.main_win, image=self.pic1, bg="white",bd=0, command=lambda: self.add_student_menu())
        self.add_student_btn.place(x=40+40,y=100)

        self.show_student_btn = Button(self.main_win,image=self.pic2, bg="white", bd=0, command=lambda: self.show_student_menu())
        self.show_student_btn.place(x=410-40, y=100)

        # ******** ********


        self.add_book_btn = Button(self.main_win,image=self.pic3,bg="white",
                                      bd=0, command=lambda: self.add_book_menu())
        self.add_book_btn.place(x=40, y=200)


        self.show_book_btn = Button(self.main_win,image=self.pic4,
                                       bg="white",
                                       bd=0, command=lambda: self.show_book_menu())
        self.show_book_btn.place(x=410, y=200)

        # ******** ********


        self.issue_book_btn = Button(self.main_win,image=self.pic5, bg="white",
                                   fg="white", bd=0, command=lambda: self.issue_menu())
        self.issue_book_btn.place(x=40+40, y=300)

        self.return_book_btn = Button(self.main_win,image=self.pic6,
                                   bg="white",
                                   bd=0, command=lambda: self.return_menu())
        self.return_book_btn.place(x=410-40, y=300)

        self.logout_btn = Button(self.main_win,image=self.pic7,
                                    bg="white",
                                    bd=0, command=lambda: self.login_menu())
        self.logout_btn.place(x=225, y=200)

        #tooltip

        tip=Balloon(self.main_win)
        # Bind the tooltip with button
        tip.bind_widget(self.add_student_btn, balloonmsg="Add New Student")
        tip.bind_widget(self.show_student_btn, balloonmsg="Show Student Details")
        tip.bind_widget(self.add_book_btn, balloonmsg="Add New Book")
        tip.bind_widget(self.show_book_btn, balloonmsg="Show Book Details")
        tip.bind_widget(self.issue_book_btn, balloonmsg="Issue Book")
        tip.bind_widget(self.return_book_btn, balloonmsg="Return Book")
        tip.bind_widget(self.logout_btn, balloonmsg="Logout")

        self.main_win.mainloop()

    def add_book_menu(self):
        self.main_win.withdraw()
        book_obj = ab.AddBook()
        book_obj.add_book_window(self.main_win)

    def show_book_menu(self):
        self.main_win.withdraw()
        show_book_obj = bd.bookDeailsWindow()
        show_book_obj.book_details_window(self.main_win)

    def add_student_menu(self):
        self.main_win.withdraw()
        student_obj = ast.AddStudent()
        student_obj.add_student_window(self.main_win)

    def show_student_menu(self):
        self.main_win.withdraw()
        show_student_obj = sd.studentDeailsWindow()
        show_student_obj.create_window(self.main_win)

    def issue_menu(self):
        self.main_win.withdraw()
        issue_obj = ib.IssueBook()
        issue_obj.issue_book_window(self.main_win)

    def return_menu(self):
        self.main_win.withdraw()
        return_obj = rb.ReturnBook()
        return_obj.return_book_window(self.main_win)

    def login_menu(self):
        self.main_win.destroy()
        login_obj = lw.LoginWindow()
        login_obj.create_login_window()