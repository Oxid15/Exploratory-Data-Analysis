import urllib

import tkinter as tk
import pandas as pd
from matplotlib import pyplot as plt
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import automap

class DBManager():

    def __init__(self):
        self.numerical_types = [
            'BIGINT',
            'INT',
            'int',
            'INTEGER',
            'SMALLINT',
            'DECIMAL',
            'FLOAT',
            'NUMERIC',
            'REAL',
            'float'
            ]

    #TODO add exception handling
    def collect_metadata(self):
        self.metadata = sa.MetaData()
        self.table_names = self.engine.table_names()

    #TODO replace default arguments with input boxes
    def connect(self):
        params = urllib.parse.quote_plus(r"DRIVER={SQL Server};SERVER=LAPTOP-OEGPUQVV\SQLEXPRESS;DATABASE=RUData;Trusted_Connection=yes")
        self.engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        self.conn = self.engine.connect()
        self.sessionmaker = sa.orm.sessionmaker(bind=self.engine)
        self.collect_metadata()

    def get_column_names(self, table_name):
        table = sa.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
        return table.columns.keys()

    def get_connection(self):
        return self.conn

    def get_table(self, table_name):
        return sa.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)

class DataManager():
    def connect(self):
        self.DBManager.connect()

    def get_table_names(self):
        return self.DBManager.table_names

    def get_column_names(self, table_name):
        return self.DBManager.get_column_names(table_name)

    def compute_averages(self, table_name):
        table = self.DBManager.get_table(table_name)
        connection = self.DBManager.get_connection()
        avgs = []
        for column in table.columns.values():
            if str(column.type) in self.DBManager.numerical_types:
                query = sa.select([sa.func.avg(column)])
                resproxy = connection.execute(query)
                avgs.append(resproxy.fetchall()[0][0])
            else:
                avgs.append(None)
        return avgs

    # def getSummaryInfo(self, table : pd.dataFrame):
    #     means = [column.mean() for column in table]
    #     stds = [column.std() for column in table]

class Presenter():
    def append_text_to_textbox(self, textbox, text):
        self.gui.append_text(textbox, text)
    
    def append_elem_to_list_box(self, listbox, elem):
        self.gui.append_elem(listbox, elem)

    def onConnect(self):
        #TODO exception handling here too
        self.DataManager.connect()
        table_names = self.DataManager.get_table_names()
        for table_name in table_names:
            self.append_elem_to_list_box(self.gui.left_listbox, table_name)

    # def create_string_table(self, data):
    #     pass

    def onSummary(self):
        table_names = self.DataManager.get_table_names()
        tableIdx = self.gui.left_listbox.curselection()
        if(len(tableIdx) == 1):
            col_names = self.DataManager.get_column_names(table_names[tableIdx[0]])
            col_avgs = self.DataManager.compute_averages(table_names[tableIdx[0]])

            tb = self.gui.main_textbox
            for name in col_names:
                self.gui.append_text(tb, name + '|')
            self.gui.append_text(tb, '\nmean:')
            for avg in col_avgs:
                self.gui.append_text(tb, str(avg) + ' | ')    

# class Plotting_manager():
#     def hists(self, table):
#        table.hist() #pd.DataFrame.hist()
    # def pairplot(self, table):
    #     sns.pairplot(table)

class GUI():
    def __init__(self):
        self.window = tk.Tk()

    def window_config(self):
        self.window.wm_title('Exploratory Data Analysis Program')

    def mainscreen(self):
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        self.right_frame = tk.Frame(self.window, relief='raised', borderwidth=1)
        self.right_frame.grid(column = 1, row = 0, sticky='nwes')
        self.right_frame.columnconfigure(0, weight=100)

        self.left_frame = tk.Frame(self.window, relief='raised', borderwidth=1)
        self.left_frame.grid(column = 0, row = 0, sticky='nwes')
        self.left_frame.columnconfigure(0, weight=100)

        self.main_textbox = tk.Text(self.right_frame, font='Consolas 9', wrap=tk.NONE)
        self.main_textbox.grid(column = 0, row = 0, sticky='wes')

        self.main_textbox_vscrollbar = tk.Scrollbar(self.window)
        self.main_textbox_vscrollbar.configure(command=self.main_textbox.yview)
        self.main_textbox_vscrollbar.grid(row=0, column=2, sticky='ns')

        self.main_textbox_hscrollbar = tk.Scrollbar(self.window, orient=tk.HORIZONTAL)
        self.main_textbox_hscrollbar.configure(command=self.main_textbox.xview)
        self.main_textbox_hscrollbar.grid(row=0, column=1, sticky='wes')

        self.left_listbox = tk.Listbox(self.left_frame, height=35)
        self.left_listbox.grid(column = 0, row = 0, sticky='nwe')

        self.left_listbox_scrollbar = tk.Scrollbar(self.left_frame)
        self.left_listbox_scrollbar.configure(command=self.left_listbox.yview)
        self.left_listbox_scrollbar.grid(row=0, column=0, sticky='nse')

        self.top_menu = tk.Menu(self.window)
        self.window.config(menu=self.top_menu)

        self.file_menu = tk.Menu(self.top_menu)
        self.top_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Connect to database", command = self.Presenter.onConnect)

        self.data_menu = tk.Menu(self.top_menu)
        self.top_menu.add_cascade(label="Data", menu=self.data_menu)
        self.data_menu.add_command(label="Summary", command=self.Presenter.onSummary)

    def mainloop(self):
        self.window_config()
        self.mainscreen()
        self.window.mainloop()
    
    def append_text(self, textbox, text):
        textbox.insert(tk.END, text)

    def append_elem(self, listbox, elem):
        listbox.insert(tk.END, elem)

def main():
    #initialize app objectcs
    dbm = DBManager()
    dm = DataManager()
    pr = Presenter()
    g = GUI()

    #connect objects to form MVP model
    g.Presenter = pr
    pr.gui = g
    pr.DataManager = dm
    dm.DBManager = dbm

    g.mainloop()

main()