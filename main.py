from configparser import SafeConfigParser
import configparser
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import DateEntry

from apiSupport import take_secret_credentials, update_table, update_table_custom
COORDINATES = {'AF': '33,65,5000km', 'AL': '41,20,5000km', 'DZ': '28,3,5000km', 'AS': '-14.3333,-170,5000km', 'AD': '42.5,1.6,5000km', 'AO': '-12.5,18.5,5000km', 'AI': '18.25,-63.1667,5000km', 'AQ': '-90,0,5000km', 'AG': '17.05,-61.8,5000km', 'AR': '-34,-64,5000km', 'AM': '40,45,5000km', 'AW': '12.5,-69.9667,5000km', 'AU': '-27,133,5000km', 'AT': '47.3333,13.3333,5000km', 'AZ': '40.5,47.5,5000km', 'BS': '24.25,-76,5000km', 'BH': '26,50.55,5000km', 'BD': '24,90,5000km', 'BB': '13.1667,-59.5333,5000km', 'BY': '53,28,5000km', 'BE': '50.8333,4,5000km', 'BZ': '17.25,-88.75,5000km', 'BJ': '9.5,2.25,5000km', 'BM': '32.3333,-64.75,5000km', 'BT': '27.5,90.5,5000km', 'BO': '-17,-65,5000km', 'BA': '44,18,5000km', 'BW': '-22,24,5000km', 'BV': '-54.4333,3.4,5000km', 'BR': '-10,-55,5000km', 'IO': '-6,71.5,5000km', 'BN': '4.5,114.6667,5000km', 'BG': '43,25,5000km', 'BF': '13,-2,5000km', 'BI': '-3.5,30,5000km', 'KH': '13,105,5000km', 'CM': '6,12,5000km', 'CA': '60,-95,5000km', 'CV': '16,-24,5000km', 'KY': '19.5,-80.5,5000km', 'CF': '7,21,5000km', 'TD': '15,19,5000km', 'CL': '-30,-71,5000km', 'CN': '35,105,5000km', 'CX': '-10.5,105.6667,5000km', 'CC': '-12.5,96.8333,5000km', 'CO': '4,-72,5000km', 'KM': '-12.1667,44.25,5000km', 'CG': '-1,15,5000km', 'CD': '0,25,5000km', 'CK': '-21.2333,-159.7667,5000km', 'CR': '10,-84,5000km', 'CI': '8,-5,5000km', 'HR': '45.1667,15.5,5000km', 'CU': '21.5,-80,5000km', 'CY': '35,33,5000km', 'CZ': '49.75,15.5,5000km', 'DK': '56,10,5000km', 'DJ': '11.5,43,5000km', 'DM': '15.4167,-61.3333,5000km', 'DO': '19,-70.6667,5000km', 'EC': '-2,-77.5,5000km', 'EG': '27,30,5000km', 'SV': '13.8333,-88.9167,5000km', 'GQ': '2,10,5000km', 'ER': '15,39,5000km', 'EE': '59,26,5000km', 'ET': '8,38,5000km', 'FK': '-51.75,-59,5000km', 'FO': '62,-7,5000km', 'FJ': '-18,175,5000km', 'FI': '64,26,5000km', 'FR': '46,2,5000km', 'GF': '4,-53,5000km', 'PF': '-15,-140,5000km', 'TF': '-43,67,5000km', 'GA': '-1,11.75,5000km', 'GM': '13.4667,-16.5667,5000km', 'GE': '42,43.5,5000km', 'DE': '51,9,5000km', 'GH': '8,-2,5000km', 'GI': '36.1833,-5.3667,5000km', 'GR': '39,22,5000km', 'GL': '72,-40,5000km', 'GD': '12: -21.1,55.6,5000km', 'RO': '46,25,5000km', 'RU': '60,100,5000km', 'RW': '-2,30,5000km', 'SH': '-15.9333,-5.7,5000km', 'KN': '17.3333,-62.75,5000km', 'LC': '13.8833,-61.1333,5000km', 'PM': '46.8333,-56.3333,5000km', 'VC': '13.25,-61.2,5000km', 'WS': '-13.5833,-172.3333,5000km', 'SM': '43.7667,12.4167,5000km', 'ST': '1,7,5000km', 'SA': '25,45,5000km', 'SN': '14,-14,5000km', 'RS': '44,21,5000km', 'SC': '-4.5833,55.6667,5000km', 'SL': '8.5,-11.5,5000km', 'SG': '1.3667,103.8,5000km', 'SK': '48.6667,19.5,5000km', 'SI': '46,15,5000km', 'SB': '-8,159,5000km', 'SO': '10,49,5000km', 'ZA': '-29,24,5000km', 'GS': '-54.5,-37,5000km', 'SS': '8,30,5000km', 'ES': '40,-4,5000km', 'LK': '7,81,5000km', 'SD': '15,30,5000km', 'SR': '4,-56,5000km', 'SJ': '78,20,5000km', 'SZ': '-26.5,31.5,5000km', 'SE': '62,15,5000km', 'CH': '47,8,5000km', 'SY': '35,38,5000km', 'TW': '23.5,121,5000km', 'TJ': '39,71,5000km', 'TZ': '-6,35,5000km', 'TH': '15,100,5000km', 'TL': '-8.55,125.5167,5000km', 'TG': '8,1.1667,5000km', 'TK': '-9,-172,5000km', 'TO': '-20,-175,5000km', 'TT': '11,-61,5000km', 'TN': '34,9,5000km', 'TR': '39,35,5000km', 'TM': '40,60,5000km', 'TC': '21.75,-71.5833,5000km', 'TV': '-8,178,5000km', 'UG': '1,32,5000km', 'UA': '49,32,5000km', 'AE': '24,54,5000km', 'GB': '54,-2,5000km', 'US': '38,-97,5000km', 'UM': '19.2833,166.6,5000km', 'UY': '-33,-56,5000km', 'UZ': '41,64,5000km', 'VU': '-16,167,5000km', 'VE': '8,-66,5000km', 'VN': '16,106,5000km', 'VG': '18.5,-64.5,5000km', 'VI': '18.3333,-64.8333,5000km', 'WF': '-13.3,-176.2,5000km', 'EH': '24.5,-13,5000km', 'YE': '15,48,5000km', 'ZM': '-15,30,5000km', 'ZW': '-20,30,5000km'}

