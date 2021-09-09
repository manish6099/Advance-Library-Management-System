from tkinter import *
from tkinter.ttk import Progressbar, Style
from PIL import Image, ImageTk
import time


class SplashScreen:

    def create_splash_window(self):

        # width and height of the window
        self.width = 600
        self.height = 400

        splash_win = Tk()
        self.splash_win = splash_win

        self.screen_width = int((self.splash_win.winfo_screenwidth())/4)
        self.screen_height = int((self.splash_win.winfo_screenheight())/6)

        self.splash_win.geometry(f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}")
        self.splash_win.overrideredirect(1)

        # loading image and resizing it
        self.img = Image.open("images/splash_screen.jpg")
        self.resized_image = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resized_image)

        # creating canvas
        self.canvas = Canvas(self.splash_win)
        self.canvas.pack(fill=BOTH, expand=1)


        # Style
        self.style = Style(self.canvas)
        self.style.layout("LabeledProgressbar", [('LabeledProgressbar.trough',
                                                 {'children': [('LabeledProgressbar.pbar', {'side':'left',
                                                   'sticky': 'ns'}),("LabeledProgressbar.label",  # label inside the bar
                                                    {"sticky": ""})], 'sticky': 'nswe'})])

        info = """\t   This  product  is   licensed  to:  Manish  Kumar
                   Website: https://justdocodings.blogspot.com
                   Copyright   ©   2021 :  All   rights  reserved"""

        # displaying image in canvas
        self.canvas.create_image(0,0,anchor='nw', image=self.new_image)
        self.canvas.create_text(100,self.height-30,text=info, font=("Nirmala UI", "8"), fill="#006600")

        # creating progress bar
        self.progress = Progressbar(self.canvas, style="LabeledProgressbar", orient=HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(side=BOTTOM, padx = 30, pady=100)

        # change the text of the progressbar
        self.style.configure("LabeledProgressbar", text="0 %")
        self.style.configure("LabeledProgressbar", background="#62f1b4", foreground="#c55f52")




        # update progressbar

        def update():
            for i in range(self.progress['maximum']+1):
                self.style.configure("LabeledProgressbar", text="{0} %".format(i))
                time.sleep(0.023)
                self.progress['value'] = i
                self.canvas.update()
            time.sleep(1)
            self.splash_win.destroy()

        self.progress.after(1, update)

        self.splash_win.mainloop()
