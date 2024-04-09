import datetime
from tkinter import CENTER, LEFT, NO, RIGHT, Y, Button, Checkbutton, Frame, IntVar, Label, LabelFrame, PhotoImage, Radiobutton, Scrollbar, StringVar, Tk, Toplevel, font

from regex import E
from apiSupport import export_results, should_update_chart, stop_real_time_analysis, take_predict_rd, take_predict_tw, take_secret_credentials, update_table_custom, update_table_real_time, update_to_real_time_dictionary
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gensim.parsing.preprocessing import remove_stopwords
from neural import activate_model, disable_model, load_models, model_status, predict
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import messagebox
from typing import Counter
from operator import xor
from tkinter import ttk
import pandas as pd
import numpy as np
import configparser
import webbrowser
import threading
import time
import os
from tkcalendar import DateEntry
COORDINATES = {'AF': '33,65,5000km', 'AL': '41,20,5000km', 'DZ': '28,3,5000km', 'AS': '-14.3333,-170,5000km', 'AD': '42.5,1.6,5000km', 'AO': '-12.5,18.5,5000km', 'AI': '18.25,-63.1667,5000km', 'AQ': '-90,0,5000km', 'AG': '17.05,-61.8,5000km', 'AR': '-34,-64,5000km', 'AM': '40,45,5000km', 'AW': '12.5,-69.9667,5000km', 'AU': '-27,133,5000km', 'AT': '47.3333,13.3333,5000km', 'AZ': '40.5,47.5,5000km', 'BS': '24.25,-76,5000km', 'BH': '26,50.55,5000km', 'BD': '24,90,5000km', 'BB': '13.1667,-59.5333,5000km', 'BY': '53,28,5000km', 'BE': '50.8333,4,5000km', 'BZ': '17.25,-88.75,5000km', 'BJ': '9.5,2.25,5000km', 'BM': '32.3333,-64.75,5000km', 'BT': '27.5,90.5,5000km', 'BO': '-17,-65,5000km', 'BA': '44,18,5000km', 'BW': '-22,24,5000km', 'BV': '-54.4333,3.4,5000km', 'BR': '-10,-55,5000km', 'IO': '-6,71.5,5000km', 'BN': '4.5,114.6667,5000km', 'BG': '43,25,5000km', 'BF': '13,-2,5000km', 'BI': '-3.5,30,5000km', 'KH': '13,105,5000km', 'CM': '6,12,5000km', 'CA': '60,-95,5000km', 'CV': '16,-24,5000km', 'KY': '19.5,-80.5,5000km', 'CF': '7,21,5000km', 'TD': '15,19,5000km', 'CL': '-30,-71,5000km', 'CN': '35,105,5000km', 'CX': '-10.5,105.6667,5000km', 'CC': '-12.5,96.8333,5000km', 'CO': '4,-72,5000km', 'KM': '-12.1667,44.25,5000km', 'CG': '-1,15,5000km', 'CD': '0,25,5000km', 'CK': '-21.2333,-159.7667,5000km', 'CR': '10,-84,5000km', 'CI': '8,-5,5000km', 'HR': '45.1667,15.5,5000km', 'CU': '21.5,-80,5000km', 'CY': '35,33,5000km', 'CZ': '49.75,15.5,5000km', 'DK': '56,10,5000km', 'DJ': '11.5,43,5000km', 'DM': '15.4167,-61.3333,5000km', 'DO': '19,-70.6667,5000km', 'EC': '-2,-77.5,5000km', 'EG': '27,30,5000km', 'SV': '13.8333,-88.9167,5000km', 'GQ': '2,10,5000km', 'ER': '15,39,5000km', 'EE': '59,26,5000km', 'ET': '8,38,5000km', 'FK': '-51.75,-59,5000km', 'FO': '62,-7,5000km', 'FJ': '-18,175,5000km', 'FI': '64,26,5000km', 'FR': '46,2,5000km', 'GF': '4,-53,5000km', 'PF': '-15,-140,5000km', 'TF': '-43,67,5000km', 'GA': '-1,11.75,5000km', 'GM': '13.4667,-16.5667,5000km', 'GE': '42,43.5,5000km', 'DE': '51,9,5000km', 'GH': '8,-2,5000km', 'GI': '36.1833,-5.3667,5000km', 'GR': '39,22,5000km', 'GL': '72,-40,5000km', 'GD': '12: -21.1,55.6,5000km', 'RO': '46,25,5000km', 'RU': '60,100,5000km', 'RW': '-2,30,5000km', 'SH': '-15.9333,-5.7,5000km', 'KN': '17.3333,-62.75,5000km', 'LC': '13.8833,-61.1333,5000km', 'PM': '46.8333,-56.3333,5000km', 'VC': '13.25,-61.2,5000km', 'WS': '-13.5833,-172.3333,5000km', 'SM': '43.7667,12.4167,5000km', 'ST': '1,7,5000km', 'SA': '25,45,5000km', 'SN': '14,-14,5000km', 'RS': '44,21,5000km', 'SC': '-4.5833,55.6667,5000km', 'SL': '8.5,-11.5,5000km', 'SG': '1.3667,103.8,5000km', 'SK': '48.6667,19.5,5000km', 'SI': '46,15,5000km', 'SB': '-8,159,5000km', 'SO': '10,49,5000km', 'ZA': '-29,24,5000km', 'GS': '-54.5,-37,5000km', 'SS': '8,30,5000km', 'ES': '40,-4,5000km', 'LK': '7,81,5000km', 'SD': '15,30,5000km', 'SR': '4,-56,5000km', 'SJ': '78,20,5000km', 'SZ': '-26.5,31.5,5000km', 'SE': '62,15,5000km', 'CH': '47,8,5000km', 'SY': '35,38,5000km', 'TW': '23.5,121,5000km', 'TJ': '39,71,5000km', 'TZ': '-6,35,5000km', 'TH': '15,100,5000km', 'TL': '-8.55,125.5167,5000km', 'TG': '8,1.1667,5000km', 'TK': '-9,-172,5000km', 'TO': '-20,-175,5000km', 'TT': '11,-61,5000km', 'TN': '34,9,5000km', 'TR': '39,35,5000km', 'TM': '40,60,5000km', 'TC': '21.75,-71.5833,5000km', 'TV': '-8,178,5000km', 'UG': '1,32,5000km', 'UA': '49,32,5000km', 'AE': '24,54,5000km', 'GB': '54,-2,5000km', 'US': '38,-97,5000km', 'UM': '19.2833,166.6,5000km', 'UY': '-33,-56,5000km', 'UZ': '41,64,5000km', 'VU': '-16,167,5000km', 'VE': '8,-66,5000km', 'VN': '16,106,5000km', 'VG': '18.5,-64.5,5000km', 'VI': '18.3333,-64.8333,5000km', 'WF': '-13.3,-176.2,5000km', 'EH': '24.5,-13,5000km', 'YE': '15,48,5000km', 'ZM': '-15,30,5000km', 'ZW': '-20,30,5000km'}
dictionary_csv_results = {'text':[],'Sentiment':[], 'Aggressive':[]}
dictionary_custom_analysis = {'text':[],'Sentiment':[], 'Aggressive':[]}
HIDE_STRING = '*************************************'
FONT_SE12 = 'SegoeUI 12'
FONT_SE9 = 'SegoeUI 9'
FONT_SE8 = 'SegoeUI 8'
DISTRIBUTION_FIGURE_SENTIMENT_TITLE = 'Distribution of sentiments'
DISTRIBUTION_FIGURE_AGGRESSIVE_TITLE = 'Distribution of aggressiveness'
SENTIMENT_PIE_CHART_LABELS = ["Positive", "Negative"]
AGGRESIVE_PIE_CHART_LABELS = ["Hate", "No hate"]

