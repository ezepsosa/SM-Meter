from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
from turtle import bgcolor
from click import command
from tkcalendar import DateEntry

def new_window(root):
    global win2
    try:
        if win2.state() == "normal": win2.focus()
    except NameError as e:
        print(e)
        win2 = Toplevel(root)



class App(Frame):
    def uploadAction(self, textDirectory):
        textDirectory.set(filedialog.askopenfilename())

    def showHideFrame(self, toggle):
            if toggle[0].place_info():
                for element in toggle:
                    element.place_forget()
            else:
                toggle[4].place(x='976',y='38')
                toggle[5].place(x='986', y='66')
                toggle[6].place(x='1022', y='119')
                toggle[1].place(x='1095', y='51')
                toggle[0].place(x='1095', y='74')
                toggle[2].place(x='1115', y='106')
                toggle[3].place(x='1115', y='131')

    def helpMenu(self, home):
            self.settings = Toplevel(home, width=372, height=590)
            self.settings.grab_set()
            self.settings.resizable(0,0)
            
            # Create tab panel.
            self.notebook = ttk.Notebook(self.settings, width=372, height=590)
            
            # Create the content tabs.
            self.general = None
            self.api = None
            self.about = None
            
            
            # Añadirlas al panel con su respectivo texto.
            self.notebook.add(self.home, text='Home', padding=20)
            self.notebook.add(self.realTime, text='Real time', padding=20)
            self.notebook.add(self.customAnalysis, text='Custom analysis', padding=20)
            self.notebook.pack()
            self.settings.pack()

    def home(self):

        

        # Home frames
        global explore_button_image
        global advanced_button_image
        global compute_button_image
        global settings_button_image
        

        self.home = ttk.Frame(self, height=1280, width=792)
        ''' -------- FRAMES SETTINGS -------- '''
        # Home frames
        white_frame = Frame(self.home, bg='white', height=792, width=640)  # this is the background
        gray_frame = Frame(self.home, bg='#949494', height=792, width=640)  # this is the background
        
        light_gray_frame_up = Frame(self.home, bg='#E4E4E4', height=355, width=700)
        light_gray_frame_down = Frame(self.home, bg='#E4E4E4', height=375, width=700)

        white_frame.pack(fill='both', expand=True)
        gray_frame.place(x='0',y='0')
        light_gray_frame_up.place(x='653',y='0')
        light_gray_frame_down.place(x='653',y='365')

        ''' -------- LEFT FRAME -------- '''
        
        # Home text left
        home_title = Label(self.home, text='Welcome to Social Media Meter', bg='#949494', fg='white', font=('Helvetica 18 bold'))
        label_title1 = Label(self.home, text='It starts sentiment and aggressiveness analysis with BERT, trained on\n ~200k tweets and properly tuned. These models are suitable for English\n and Spanish.\n\n\nMore information on datasets and sources used can be found in the help\nsection.\n\n\n\nEnjoy!', bg='#949494', fg='white', font=('Helvetica 13'), justify=LEFT)
        home_title.place(x='135', y='57')
        label_title1.place(x='25', y='130')

        # Home text left    

        # Hyperlinks social media TODO

        # Frame Buttons
        settings_button_image = PhotoImage(file=r'icons/settings_button.png')
        settingsButton = Button(self.home, image=settings_button_image, command =lambda: self.helpMenu(self.home), border=0, bg='#949494', activebackground='#949494')
        settingsButton.place(x='20', y='680')

        ''' -------- RIGHT-UPPER FRAME SETTINGS -------- '''

        Label(self.home, text='Quick text', bg='#E4E4E4', fg='black', font=('SegoeUI 9'), justify=LEFT).place(x='655', y='1')
        
        # Frame radio-check buttons
        language_UF = IntVar()
        Radiobutton(self.home,text='English', padx = 20,variable=language_UF,value=1, bg='#E4E4E4', activebackground='#E4E4E4').place(x='653', y='26')
        Radiobutton(self.home,text='Spanish', padx = 20,variable=language_UF,value=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='653', y='46')

        

        # Frame inputs
        phrase = ttk.Entry(self.home, font = ('SegoeUI', 9))
        phrase.place(x='675', y='74', width=180, height=20)
        phrase.insert(0, 'Enter any Text ...')
        
        # Frame buttons
        #TODO
        advanced_button_image = PhotoImage(file=r'icons/advanced_button.png')
        
        Button(self.home, image=advanced_button_image, command = lambda: self.showHideFrame(self.home.toggle), border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='865', y='68')
        compute_button_image = PhotoImage(file=r'icons/compute_button.png')
        Button(self.home, image=compute_button_image, command = None, border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='690', y='98')
        
        #TODO
        ''' -------- RIGHT-BOTTOM FRAME SETTINGS -------- '''
        # Frame label
        Label(self.home, text='CSV analysis', bg='#E4E4E4', fg='black', font=('SegoeUI 9'), justify=LEFT).place(x='655', y='370')

        # Frame buttons
        explore_button_image = PhotoImage(file=r'icons/explore_button.png')
        Button(self.home, image=compute_button_image, command = None, border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='690', y='467')
        Button(self.home, image=explore_button_image, command=lambda: self.uploadAction(textDirectory),border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='865', y='438')
        
        # Frame radio-check buttons
        language_BF = IntVar()
        Radiobutton(self.home,text='English', padx = 20,variable=language_BF,value=1, bg='#E4E4E4', activebackground='#E4E4E4').place(x='653', y='393')
        Radiobutton(self.home,text='Spanish', padx = 20,variable=language_BF,value=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='653', y='413')
        
        # Frame inputs
        textDirectory = StringVar()
        directory = ttk.Entry(self.home,textvariable=textDirectory, font = ('SegoeUI', 9))
        directory.place(x='675', y='443', width=180, height=20)
        
        ''' -------- FRAMES SETTINGS -------- '''
        # Home frames
        light_gray_frame = Frame(self.home, bg='#F9F9F9', height=134, width=242)  # this is the background
        

        # Frame label
        social_media_mode = Label(self.home, text='Social media mode:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT)
        analysis_type = Label(self.home, text='Analysis type:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT)

        # Frame radio-check buttons
        socialM_SF = IntVar()
        rb_tw_frameS = Radiobutton(self.home,text='Twitter', padx = 20,variable=socialM_SF,value=1, bg='#F9F9F9', activebackground='#F9F9F9')
        rb_re_frameS = Radiobutton(self.home,text='Reddit', padx = 20,variable=socialM_SF,value=0, bg='#F9F9F9', activebackground='#F9F9F9')

        # Frame check buttons
        sentimentVarSF = IntVar()
        aggressiveVarSF = IntVar()
        sfCB = Checkbutton(self.home, text = 'Sentiment', variable = sentimentVarSF, bg='#F9F9F9', activebackground='#F9F9F9', onvalue = 1, offvalue = 0)
        afCB = Checkbutton(self.home, text = 'Aggressive', variable = aggressiveVarSF, bg='#F9F9F9', activebackground='#F9F9F9', onvalue = 1, offvalue = 0)
        self.home.toggle = [rb_re_frameS, rb_tw_frameS, sfCB, afCB, light_gray_frame, social_media_mode, analysis_type]  
        return self.home
        
    def realTime(self):
        self.realTime = Frame(self, height=1280, width=792, bg="white")
        global start_rt_button_image
        ''' -------- TABLE SETTINGS -------- '''
        
        # Label Frame Settings

        lb = LabelFrame(self.realTime, text='Analysis', bg='white', fg='black', width=1215, height=370, font=('SegoeUI 9'))
        lb.place(x='10', y='30')

         #Scroll settings 

        analysis_scroll = Scrollbar(lb)
        analysis_scroll.pack(side=RIGHT, fill=Y)

        #Table settings

        analysis = ttk.Treeview(lb,yscrollcommand=analysis_scroll.set, xscrollcommand =analysis_scroll.set)
        analysis.pack()

        analysis['columns'] = ('text', 'user_id', 'date', 'country', 'sentiment','aggressive')

        analysis.column("#0", width=0,  stretch=NO)
        analysis.column("text",anchor=CENTER,width=450)
        analysis.column("user_id",anchor=CENTER,width=115)
        analysis.column("date",anchor=CENTER,width=165)
        analysis.column("country",anchor=CENTER,width=120)
        analysis.column("sentiment",anchor=CENTER,width=175)
        analysis.column("aggressive",anchor=CENTER,width=175)

        analysis.heading("#0",text="",anchor=CENTER)
        analysis.heading("text",text="Text",anchor=CENTER)
        analysis.heading("user_id",text="User",anchor=CENTER)
        analysis.heading("date",text="Date",anchor=CENTER)
        analysis.heading("country",text="Country",anchor=CENTER)
        analysis.heading("sentiment",text="Sentiment",anchor=CENTER)
        analysis.heading("aggressive",text="Aggressive",anchor=CENTER)
        
        #analysis.insert(parent='',index='end',iid=0,text='',
        #values=('1','Ninja','101','Oklahoma', 'Moore'))

       
        analysis_scroll.config(command=analysis.yview)
        analysis_scroll.config(command=analysis.xview)

        # Buttons
        start_rt_button_image = PhotoImage(file=r'icons/start_button.png')
        Button(self.realTime, image=start_rt_button_image, command = None, border=0, bg='white', activebackground='white').place(x='1060', y='5')
        Button(self.realTime, image=advanced_button_image, command = None, border=0, bg='white', activebackground='white').place(x='1140', y='5')
       



        return self.realTime
    
    def customAnalysis(self):
        self.customAnalysis = Frame(self, height=1280, width=792, bg="white")
        global start_ca_button_image
        global choose_date
        ''' -------- TABLE SETTINGS -------- '''
        
        # Label Frame Settings

        lb = LabelFrame(self.customAnalysis, text='Analysis', bg='white', fg='black', width=1215, height=370, font=('SegoeUI 9'))
        lb.place(x='10', y='30')

         #Scroll settings 

        analysis_scroll = Scrollbar(lb)
        analysis_scroll.pack(side=RIGHT, fill=Y)

        #Table settings

        analysis = ttk.Treeview(lb,yscrollcommand=analysis_scroll.set, xscrollcommand =analysis_scroll.set)
        analysis.pack()

        analysis['columns'] = ('text', 'user_id', 'date', 'country', 'sentiment','aggressive')

        analysis.column("#0", width=0,  stretch=NO)
        analysis.column("text",anchor=CENTER,width=450)
        analysis.column("user_id",anchor=CENTER,width=115)
        analysis.column("date",anchor=CENTER,width=165)
        analysis.column("country",anchor=CENTER,width=120)
        analysis.column("sentiment",anchor=CENTER,width=175)
        analysis.column("aggressive",anchor=CENTER,width=175)

        analysis.heading("#0",text="",anchor=CENTER)
        analysis.heading("text",text="Text",anchor=CENTER)
        analysis.heading("user_id",text="User",anchor=CENTER)
        analysis.heading("date",text="Date",anchor=CENTER)
        analysis.heading("country",text="Country",anchor=CENTER)
        analysis.heading("sentiment",text="Sentiment",anchor=CENTER)
        analysis.heading("aggressive",text="Aggressive",anchor=CENTER)
        
        #analysis.insert(parent='',index='end',iid=0,text='',
        #values=('1','Ninja','101','Oklahoma', 'Moore'))

       
        analysis_scroll.config(command=analysis.yview)
        analysis_scroll.config(command=analysis.xview)

        # Buttons
        start_ca_button_image = PhotoImage(file=r'icons/start_button.png')
        Button(self.customAnalysis, image=start_ca_button_image, command = None, border=0, bg='white', activebackground='white').place(x='1060', y='5')
        Button(self.customAnalysis, image=advanced_button_image, command = None, border=0, bg='white', activebackground='white').place(x='1145', y='5')
    
        #Entry
        phrase = ttk.Entry(self.customAnalysis, font = ('SegoeUI', 9))
        phrase.place(x='860', y='10', width=180, height=20)
        phrase.insert(0, 'Country ...')
        Label(self.customAnalysis, text="Country", bg="white").place(x='800', y='8')

        phrase = ttk.Entry(self.customAnalysis, font = ('SegoeUI', 9))
        phrase.place(x='600', y='10', width=180, height=20)
        phrase.insert(0, 'Example ...')
        Label(self.customAnalysis, text="Query", bg="white").place(x='550', y='8')

        cal = DateEntry(self.customAnalysis, width= 16, background= "gray", foreground= "black",bd=5)
        cal.place(x='550', y='8')


        return self.customAnalysis
    
       

    def __init__(self, main):
        super().__init__(main)
        style = ttk.Style()
        style.theme_create( "custom", parent="vista", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [0, 0], "background": "green" },
            "map":       {"background": [("selected", "red")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )
        style.configure('Treeview', rowheight=40)
        style.theme_use("custom")
        main.title('SM - Meter')
        ''' -------- GENERAL SETTINGS -------- '''
        # Window size
        main.resizable(0,0)
        main.geometry('1280x792')
        main.title('SM - Home')
        self.font = font.Font(weight='bold')
        
        # Create tab panel.
        self.notebook = ttk.Notebook(self, width=1280, height=793)
        
        # Create the content tabs.
        self.home = self.home()
        self.realTime = self.realTime()
        self.customAnalysis = self.customAnalysis()
        
        
        # Añadirlas al panel con su respectivo texto.
        self.notebook.add(self.home, text='Home', padding=20)
        self.notebook.add(self.realTime, text='Real time', padding=20)
        self.notebook.add(self.customAnalysis, text='Custom analysis', padding=20)
        self.notebook.pack()
        self.pack()



if __name__ == '__main__':
    main = Tk()
    app = App(main)
    app.mainloop()

