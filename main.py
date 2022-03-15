from tkinter import *
from tkinter import font
from tkinter import ttk
from turtle import color

from matplotlib.pyplot import fill, text
from numpy import pad

class App():
    def __init__(self):
        self.root = Tk()

        """ -------- GENERAL SETTINGS -------- """
        
        # Window size
        self.root.geometry("1280x792")
        self.root.wm_attributes('-transparentcolor', 'black')
        # Window size can't be changed
        self.root.resizable(0,0)
        self.root.title("SM - Home")
        self.font = font.Font(weight='bold')
        
        # Menu bar top
        menubar = Menu(self.root)
        helpmenu = Menu(menubar, tearoff=False)

        menubar.add_cascade(label="Home", command=None)
        menubar.add_cascade(label="Real time", command=None)
        menubar.add_cascade(label="Custom analysis", command=None)
        menubar.add_cascade(label="Help", menu=helpmenu)

        helpmenu.add_command(label="Settings")
        helpmenu.add_command(label="Version")
        helpmenu.add_separator()
        helpmenu.add_command(label="Exit", command=self.root.quit)

        """ -------- FRAMES SETTINGS -------- """

        # Home frames
        white_frame = Frame(self.root, bg="white", height=792, width=640)  # this is the background
        gray_frame = Frame(self.root, bg="#949494", height=792, width=640)  # this is the background
        
        light_gray_frame_up = Frame(self.root, bg="#E4E4E4", height=358, width=607)
        light_gray_frame_down = Frame(self.root, bg="#E4E4E4", height=358, width=607)

        white_frame.pack(fill="both", expand=True)
        gray_frame.place(x="0",y="0")
        light_gray_frame_up.place(x="653",y="24")
        light_gray_frame_down.place(x="653",y="412")
        self.root.config(menu=menubar)

        """ -------- LEFT FRAME -------- """
        
        # Home text left
        home_title = Label(self.root, text="Welcome to Social Media Meter", bg="#949494", fg="white", font=('Helvetica 18 bold'))
        label_title1 = Label(self.root, text="It starts sentiment and aggressiveness analysis with BERT, trained on\n ~200k tweets and properly tuned. These models are suitable for English\n and Spanish.\n\n\nMore information on datasets and sources used can be found in the help\nsection.\n\n\n\nEnjoy!", bg="#949494", fg="white", font=('Helvetica 13'), justify=LEFT)
        home_title.place(x="135", y="57")
        label_title1.place(x="25", y="130")

        # Home text left    

        # Hyperlinks social media TODO

        #twitter_icon = PhotoImage(file="icons/twitter_logo.png")
        #twitter_icon.subsample(32)
        #image_link = Label(self.root, image=twitter_icon, cursor="left_ptr", bg="#949494")
        #image_link.place(x="453", y="530")
        #image_link.bind("<1>",)
        #self.root.window_create("insert", window=image_link)

        """ -------- RIGHT-UPPER FRAME SETTINGS -------- """

        label_quick_text = Label(self.root, text="Quick text", bg="#E4E4E4", fg="black", font=('SegoeUI 9'), justify=LEFT)
        label_quick_text.place(x="655", y="25")

        # Frame inputs
        phrase = ttk.Entry(self.root, font = ('SegoeUI', 9))
        phrase.place(x="675", y="65", width=180, height=20)
        phrase.insert(0, "Enter any Text ...")
        # Frame buttons
        
        """ -------- RIGHT-BOTTOM FRAME SETTINGS -------- """
        # Frame label
        label_csv_analysis = Label(self.root, text="CSV analysis", bg="#E4E4E4", fg="black", font=('SegoeUI 9'), justify=LEFT)
        label_csv_analysis.place(x="655", y="415")


        #label_title1.config(width=30, height=20)
        
        self.root.mainloop()
if __name__ == '__main__':
    app = App()


    