# AUX: Method that creates a bar chart by passing two sets of data, figure size and X-axis bottom label. It returns a pyplot type figure.
def create_line_chart(param_list_sent, param_list_agrs, moment, figsize):
    fig = plt.Figure(figsize = figsize,dpi = 100, layout='tight')
    ax = fig.add_subplot(111)
    ax.plot(moment,param_list_sent, label = 'Positiveness', marker = 'o', color = 'tab:green')
    ax.plot(moment,param_list_agrs, label = 'Aggresiveness', marker = 'o', color = 'tab:orange')
    ax.set_ylim([0,100])
    ax.legend(loc = 'upper right')
    ax.set_title('Aggressiveness and sentiment over time.', fontweight ="bold", fontsize=10)
    return fig

# AUX: Method that adds three graphs to the custom section of the application, it is updated after obtaining
# all the data requested by the user. It creates one bar chart and two pie charts. 
def put_custom_graphs(dictionary, sentiment, aggressive, parent):
    y, non_figure = np.array([0,1]), plt.Figure(figsize=(3.5,3.5), dpi=100, layout='tight')
    ax = non_figure.add_subplot(111)
    ax.pie(y, radius=1, shadow=True, colors=["white", "grey"])
    if(sentiment == 1):
        sentiment_figure = create_pie_chart(dictionary['Sentiment'], SENTIMENT_PIE_CHART_LABELS,["Positive", "Neutral", "Negative"], (3.5,3.5), ["#9CFF4F", "#CCCCCC", "#FF634F"], DISTRIBUTION_FIGURE_SENTIMENT_TITLE)
    else:
        ax.set_title(DISTRIBUTION_FIGURE_SENTIMENT_TITLE, fontweight ="bold", fontsize=10)
        sentiment_figure = non_figure
    if(aggressive == 1):
        aggressive_figure = create_pie_chart(dictionary['Aggressive'], AGGRESIVE_PIE_CHART_LABELS,["Hate", "Neutral", "No hate"], (3.5,3.5), ["#FFD84F", "#CCCCCC", "#F1FF4F"], DISTRIBUTION_FIGURE_AGGRESSIVE_TITLE)
    else:
        ax.set_title(DISTRIBUTION_FIGURE_AGGRESSIVE_TITLE, fontweight ="bold", fontsize=10)
        aggressive_figure = non_figure
    frequency_figure = create_bar_chart(dictionary['text'],(4,2.5))
    frequency_words = FigureCanvasTkAgg(frequency_figure, parent)
    frequency_words.get_tk_widget().place(x='950', y='520')
    sentiment_figure_canvas = FigureCanvasTkAgg(sentiment_figure, parent) 
    sentiment_figure_canvas.get_tk_widget().place(x='500', y='510')
    aggresive_figure_canvas = FigureCanvasTkAgg(aggressive_figure, parent) 
    aggresive_figure_canvas.get_tk_widget().place(x='0', y='510')

#AUX: Method that creates a complete pie chart of six elements. This method is used to create in a single graph both the distribution of sentiment and aggressiveness. 
def create_complete_pie_chart(param_list_sent, param_list_agrs, labels, labels_for_plot, figsize, colors, title):
    chart = [0,0,0,0,0,0]
    param_list = []
    param_list.extend(param_list_agrs)
    param_list.extend(param_list_sent)
    for element in param_list:
        label = element.split(":")
        element_type, element_pnt = label[0], float(label[1].replace("%","").strip())
        if(element_type == labels[0] and element_pnt > 69):
            chart[0] = chart[0] + 1
        elif(element_type == labels[1] and element_pnt > 69):      
            chart[2] = chart[2] + 1
        elif(element_type == labels[1]):
            chart[1] = chart[1] + 1
        elif(element_type == labels[2] and element_pnt > 69):
            chart[3] = chart[3] + 1
        elif(element_type == labels[3] and element_pnt > 69):
            chart[4] = chart[4] + 1
        else:
            chart[5] = chart[5] + 1
    chart_sent = percentage_distribution_list(chart[:3])
    chart_sent.extend(percentage_distribution_list(chart[3:]))
    figure = create_figure(chart_sent, labels_for_plot, figsize,colors,title)
    return figure

#AUX: Method that returns the percentage of values of a key in a dictionary with respect to the rest. 
def take_percentage(dictionary, label_dict, first_label):
    distribution = [0,0]
    for element in dictionary[label_dict]:
        element_type = element.split(":")[0].strip().lower()

        if(element_type == first_label.lower()):
            distribution[0] = distribution[0] + 1
        else:
            distribution[1] = distribution[1] + 1
    return percentage_distribution_list(distribution)[0]