class App(Frame):
        
    def aboutTabSettings(self, parent):
        self.about = Frame(parent, width=372, height=590, bg="white")
        lb = LabelFrame(self.about, text='About ...', bg='white', fg='black', width=372, height=64, font=('SegoeUI 9'))
        lb.place(x='0', y='0')
        Label(lb, text="Version: 1.0.0", justify=LEFT, bg="white", font=('SegoeUI 9')).place(x='5', y='0')
        Label(lb, text='Date: 01-05-22', justify=LEFT, bg="white", font=('SegoeUI 9')).place(x='5', y='20')
        return self.about

    def apiTabSettings(self, parent):
        def modifyConfig():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('TWITTER','CONSUMER_KEY', ck_entry.get())
            config.set('TWITTER','CONSUMER_SECRET', cs_entry.get())
            config.set('TWITTER','ACCESS_TOKEN', at_entry.get())
            config.set('TWITTER','ACCESS_TOKEN_SECRET', as_entry.get())
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
                configfile.close()

        def toggleShowHideEntry(bool):
            if(bool):
                previous = ck_entry.get()
                ck_entry.delete(0, 'end')
                cs_entry.delete(0, 'end')
                as_entry.delete(0, 'end')
                at_entry.delete(0, 'end')
                if previous == '*************************************':
                    ck_entry.insert(0, tw_cr['ck'])
                    cs_entry.insert(0, tw_cr['csk'])
                    as_entry.insert(0, tw_cr['ats'])
                    at_entry.insert(0, tw_cr['at'])
                    showHideButtonTW.config(image=hide_button_image)
                else:
                    ck_entry.insert(0, '*************************************')
                    cs_entry.insert(0, '*************************************')
                    as_entry.insert(0, '*************************************')
                    at_entry.insert(0, '*************************************')
                    showHideButtonTW.config(image=show_button_image)
            else:
                previous = ci_entry.get()
                ci_entry.delete(0, 'end')
                s_entry.delete(0, 'end')
                if previous == '*************************************':
                    ci_entry.insert(0, tw_cr['ci'])
                    s_entry.insert(0, tw_cr['cs'])
                    showHideButtonRD.config(image=hide_button_image)
                else:
                    ci_entry.insert(0, '*************************************')
                    s_entry.insert(0, '*************************************')
                    showHideButtonRD.config(image=show_button_image)

        global save_button_image
        global reset_button_image
        global show_button_image
        global hide_button_image
        ''' -------- GENERAL ---------- '''
        self.api = Frame(parent, width=372, height=590, bg="white")
        info = LabelFrame(self.api, text=' ', bg='white', fg='black', width=372, height=65, font=('SegoeUI 9'))
        info.place(x='0', y='0')
        Label(info, text="The default keys are from a standard application, if you want to\nchange it for your own, modify the following fields.", justify=LEFT, bg="white", font=('SegoeUI 9')).place(x='5', y='0')
        #General Buttons
        save_button_image = PhotoImage(file=r'icons/save_button.png')
        saveButton = Button(self.api, image=save_button_image, command = modifyConfig, border=0, bg='white', activebackground='white')
        saveButton.place(x='280', y='560')
        ''' -------- TWITTER -------- '''
        #LabelFrames
        LabelFrame(self.api, text='Twitter', bg='white', fg='black', width=372, height=265, font=('SegoeUI 9')).place(x='0', y='77')
        #Labels
        Label(self.api, text="Consumer Key", bg="white").place(x='10', y='110') 
        Label(self.api, text="Consumer Secret", bg="white").place(x='10', y='160') 
        Label(self.api, text="Access Token", bg="white").place(x='10', y='210') 
        Label(self.api, text="Access Secret", bg="white").place(x='10', y='260') 
        #Entry
        tw_cr = take_secret_credentials() # Take creds from tw
        ck_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        ck_entry.place(x='120', y='112', width=220, height=20)
        ck_entry.insert(0, '*************************************')
        cs_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        cs_entry.place(x='120', y='162', width=220, height=20)
        cs_entry.insert(0, '*************************************')
        at_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        at_entry.place(x='120', y='212', width=220, height=20)
        at_entry.insert(0, '*************************************')
        as_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        as_entry.place(x='120', y='262', width=220, height=20)
        as_entry.insert(0, '*************************************')
        #Buttons
        reset_button_image = PhotoImage(file=r'icons/reset_button.png')
        Button(self.api, image=reset_button_image, command = None, border=0, bg='white', activebackground='white').place(x='280', y='300')
        show_button_image = PhotoImage(file=r'icons/show_button.png')
        hide_button_image = PhotoImage(file=r'icons/hide_button.png')
        showHideButtonTW = Button(self.api, image=show_button_image, command = lambda: toggleShowHideEntry(True), border=0, bg='white', activebackground='white')
        showHideButtonTW.place(x='340', y='90')
        ''' -------- REDDIT -------- '''
        #LabelFrames
        LabelFrame(self.api, text='Reddit', bg='white', fg='black', width=372, height=200, font=('SegoeUI 9')).place(x='0', y='352')
         #Labels
        Label(self.api, text="Client ID", bg="white").place(x='10', y='385') 
        Label(self.api, text="Secret", bg="white").place(x='10', y='435') 
        #Entry
        ci_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        ci_entry.place(x='120', y='387', width=220, height=20)
        ci_entry.insert(0, '*************************************')
        s_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        s_entry.place(x='120', y='437', width=220, height=20)
        s_entry.insert(0, '*************************************')
        #Buttons
        showHideButtonRD = Button(self.api, image=show_button_image, command = lambda: toggleShowHideEntry(False), border=0, bg='white', activebackground='white')
        showHideButtonRD.place(x='340', y='365')
        Button(self.api, image=reset_button_image, command = None, border=0, bg='white', activebackground='white').place(x='280', y='510')
        
        return self.api

    def generalTabSettings(self, parent):
        self.general = Frame(parent, width=372, height=590)
        lb = LabelFrame(self.general, text='General Settings', bg='white', fg='black', width=372, height=590, font=('SegoeUI 9'))
        lb.place(x='0', y='0')
        return self.general      

    def home(self):

        def uploadAction(textDirectory):
            textDirectory.set(filedialog.askopenfilename())

        def helpMenu():  
            rt1 = Toplevel(width=372, height=590)
            rt1.grab_set()
            rt1.resizable(0,0)
            notebook = ttk.Notebook(rt1)
            f1 = self.generalTabSettings(notebook)
            f2 = self.apiTabSettings(notebook)
            f3 = self.aboutTabSettings(notebook)
            notebook.add(f1, text="General", padding=20)
            notebook.add(f2, text="API", padding=20)
            notebook.add(f3, text="About ...", padding=20)
            notebook.pack()     

        def showHideFrame(toggle):
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
        settingsButton = Button(self.home, image=settings_button_image, command =lambda: helpMenu(), border=0, bg='#949494', activebackground='#949494')
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
        
        Button(self.home, image=advanced_button_image, command = lambda: showHideFrame(self.home.toggle), border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='865', y='68')
        compute_button_image = PhotoImage(file=r'icons/compute_button.png')
        Button(self.home, image=compute_button_image, command = None, border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='690', y='98')
        
        #TODO
        ''' -------- RIGHT-BOTTOM FRAME SETTINGS -------- '''
        # Frame label
        Label(self.home, text='CSV analysis', bg='#E4E4E4', fg='black', font=('SegoeUI 9'), justify=LEFT).place(x='655', y='370')

        # Frame buttons
        explore_button_image = PhotoImage(file=r'icons/explore_button.png')
        Button(self.home, image=compute_button_image, command = None, border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='690', y='467')
        Button(self.home, image=explore_button_image, command=lambda: uploadAction(textDirectory),border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='865', y='438')
        
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
        def showHideFrame(toggle):
            if toggle[0].place_info():
                for element in toggle:
                    element.place_forget()
            else:
                toggle[0].place(x='10',y='10')
                toggle[1].place(x='10',y='40')
                toggle[2].place(x='10',y='70')
                toggle[3].place(x='90', y='10', width=120, height=20)
                toggle[4].place(x='90', y='40', width=120, height=20)
                toggle[5].place(x='90', y='70', width=120, height=20)
                toggle[6].place(x='15', y='100')
                toggle[7].place(x='15', y='130')
                toggle[8].place(x='15', y='160')
                toggle[9].place(x='15', y='190')
                toggle[10].place(x='15', y='220')
                toggle[11].place(x='15', y='250')
                toggle[12].place(x='1000', y='75')
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
        analysis['columns'] = ('text', 'user_id', 'date', 'country', 'Platform','Results')
        analysis.column("#0", width=0,  stretch=NO)
        analysis.column("text",anchor=CENTER,width=450)
        analysis.column("user_id",anchor=CENTER,width=115)
        analysis.column("date",anchor=CENTER,width=165)
        analysis.column("country",anchor=CENTER,width=120)
        analysis.column("Platform",anchor=CENTER,width=175)
        analysis.column("Results",anchor=CENTER,width=175)
        analysis.heading("#0",text="",anchor=CENTER)
        analysis.heading("text",text="Text",anchor=CENTER)
        analysis.heading("user_id",text="User",anchor=CENTER)
        analysis.heading("date",text="Date",anchor=CENTER)
        analysis.heading("country",text="Country",anchor=CENTER)
        analysis.heading("Platform",text="Platform",anchor=CENTER)
        analysis.heading("Results",text="Results",anchor=CENTER)      
        analysis_scroll.config(command=analysis.yview)
        analysis_scroll.config(command=analysis.xview)

        # Buttons
        start_rt_button_image = PhotoImage(file=r'icons/start_button.png')
        Button(self.realTime, image=start_rt_button_image, command = lambda: update_table(analysis), border=0, bg='white', activebackground='white').place(x='1060', y='5')
        Button(self.realTime, image=advanced_button_image, command = lambda: showHideFrame(white_frame.toggle), border=0, bg='white', activebackground='white').place(x='1140', y='5')
        
        ''' -------- FRAMES SETTINGS -------- '''
        # Home frames
        Frame(self.realTime, bg='white', height=134, width=242, border=1)  # this is the background

        # Frame label
        Label(self.realTime, text='Social media mode:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT)
        Label(self.realTime, text='Analysis type:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT)

        # Frame radio-check buttons
        socialM_SF = IntVar()
        Radiobutton(self.realTime,text='Twitter', padx = 20,variable=socialM_SF,value=1, bg='#F9F9F9', activebackground='#F9F9F9')
        Radiobutton(self.realTime,text='Reddit', padx = 20,variable=socialM_SF,value=0, bg='#F9F9F9', activebackground='#F9F9F9')

        # Frame check buttons
        sentimentVarSF = IntVar()
        aggressiveVarSF = IntVar()
        Checkbutton(self.realTime, text = 'Sentiment', variable = sentimentVarSF, bg='#F9F9F9', activebackground='#F9F9F9', onvalue = 1, offvalue = 0)
        Checkbutton(self.realTime, text = 'Aggressive', variable = aggressiveVarSF, bg='#F9F9F9', activebackground='#F9F9F9', onvalue = 1, offvalue = 0)
        """ ADVANCED """
        # Home frames
        white_frame = Frame(self.realTime, bg='white', height=285, width=220, highlightbackground="black", highlightthickness=1)
        
        # Frame label
        subreddit_label = Label(white_frame, text='SubReddit**:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT, background='white')
        country_label = Label(white_frame, text='Country*:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT, background='white')
        query_label = Label(white_frame, text='Query:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT, background='white')

        #Entry
        entry_subreddit = ttk.Entry(white_frame, font = ('SegoeUI', 9))
        entry_country = ttk.Entry(white_frame, font = ('SegoeUI', 9))
        entry_query = ttk.Entry(white_frame, font = ('SegoeUI', 9))
        
        # Frame check buttons
        sentimentVarSF = IntVar()
        aggressiveVarSF = IntVar()
        englishVarSF = IntVar()
        spanishVarSF = IntVar()
        twitterVarSF = IntVar()
        redditVarSF = IntVar()
        sfCB = Checkbutton(white_frame, text = 'Sentiment', variable = sentimentVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        afCB = Checkbutton(white_frame, text = 'Aggressive', variable = aggressiveVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        efCB = Checkbutton(white_frame, text = 'English', variable = englishVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        spCB = Checkbutton(white_frame, text = 'Spanish', variable = spanishVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        twCB = Checkbutton(white_frame, text = 'Twitter', variable = twitterVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        rdCB = Checkbutton(white_frame, text = 'Reddit', variable = redditVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        white_frame.toggle = [subreddit_label, country_label, query_label, entry_subreddit, entry_country, entry_query, sfCB, afCB, efCB, spCB, twCB, rdCB, white_frame]  
        return self.realTime

    # Window for customized analysis
    def customAnalysis(self):

        def startCustomAnalysis():
            map = {'RB':[sentimentVarSF.get(), aggressiveVarSF.get(), englishVarSF.get(), spanishVarSF.get(), twitterVarSF.get(), redditVarSF.get()],'EN': [entry_subreddit.get(), country_phrase.get(), query_phrase.get(), numItems.get()]}
            numIt = str(map['EN'][3])
            if numIt.isdigit():
                update_table_custom(analysis, map)
            else:
                messagebox.showwarning("Input error", "Num items must be a number!")

        def showHideFrame(toggle):
            if toggle[0].place_info():
                for element in toggle:
                    element.place_forget()
            else:
                toggle[0].place(x='10',y='15')
                toggle[1].place(x='90', y='15', width=120, height=20)
                toggle[2].place(x='15', y='50')
                toggle[3].place(x='15', y='80')
                toggle[4].place(x='15', y='110')
                toggle[5].place(x='15', y='140')
                toggle[6].place(x='15', y='170')
                toggle[7].place(x='15', y='200')
                toggle[8].place(x='1000', y='75')
        
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
        analysis['columns'] = ('text', 'user_id', 'date', 'country', 'Platform','Results')
        analysis.column("#0", width=0,  stretch=NO)
        analysis.column("text",anchor=CENTER,width=450)
        analysis.column("user_id",anchor=CENTER,width=115)
        analysis.column("date",anchor=CENTER,width=165)
        analysis.column("country",anchor=CENTER,width=120)
        analysis.column("Platform",anchor=CENTER,width=175)
        analysis.column("Results",anchor=CENTER,width=175)
        analysis.heading("#0",text="",anchor=CENTER)
        analysis.heading("text",text="Text",anchor=CENTER)
        analysis.heading("user_id",text="User",anchor=CENTER)
        analysis.heading("date",text="Date",anchor=CENTER)
        analysis.heading("country",text="Country",anchor=CENTER)
        analysis.heading("Platform",text="Platform",anchor=CENTER)
        analysis.heading("Results",text="Results",anchor=CENTER)
        analysis_scroll.config(command=analysis.yview)
        analysis_scroll.config(command=analysis.xview)

        #Entry
        #start_date = DateEntry(self.customAnalysis, width= 16, background= "gray", foreground= "black",bd=5)
        #start_date.place(x='95', y='8')
        #end_date = DateEntry(self.customAnalysis, width= 16, background= "gray", foreground= "black",bd=5)
        #end_date.place(x='295', y='8')
        numItems = ttk.Entry(self.customAnalysis, font = ('SegoeUI', 9))
        numItems.place(x="600", y="10", width=100, height=20)
        query_phrase = ttk.Entry(self.customAnalysis, font = ('SegoeUI', 9))
        query_phrase.place(x='770', y='10', width=100, height=20)
        query_phrase.insert(0, '')
        country_phrase = ttk.Combobox(self.customAnalysis,font = ('SegoeUI', 9), state="readonly", values=list(COORDINATES.keys()))
        country_phrase.place(x='940', y='10', width=100, height=20)
        country_phrase.insert(0, 'ES')
        #Label(self.customAnalysis, text="Start Date", bg="white").place(x='25', y='8')
        #Label(self.customAnalysis, text="End Date", bg="white").place(x='225', y='8')
        Label(self.customAnalysis, text="Samples (N)", bg="white").place(x='520', y='8')
        Label(self.customAnalysis, text="Query", bg="white").place(x='720', y='8')
        Label(self.customAnalysis, text="Country", bg="white").place(x='880', y='8')
        
        # Buttons
        start_ca_button_image = PhotoImage(file=r'icons/start_button.png')
        Button(self.customAnalysis, image=start_ca_button_image, command = startCustomAnalysis, border=0, bg='white', activebackground='white').place(x='1060', y='5')
        Button(self.customAnalysis, image=advanced_button_image, command = lambda: showHideFrame(white_frame.toggle), border=0, bg='white', activebackground='white').place(x='1145', y='5')

        """ ADVANCED """
        # Home frames
        white_frame = Frame(self.customAnalysis, bg='white', height=260, width=220, highlightbackground="black", highlightthickness=1)
        
        # Frame label
        subreddit_label = Label(white_frame, text='SubReddit**:', bg='#F9F9F9', fg='black', font=('SegoeUI 9'), justify=LEFT, background='white')

        #Entry
        entry_subreddit = ttk.Entry(white_frame, font = ('SegoeUI', 9))
        
        # Frame check buttons
        sentimentVarSF = IntVar()
        aggressiveVarSF = IntVar()
        englishVarSF = IntVar()
        spanishVarSF = IntVar()
        twitterVarSF = IntVar()
        redditVarSF = IntVar()
        sfCB = Checkbutton(white_frame, text = 'Sentiment', variable = sentimentVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        afCB = Checkbutton(white_frame, text = 'Aggressive', variable = aggressiveVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        efCB = Checkbutton(white_frame, text = 'English', variable = englishVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        spCB = Checkbutton(white_frame, text = 'Spanish', variable = spanishVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        twCB = Checkbutton(white_frame, text = 'Twitter', variable = twitterVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        rdCB = Checkbutton(white_frame, text = 'Reddit', variable = redditVarSF, bg='white', activebackground='white', onvalue = 1, offvalue = 0)
        white_frame.toggle = [subreddit_label, entry_subreddit, sfCB, afCB, efCB, spCB, twCB, rdCB, white_frame]  

        return self.customAnalysis
    
    def __init__(self, main):
        def defineStyles():
            style = ttk.Style()
            style.theme_create( "custom", parent="vista", settings={
            "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
            "TNotebook.Tab": {
                "configure": {"padding": [0, 0], "background": "green" },
                "map":       {"background": [("selected", "red")],
                            "expand": [("selected", [1, 1, 1, 0])] } } } )
            style.theme_use("custom")
            style.configure('Treeview', rowheight=30, highlightthickness=0, bd=0, font=('Calibri', 11), bg="white")
            style.configure('TEntry', bordercolor='black')
        super().__init__(main)
        defineStyles()
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