# AUX: Method that adds three graphs to the real time section of the application, updated every few minutes set by the user.
# It creates a bar chart, a pie chart and a line chart. The graphs are updated as new data is collected.
def put_realtime_graphs(sentiment, aggressive, parent):
    dictionary, chart, freq, moment, punt_sent, punt_aggrs = update_to_real_time_dictionary(), True, 60, [0],[0],[0]
    time.sleep(freq)
    while(chart):
        moment.append(moment[len(moment)-1]+freq)
        punt_sent.append(take_percentage(dictionary, 'Sentiment', 'Positive'))
        punt_aggrs.append(take_percentage(dictionary, 'Aggressive', 'Hate')) 
        if(sentiment == 1 and aggressive == 0):
            pie_figure = create_pie_chart(dictionary['Sentiment'], SENTIMENT_PIE_CHART_LABELS,["Positive", "Neutral", "Negative"], (3.5,3.5), ["#9CFF4F", "#CCCCCC", "#FF634F"], DISTRIBUTION_FIGURE_SENTIMENT_TITLE)
        elif(sentiment == 0 and aggressive == 1):
            pie_figure = create_pie_chart(dictionary['Aggressive'], ["Hate", "Not sure", "No hate"],["H", "- ", "NH"], (3.5,3.5), ["#FFD84F", "#CCCCCC", "#F1FF4F"], DISTRIBUTION_FIGURE_AGGRESSIVE_TITLE)
        else:
            pie_figure = create_complete_pie_chart(dictionary['Sentiment'], dictionary['Aggressive'], ["Positive","Negative","Hate", "No hate"],["Positive", "Neutral (SE) ", "Negative","Hate", "Neutral (AG) ", "No hate"], (3.5,3.5), ["#9CFF4F", "#CCCCCC", "#FF634F","#FFD84F", "#CCCCCC", "#F1FF4F"], 'Distribution of aggressiveness/feelings')
        fluctuation_figure = create_line_chart(punt_sent, punt_aggrs, moment, (4,2.5))
        fluctuation_figure = FigureCanvasTkAgg(fluctuation_figure, parent)
        fluctuation_figure.get_tk_widget().place(x="0", y="510")
        frequency_figure = create_bar_chart(dictionary['text'],(4,2.5))
        frequency_words = FigureCanvasTkAgg(frequency_figure, parent)
        frequency_words.get_tk_widget().place(x='950', y='530')
        pie_figure_canvas = FigureCanvasTkAgg(pie_figure, parent) 
        pie_figure_canvas.get_tk_widget().place(x='500', y='510')
        time.sleep(freq)
        chart = should_update_chart()
        dictionary = update_to_real_time_dictionary()

# AUX: Method that opens a url passed by parameters.
def callback(url):
    webbrowser.open_new(url)

# AUX: Method that creates a table on the parent element passed by parameters and adds two dictionary elements. This method is used to create such a table when parsing a csv. 
def create_table(parent, dict_res):
    tree=ttk.Treeview(parent, column=("c1", "c2", "c3"), show='headings', height=3)
    tree.column("# 1",anchor=CENTER, stretch=NO, width=120)
    tree.heading("# 1", text="Text")
    tree.column("# 2", anchor=CENTER, stretch=NO, width=85)
    tree.heading("# 2", text="Sentiment")
    tree.column("# 3", anchor=CENTER, stretch=NO, width=85)
    tree.heading("# 3", text=" Aggressiveness")
    tree.place(x='1050', y='500')
    tree.insert('', 'end',text="1",values=(dict_res['text'][0], dict_res['Sentiment'][0], dict_res['Aggressive'][0]))
    tree.insert('', 'end',text="2",values=(dict_res['text'][1], dict_res['Sentiment'][1], dict_res['Aggressive'][1]))
    tree.insert('', 'end',text="3",values=('...', '...', '...'))

#AUX(2): Method that creates a simple pie chart of three elements. This method is used to create a single graph of sentiment or aggressiveness. 
def create_figure(array, labels, figsize, colors, title):
    figure = plt.Figure(figsize=figsize, dpi=100, layout='tight')
    ax = figure.add_subplot(111)
    ax.pie(array, labels=labels, radius=1,autopct='%0.2f%%', shadow=True, colors=colors)
    ax.set_title(title, fontweight ="bold", fontsize=10)
    return figure

#AUX: Method that creates a simple pie chart of three elements. This method is used to create a single graph of sentiment or aggressiveness. 
def create_pie_chart(param_list, labels, labels_for_plot, figsize, colors,title):
    chart = [0,0,0]
    for element in param_list:
        label = element.split(":")
        element_type, element_pnt = label[0], float(label[1].replace("%","").strip())
        if(element_type == labels[0] and element_pnt > 69):
            chart[0] = chart[0] + 1
        elif(element_type == labels[1] and element_pnt > 69):      
            chart[2] = chart[2] + 1
        else:
            chart[1] = chart[1] + 1
    chart = np.array(percentage_distribution_list(chart))
    figure = create_figure(chart, labels_for_plot, figsize,colors, title)
    return figure

#AUX: Method that returns the percentage of elements in a list.
def percentage_distribution_list(chart):
    total = np.sum(chart)
    for ix in range(0,len(chart)):
        chart[ix] = (chart[ix] / total) * 100
    return chart

# AUX: Method that creates a bar chart by passing a set of data and figure size. It returns a pyplot type figure of the most frequence words.
def create_bar_chart(array, figsize):
    array = [remove_stopwords(text) for text in array]
    word_frequency = Counter(" ".join(array).split()).most_common(10)
    words, counts, figure = [word for word, _ in word_frequency],[counts for _, counts in word_frequency], plt.Figure(figsize=figsize, dpi=100, layout='tight')
    ax = figure.add_subplot(111)
    ax.bar(words,counts, color = 'lightsteelblue')
    ax.tick_params(axis='x', labelrotation=30)
    ax.set_title('Most frequent words.', fontweight ="bold", fontsize=10)
    return figure

class App(Frame):
    
    # Method that creates a tab with data about the application, date and version.
    def aboutTabSettings(self, parent):
        self.about = Frame(parent, width=372, height=590, bg="white")
        lb = LabelFrame(self.about, text='About ...', bg='white', fg='black', width=372, height=64, font=(FONT_SE9))
        lb.place(x='0', y='0')
        Label(lb, text="Version: 1.0.0", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='5', y='0')
        Label(lb, text='Date: 01-05-22', justify=LEFT, bg="white", font=(FONT_SE9)).place(x='5', y='20')
        return self.about

    # Method that creates a tab with the api keys data, to be able to modify them.
    def apiTabSettings(self, parent):
       
        # AUX: Method that edits the keys stored in the configuration file.
        def modify_config():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('TWITTER','CONSUMER_KEY', ck_entry.get())
            config.set('TWITTER','CONSUMER_SECRET', cs_entry.get())
            config.set('TWITTER','ACCESS_TOKEN', at_entry.get())
            config.set('TWITTER','ACCESS_TOKEN_SECRET', as_entry.get())
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
                configfile.close()
        
        # AUX: Method that hides or displays keys in clear text.
        def toggle_show_hide_entry(bool):
            keys = take_secret_credentials()
            if(bool):
                previous = ck_entry.get()
                ck_entry.delete(0, 'end')
                cs_entry.delete(0, 'end')
                as_entry.delete(0, 'end')
                at_entry.delete(0, 'end')
                if previous == HIDE_STRING:
                    ck_entry.insert(0, keys['ck'])
                    cs_entry.insert(0, keys['csk'])
                    as_entry.insert(0, keys['ats'])
                    at_entry.insert(0, keys['at'])
                    showHideButtonTW.config(image=hide_button_image)
                else:
                    ck_entry.insert(0, HIDE_STRING)
                    cs_entry.insert(0, HIDE_STRING)
                    as_entry.insert(0, HIDE_STRING)
                    at_entry.insert(0, HIDE_STRING)
                    showHideButtonTW.config(image=show_button_image)
            else:
                previous = ci_entry.get()
                ci_entry.delete(0, 'end')
                s_entry.delete(0, 'end')
                if previous == HIDE_STRING:
                    ci_entry.insert(0, keys['ci'])
                    s_entry.insert(0, keys['cs'])
                    showHideButtonRD.config(image=hide_button_image)
                else:
                    ci_entry.insert(0, HIDE_STRING)
                    s_entry.insert(0, HIDE_STRING)
                    showHideButtonRD.config(image=show_button_image)

        global save_button_image, show_button_image, hide_button_image
        ''' -------- GENERAL ---------- '''
        self.api = Frame(parent, width=372, height=590, bg="white")
        info = LabelFrame(self.api, text=' ', bg='white', fg='black', width=372, height=65, font=(FONT_SE9))
        info.place(x='0', y='0')
        Label(info, text="The default keys are from a standard application, if you want to\nchange it for your own, modify the following fields.", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='5', y='0')
        #General Buttons
        save_button_image = PhotoImage(file=r'icons/save_button.png')
        saveButton = Button(self.api, image=save_button_image, command = modify_config, border=0, bg='white', activebackground='white')
        saveButton.place(x='280', y='560')
        ''' -------- TWITTER -------- '''
        #LabelFrames
        LabelFrame(self.api, text='Twitter', bg='white', fg='black', width=372, height=265, font=(FONT_SE9)).place(x='0', y='77')
        #Labels
        Label(self.api, text="Consumer Key", bg="white").place(x='10', y='110') 
        Label(self.api, text="Consumer Secret", bg="white").place(x='10', y='160') 
        Label(self.api, text="Access Token", bg="white").place(x='10', y='210') 
        Label(self.api, text="Access Secret", bg="white").place(x='10', y='260') 
        #Entry
        ck_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        ck_entry.place(x='120', y='112', width=220, height=20)
        ck_entry.insert(0, HIDE_STRING)
        cs_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        cs_entry.place(x='120', y='162', width=220, height=20)
        cs_entry.insert(0, HIDE_STRING)
        at_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        at_entry.place(x='120', y='212', width=220, height=20)
        at_entry.insert(0, HIDE_STRING)
        as_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        as_entry.place(x='120', y='262', width=220, height=20)
        as_entry.insert(0, HIDE_STRING)
        #Buttons
        # COMMAND TODO
        show_button_image = PhotoImage(file=r'icons/show_button.png')
        hide_button_image = PhotoImage(file=r'icons/hide_button.png')
        showHideButtonTW = Button(self.api, image=show_button_image, command = lambda: toggle_show_hide_entry(True), border=0, bg='white', activebackground='white')
        showHideButtonTW.place(x='340', y='90')
        ''' -------- REDDIT -------- '''
        #LabelFrames
        LabelFrame(self.api, text='Reddit', bg='white', fg='black', width=372, height=200, font=(FONT_SE9)).place(x='0', y='352')
        #Labels
        Label(self.api, text="Client ID", bg="white").place(x='10', y='385') 
        Label(self.api, text="Secret", bg="white").place(x='10', y='435') 
        #Entry
        ci_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        ci_entry.place(x='120', y='387', width=220, height=20)
        ci_entry.insert(0, HIDE_STRING)
        s_entry = ttk.Entry(self.api, font = ('SegoeUI', 9))
        s_entry.place(x='120', y='437', width=220, height=20)
        s_entry.insert(0, HIDE_STRING)
        #Buttons
        showHideButtonRD = Button(self.api, image=show_button_image, command = lambda: toggle_show_hide_entry(False), border=0, bg='white', activebackground='white')
        showHideButtonRD.place(x='340', y='365')
        
        return self.api

    # Method that creates a tab with the general settings, to be able to stop o run the models.
    def generalTabSettings(self, parent):
        
        # AUX: Method that displays a text when it passes over the label.
        def on_enter(self):
            lb1.configure(text="It will take some time for the model to be up and running.\nPlease be patient and wait until the model is ready.")
        # Method that hide a text when it passes over the label.
        def on_leave(self):
            lb1.configure(text="")

        # Method that changes the image depending on whether the model has been loaded. It also gives the possibility to load or stop the model. 
        def set_buttons():
            global toggle_off_image, toggle_on_image
            toggle_on_image = PhotoImage(file=r'icons/toggle_on.png')
            toggle_off_image = PhotoImage(file=r'icons/toggle_off.png')
            models = model_status()
            y=0
            for index, model in enumerate(models):
                if(model):
                    btn = Button(lb, image=toggle_on_image, border=0, bg='white', activebackground='white')
                    btn.configure(command = lambda btn_number=index, btn_selected=btn: threading.Thread(target=disable_model, args=[btn_number, btn_selected, toggle_off_image]).start())
                    btn.place(x=5, y=y)
                    
                else:
                    btn = Button(lb, image=toggle_off_image, border=0, bg='white', activebackground='white')
                    btn.configure(command=lambda btn_number=index, btn_selected=btn: threading.Thread(target=activate_model, args=[btn_number, btn_selected, toggle_on_image]).start())
                    btn.place(x=5, y=y)
                    btn.bind("<Enter>", on_enter)
                    btn.bind("<Leave>", on_leave)
                
                y = y+30
               
        self.general = Frame(parent, width=372, height=590)
        lb = LabelFrame(self.general, text='General Settings', bg='white', fg='black', width=372, height=590, font=(FONT_SE9))
        lb.place(x='0', y='0')
        Label(lb, text="[ENG] Sentiment analysis twitter", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='45', y='0')
        Label(lb, text="[ENG] Aggressive analysis twitter", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='45', y='30')
        Label(lb, text="[ENG] Sentiment analysis reddit", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='45', y='60')
        Label(lb, text="[ENG] Aggressive analysis reddit", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='45', y='90')
        Label(lb, text="[ESP] Sentiment analysis", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='45', y='120')
        Label(lb, text="[ESP] Aggressive analysis", justify=LEFT, bg="white", font=(FONT_SE9)).place(x='45', y='150')
        lb1 = Label(lb, justify=LEFT, bg="white", font=(FONT_SE9))
        lb1.place(x='20', y='200')
        set_buttons()
        return self.general      

    # Window for home    
    def home(self):
        # Method that sets the text directory variable to the name of a file chosen by the user on his local computer.
        def upload_action(textDirectory):
            textDirectory.set(filedialog.askopenfilename())

        # Method that creates a help menu with three options. General, API and about.
        def help_menu():  
            rt1 = Toplevel(width=372, height=590)
            rt1.grab_set()
            rt1.resizable(0,0)
            notebook = ttk.Notebook(rt1)
            f1, f2, f3 = self.generalTabSettings(notebook), self.apiTabSettings(notebook), self.aboutTabSettings(notebook)
            notebook.add(f1, text="General", padding=20)
            notebook.add(f2, text="API", padding=20)
            notebook.add(f3, text="About ...", padding=20)
            notebook.pack()     

        # Method that displays a column in a new tab with the CSV dictionary items. 
        def show_results():
            global dictionary_csv_results
            rt1 = Toplevel(width=655, height=525, background="white")
            rt1.grab_set()
            rt1.resizable(0,0)
            tree=ttk.Treeview(rt1, column=("c1", "c2", "c3"), show='headings', height=4)
            tree.column("# 1",anchor=CENTER, stretch=NO, width=415)
            tree.heading("# 1", text="Text")
            tree.column("# 2", anchor=CENTER, stretch=NO, width=100)
            tree.heading("# 2", text="Sentiment")
            tree.column("# 3", anchor=CENTER, stretch=NO, width=100)
            tree.heading("# 3", text=" Aggressiveness")
            sentiment_figure = create_pie_chart(dictionary_csv_results['Sentiment'], SENTIMENT_PIE_CHART_LABELS,["Positive", "Neutral", "Negative"], (3,3),["#9CFF4F", "#CCCCCC", "#FF634F"], "Sentiment distribution")
            aggressive_figure = create_pie_chart(dictionary_csv_results['Aggressive'], AGGRESIVE_PIE_CHART_LABELS,["Hate", "Neutral", "No hate"], (3,3), ["#FFD84F", "#CCCCCC", "#F1FF4F"], "Aggressiveness distribution")
            scatter1 = FigureCanvasTkAgg(sentiment_figure, rt1) 
            scatter1.get_tk_widget().place(x='20', y='230')
            scatter2 = FigureCanvasTkAgg(aggressive_figure, rt1) 
            scatter2.get_tk_widget().place(x='300', y='230')
            tree.place(x='20', y='20')
            for index in range(0, len(dictionary_csv_results['text'])):
                tree.insert('', 'end',text="1",values=(dictionary_csv_results['text'][index], dictionary_csv_results['Sentiment'][index], dictionary_csv_results['Aggressive'][index]))

        # Method that shows and hides the advanced elements of the simple analysis. 
        def show_hide_frame(toggle):
            if toggle[0].place_info():
                for element in toggle:
                    element.place_forget()
            else:
                toggle[4].place(x='1100',y='40')
                toggle[5].place(x='1110', y='70')
                toggle[6].place(x='1145', y='120')
                toggle[1].place(x='1220', y='50')
                toggle[0].place(x='1220', y='75')
                toggle[2].place(x='1240', y='105')
                toggle[3].place(x='1240', y='130')
        
        # Method that analyzes a simple sentence and sets the results in the home window. 
        def analyze_sentence():
            progressbar = ttk.Progressbar(self.home, style="red.Horizontal.TProgressbar")
            progressbar.place(x='770', y='350', width=100)
            try:
                text, lang, sm, sa, aa = phrase.get(), language_UF.get(), socialM_SF.get(), sentimentVarSF.get(), aggressiveVarSF.get()
                progressbar.step(20)
                load_models(xor(1,lang), xor(0, lang), xor(1,sm), xor(0,sm), sa, aa)
                progressbar.step(40)
                predictions = predict(sa, aa, lang, sm, text)
                progressbar.step(10)
                if(len(text) > 35):
                    text_label['text'] = (text[:35] + " (...)")
                else:
                    text_label['text'] = (text)
                progressbar.step(10)
                predictions_label['text'] = predictions
                progressbar.step(9)
            except:
                None
            progressbar.place_forget()
            
        # Method that parses a CSV and creates the button to view the results.
        def analyze_csv():
            global dictionary_csv_results, results_button_image
            dictionary_csv_results, path, column, lang = {'text':[],'Sentiment':[], 'Aggressive':[]}, textDirectory.get(), entry_column.get(), language_BF.get()
            
            # AUX: Method that analyzes a csv marked as English language.
            def predict_csv_eng():
                step = 100 / len(df) 
                for row in df[df.columns[int(column)]]:
                    dictionary_csv_results['text'].append(row)
                    if(lang == 0):
                        res = take_predict_tw(1,1,1, row, 'es').strip().split("\n")
                    elif(len(row) > 255):
                        res = take_predict_tw(1,1,1, row, 'en').strip().split("\n")
                    else:
                        res = take_predict_rd(1,1,1, row, True).strip().split("\n")
                    sentiment, aggressiveness = res[1], res[0]
                    dictionary_csv_results['Sentiment'].append(sentiment)
                    dictionary_csv_results['Aggressive'].append(aggressiveness)
                    progressbar.step(step)
                return dictionary_csv_results
            
            # AUX: Method that returns whether a file exists.
            def exist_file():
                return os.path.exists(path) and os.path.splitext(path)[1] == '.csv'
            
            # AUX: Method that returns that a row exists.
            def column_exist():
                return len(pd.read_csv(path).columns) > int(column)
            
            if(exist_file() and column_exist()):
                df = pd.read_csv(path)
                progressbar = ttk.Progressbar(self.home, style="red.Horizontal.TProgressbar")
                progressbar.place(x='770', y='765', width=100) 
                load_models(xor(1,lang), xor(0, lang), 1, 1, 1, 1)
                dictionary_csv_results = predict_csv_eng()
                csv_name = os.path.splitext(path)[0].split("/")
                csv_name = csv_name[len(csv_name)-1]
                df = pd.DataFrame.from_dict(dictionary_csv_results) 
                df.to_csv('analysis/' + csv_name +'_results.csv')
                progressbar.place_forget()
                create_table(self.home, dictionary_csv_results)
                results_button_image = PhotoImage(file=r'icons/results_button.png')
                Button(self.home, image=results_button_image, command= lambda: show_results(),border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='1280', y='780')
       
        # Home frames
        global explore_button_image, advanced_button_image, compute_button_image, settings_button_image, twitter_button_image, github_button_image, linkedin_button_image
        
        # Loading images
        settings_button_image = PhotoImage(file=r'icons/settings_button.png')
        twitter_button_image = PhotoImage(file=r'icons/twitter_logo.png')
        github_button_image = PhotoImage(file=r'icons/github_logo.png')
        linkedin_button_image = PhotoImage(file=r'icons/linkedin_logo.png')
        advanced_button_image = PhotoImage(file=r'icons/advanced_button.png')
        compute_button_image = PhotoImage(file=r'icons/compute_button.png')
        explore_button_image = PhotoImage(file=r'icons/explore_button.png')
    
        self.home = ttk.Frame(self, height=1440, width=900)
        ''' -------- FRAMES SETTINGS -------- '''
        # Home frames
        white_frame, gray_frame, light_gray_frame_up, light_gray_frame_down = Frame(self.home, bg='white', height=1440, width=900), Frame(self.home, bg='#949494', height=1060, width=720), Frame(self.home, bg='#E4E4E4', height=410, width=720), Frame(self.home, bg='#E4E4E4', height=410, width=720)
        white_frame.pack(fill='both', expand=True)
        gray_frame.place(x='0',y='0')
        light_gray_frame_up.place(x='735',y='0')
        light_gray_frame_down.place(x='735',y='435')

        ''' -------- LEFT FRAME -------- '''
        
        # Home text left
        home_title, label_title1 = Label(self.home, text='Welcome to Social Media Meter', bg='#949494', fg='white', font=('Helvetica 18 bold')), Label(self.home, text='It starts sentiment and aggressiveness analysis with BERT, trained on ~200k tweets \nand properly tuned. These models are suitable for English and Spanish.\n\n\nMore information on datasets and sources used can be found in the help\nsection.\n\n\n\nEnjoy!', bg='#949494', fg='white', font=('Helvetica 13'), justify=LEFT)
        home_title.place(x='135', y='57')
        label_title1.place(x='25', y='130')

        # Home text left    

        # Hyperlinks social media
        twitterButton = Button(self.home, image=twitter_button_image, border=0, bg='#949494', activebackground='#949494')
        twitterButton.place(x='608', y='760')
        twitterButton.bind("<Button-1>", lambda e: callback("https://twitter.com/WickedZequi"))
        githubButton = Button(self.home, image=github_button_image, border=0, bg='#949494', activebackground='#949494')
        githubButton.place(x='650', y='758')
        githubButton.bind("<Button-1>", lambda e: callback("https://github.com/ezepersos"))
        linkedinButton = Button(self.home, image=linkedin_button_image, border=0, bg='#949494', activebackground='#949494')
        linkedinButton.place(x='550', y='758')
        linkedinButton.bind("<Button-1>", lambda e: callback("https://www.linkedin.com/in/ezequiel-perez-b7015a18b/"))

        # Frame Buttons

        settingsButton = Button(self.home, image=settings_button_image, command =lambda: help_menu(), border=0, bg='#949494', activebackground='#949494')
        settingsButton.place(x='20', y='758')
        

        ''' -------- RIGHT-UPPER FRAME SETTINGS -------- '''

        Label(self.home, text='Quick text', bg='#E4E4E4', fg='black', font=(FONT_SE9), justify=LEFT).place(x='735', y='1')
        
        # Frame radio-check buttons
        language_UF = IntVar()
        Radiobutton(self.home,text='English', padx = 20,variable=language_UF,value=1, bg='#E4E4E4', activebackground='#E4E4E4').place(x='735', y='26')
        Radiobutton(self.home,text='Spanish', padx = 20,variable=language_UF,value=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='735', y='46')

        # Frame inputs
        phrase = ttk.Entry(self.home, font = (FONT_SE8))
        phrase.place(x='755', y='74', width=180, height=20)
        phrase.insert(0, 'Enter any Text ...')
        
        # Frame buttons


        Button(self.home, image=advanced_button_image, command = lambda: show_hide_frame(self.home.toggle), border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='945', y='68')
        Button(self.home, image=compute_button_image, command = lambda: threading.Thread(target=analyze_sentence).start(), border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='770', y='98')
        
        #TODO
        ''' -------- RIGHT-BOTTOM FRAME SETTINGS -------- '''
        # Frame label
        Label(self.home, text='CSV analysis', bg='#E4E4E4', fg='black', font=(FONT_SE9), justify=LEFT).place(x='735', y='435')
        Label(self.home, text='Column number:', bg='#E4E4E4', fg='black', font=(FONT_SE9), justify=LEFT).place(x='760', y='510')
        text_label = Label(self.home, textvariable='', fg='black', bg='#E4E4E4', font=(FONT_SE12), justify=LEFT)
        text_label.place(x='1000', y='350')
        predictions_label = Label(self.home, textvariable='', fg='black', bg='#E4E4E4', font=(FONT_SE12), justify=LEFT)
        predictions_label.place(x='1250', y='350')

        # Frame buttons
        Button(self.home, image=compute_button_image, command = lambda: threading.Thread(target=analyze_csv).start(), border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='770', y='565')
        Button(self.home, image=explore_button_image, command=lambda: upload_action(textDirectory),border=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='945', y='535')
       
        
        # Frame radio-check buttons
        language_BF = IntVar()
        Radiobutton(self.home,text='English', padx = 20,variable=language_BF,value=1, bg='#E4E4E4', activebackground='#E4E4E4').place(x='735', y='460')
        Radiobutton(self.home,text='Spanish', padx = 20,variable=language_BF,value=0, bg='#E4E4E4', activebackground='#E4E4E4').place(x='735', y='485')
        
        # Frame inputs
        textDirectory = StringVar()
        directory = ttk.Entry(self.home,textvariable=textDirectory, font = ('SegoeUI', 9))
        directory.place(x='755', y='540', width=180, height=20)
        entry_column = ttk.Entry(self.home, font = ('SegoeUI', 9), width=8)
        entry_column.place(x='875', y='510')
        
        ''' -------- FRAMES SETTINGS -------- '''
        # Home frames
        light_gray_frame = Frame(self.home, bg='#F9F9F9', height=135, width=240)  # this is the background
        

        # Frame label
        social_media_mode = Label(self.home, text='Social media mode:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT)
        analysis_type = Label(self.home, text='Analysis type:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT)

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
    
    # Window for real time analysis
    def realTime(self):

        #Method that starts a real time analysis, while is searching it updates the graphs. 
        def start_real_time_analysis():
            mapped_vars = {'RB':[sentimentVarSF.get(), aggressiveVarSF.get(), englishVarSF.get(), spanishVarSF.get(), twitterVarSF.get(), redditVarSF.get()],'EN': [entry_subreddit.get(), country_phrase.get(), entry_query.get()]}
            threading.Thread(target = update_table_real_time, args=[analysis, mapped_vars]).start()
            if(mapped_vars['RB'][4] + mapped_vars['RB'][5] >= 1):
                threading.Thread(target=put_realtime_graphs, args=[mapped_vars['RB'][0], mapped_vars['RB'][1],self.realTime]).start()
        
        #Method that hides and displays the advanced options of the real time search. 
        def show_hide_frame(toggle):
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
                toggle[13].place(x='130', y='240')
                toggle[14].place(x='130', y='260')
                toggle[12].place(x='1150', y='75')
                
        
        self.realTime = Frame(self, height=1440, width=900, bg="white")
        global start_rt_button_image, clear_rt_button_image, stop_rt_button_image, save_rt_button_image

        ''' -------- TABLE SETTINGS -------- '''
        
        # Label Frame Settings
        lb = LabelFrame(self.realTime, text='Analysis', bg='white', fg='black', width=1380, height=420, font=(FONT_SE9))
        lb.place(x='10', y='30')

         #Scroll settings 
        analysis_scroll = Scrollbar(lb)
        analysis_scroll.pack(side=RIGHT, fill=Y)

        #Table settings
        analysis = ttk.Treeview(lb,yscrollcommand=analysis_scroll.set, xscrollcommand =analysis_scroll.set)
        analysis.pack()
        analysis['columns'] = ('text', 'user_id', 'date', 'country', 'Platform','Results')
        analysis.column("#0", width=0,  stretch=NO)
        analysis.column("text",anchor=CENTER,width=600)
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
        clear_rt_button_image = PhotoImage(file=r'icons/clear_button.png')
        stop_rt_button_image = PhotoImage(file=r'icons/stop_button.png')
        save_rt_button_image = PhotoImage(file=r'icons/save_button.png')

        Button(self.realTime, image=start_rt_button_image, command = lambda: threading.Thread(target=start_real_time_analysis).start(), border=0, bg='white', activebackground='white').place(x='1200', y='5')
        Button(self.realTime, image=advanced_button_image, command = lambda: show_hide_frame(white_frame.toggle), border=0, bg='white', activebackground='white').place(x='1290', y='5')
        Button(self.realTime, image=clear_rt_button_image, command = lambda: analysis.delete(*analysis.get_children()), border=0, bg='white', activebackground='white').place(x='1290', y='480')
        Button(self.realTime, image=stop_rt_button_image, command = lambda: threading.Thread(target=stop_real_time_analysis).start(), border=0, bg='white', activebackground='white').place(x='1200', y='480')
        Button(self.realTime, image=save_rt_button_image, command = lambda: threading.Thread(target=export_results, args=[1]).start(), border=0, bg='white', activebackground='white').place(x='20', y='480')

        
        ''' -------- FRAMES SETTINGS -------- '''
        # Home frames
        Frame(self.realTime, bg='white', height=134, width=242, border=1)  # this is the background

        # Frame label
        Label(self.realTime, text='Social media mode:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT)
        Label(self.realTime, text='Analysis type:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT)

        """ ADVANCED """
        # Home frames
        white_frame = Frame(self.realTime, bg='white', height=285, width=220, highlightbackground="black", highlightthickness=1)
        
        # Frame label
        subreddit_label = Label(white_frame, text='SubReddit**:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT, background='white')
        country_label = Label(white_frame, text='*Country*:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT, background='white')
        query_label = Label(white_frame, text='Query:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT, background='white')
        reddit_adv_label = Label(white_frame, text='**Only for reddit', bg='#F9F9F9', fg='black', font=(FONT_SE8), justify=LEFT, background='white')
        twitter_adv_label = Label(white_frame, text='*Only for twitter', bg='#F9F9F9', fg='black', font=(FONT_SE8), justify=LEFT, background='white')
        
       
        #Entry
        entry_subreddit = ttk.Entry(white_frame, font = ('SegoeUI', 9))
        country_phrase = ttk.Combobox(white_frame,font = ('SegoeUI', 9), state="readonly", values=list(sorted(COORDINATES.keys())))
        
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
        white_frame.toggle = [subreddit_label, country_label, query_label, entry_subreddit, country_phrase, entry_query, sfCB, afCB, efCB, spCB, twCB, rdCB, white_frame, reddit_adv_label, twitter_adv_label]  
        return self.realTime

    # Window for customized analysis
    def customAnalysis(self):
        #Method that starts a custom analysis, checks that the input of the number of elements is correct and once the search is done, updates the graphs. 
        def start_custom_analysis():
            #after, before = time.mktime(datetime.datetime.strptime(str(start_date.get_date()),"%Y-%m-%d").timetuple()), time.mktime(datetime.datetime.strptime(str(end_date.get_date()),"%Y-%m-%d").timetuple())
            after, before = None, None
            mapped_vars = {'RB':[sentimentVarSF.get(), aggressiveVarSF.get(), englishVarSF.get(), spanishVarSF.get(), twitterVarSF.get(), redditVarSF.get()],'EN': [entry_subreddit.get(), country_phrase.get(), query_phrase.get(), numItems.get(), after, before]}
            num_items = str(mapped_vars['EN'][3])
            if num_items.isdigit():
                dictionary = update_table_custom(analysis, mapped_vars)
                put_custom_graphs(dictionary, mapped_vars['RB'][0], mapped_vars['RB'][1], self.customAnalysis)
            else:
                messagebox.showwarning("Input error", "Num items must be a number!")

        #Method that hides and displays the advanced options of the customized search. 
        def show_hide_frame(toggle):
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
                toggle[9].place(x='130', y='210')
                toggle[10].place(x='130', y='230')
                toggle[8].place(x='1150', y='75')
        
        self.customAnalysis = Frame(self, height=1440, width=900, bg="white")
        global start_ca_button_image, clear_cs_button_image, save_cs_button_image
        ''' -------- TABLE SETTINGS -------- '''
        # Label Frame Settings
        lb = LabelFrame(self.customAnalysis, text='Analysis', bg='white', fg='black', width=1380, height=420, font=(FONT_SE9))
        lb.place(x='10', y='30')

        #Scroll settings 
        analysis_scroll = Scrollbar(lb)
        analysis_scroll.pack(side=RIGHT, fill=Y)

        #Table settings
        analysis = ttk.Treeview(lb,yscrollcommand=analysis_scroll.set, xscrollcommand =analysis_scroll.set)
        analysis.pack()
        analysis['columns'] = ('text', 'user_id', 'date', 'country', 'Platform','Results')
        analysis.column("#0", width=0,  stretch=NO)
        analysis.column("text",anchor=CENTER,width=600)
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

   
        numItems = ttk.Entry(self.customAnalysis, font = ('SegoeUI', 9))
        numItems.place(x="720", y="10", width=100, height=20)
        query_phrase = ttk.Entry(self.customAnalysis, font = ('SegoeUI', 9))
        query_phrase.place(x='880', y='10', width=100, height=20)
        query_phrase.insert(0, '')
        country_phrase = ttk.Combobox(self.customAnalysis,font = ('SegoeUI', 9), state="readonly", values=list(sorted(COORDINATES.keys())))
        country_phrase.place(x='1050', y='10', width=100, height=20)
        #DateEntry
        #start_date = DateEntry(self.customAnalysis, width= 16, background= "gray", foreground= "black",bd=5)
        #end_date = DateEntry(self.customAnalysis, width= 16, background= "gray", foreground= "black",bd=5)
        #start_date.place(x='95', y='8')
        #end_date.place(x='295', y='8')
        #Labels 
        #Label(self.customAnalysis, text="Start Date", bg="white").place(x='25', y='8')
        #Label(self.customAnalysis, text="End Date", bg="white").place(x='225', y='8')
        Label(self.customAnalysis, text="Samples (N)", bg="white").place(x='640', y='8')
        Label(self.customAnalysis, text="Query", bg="white").place(x='830', y='8')
        Label(self.customAnalysis, text="Country", bg="white").place(x='990', y='8')
        
        # Buttons
        start_ca_button_image = PhotoImage(file=r'icons/start_button.png')
        clear_cs_button_image = PhotoImage(file=r'icons/clear_button.png')
        save_cs_button_image = PhotoImage(file=r'icons/save_button.png')

        Button(self.customAnalysis, image=start_ca_button_image, command = lambda: threading.Thread(target=start_custom_analysis).start(), border=0, bg='white', activebackground='white').place(x='1200', y='5')
        Button(self.customAnalysis, image=advanced_button_image, command = lambda: show_hide_frame(white_frame.toggle), border=0, bg='white', activebackground='white').place(x='1290', y='5')
        Button(self.customAnalysis, image=clear_cs_button_image, command = lambda: analysis.delete(*analysis.get_children()), border=0, bg='white', activebackground='white').place(x='1290', y='480')
        Button(self.customAnalysis, image=save_cs_button_image, command = lambda: threading.Thread(target=export_results, args=[0]).start(), border=0, bg='white', activebackground='white').place(x='20', y='480')

        """ ADVANCED """
        # Home frames
        white_frame = Frame(self.customAnalysis, bg='white', height=260, width=220, highlightbackground="black", highlightthickness=1)
        
        # Frame label
        subreddit_label = Label(white_frame, text='SubReddit**:', bg='#F9F9F9', fg='black', font=(FONT_SE9), justify=LEFT, background='white')
        reddit_adv_label = Label(white_frame, text='**Only for reddit', bg='#F9F9F9', fg='black', font=(FONT_SE8), justify=LEFT, background='white')
        twitter_adv_label = Label(white_frame, text='*Only for twitter', bg='#F9F9F9', fg='black', font=(FONT_SE8), justify=LEFT, background='white')
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
        white_frame.toggle = [subreddit_label, entry_subreddit, sfCB, afCB, efCB, spCB, twCB, rdCB, white_frame,reddit_adv_label,twitter_adv_label]  

        return self.customAnalysis
    
    #MAIN: method that starts the application by creating a parent window and adding a multi-tab notebook. 
    def __init__(self, main):
        # Auxiliary method that defines the styles of the application.
        def define_styles():
            style = ttk.Style()
            style.theme_create( "custom", parent="vista", settings={
            "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
            "TNotebook.Tab": {
                "configure": {"padding": [0, 0], "background": "green" },
                "map":       {"background": [("selected", "red")],
                            "expand": [("selected", [1, 1, 1, 0])] } } } )
            style.theme_use("custom")
            style.configure('Treeview', rowheight=40, bd=0, font=('Calibri', 11), bg="white")
            style.configure('TEntry', bordercolor='black')
            style.configure("red.Horizontal.TProgressbar", foreground='white', background='#00CCFF')
        
        super().__init__(main)
        define_styles()
        main.title('SM - Meter')
        ''' -------- GENERAL SETTINGS -------- '''
        # Window size
        main.resizable(0,0)
        main.geometry('1440x900')
        main.title('SM - Home')
        self.font = font.Font(weight='bold')

        # Create tab panel.
        self.notebook = ttk.Notebook(self, width=1440, height=900)
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

# Main method that calls the App class that starts the application.
if __name__ == '__main__':
    main = Tk()
    app = App(main)
    app.mainloop()

