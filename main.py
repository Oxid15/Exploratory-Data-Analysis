import tkinter as tk
import pandas as pd
import sqlalchemy as sa
from matplotlib import pyplot as plt

# class db():
#     pass

# class dbManager():
#     def connect(self, file):
#         pass

#     def getTable(self):
#         pass

class dataManager():
    # def getData(self, table):
    #     pass

    def getSummaryInfo(self, table):
        pass

class presenter():
    def appendTextToGUI(self, textBox, text):
        self.gui.appendText(textBox, text)
    
    def onSummary(self):
        tableIdx = self.gui.leftListBox.curselection()
        if(len(tableIdx) > 0):
            # table = self.dbManager.tables[tableIdx[0]]
            # info = self.dataManager.getSummaryInfo(table)
            #
            self.appendTextToGUI(self.gui.mainTextBox, 'Example')

# class plottingManager():
#     pass

class gui():
    def __init__(self):
        self.window = tk.Tk()

    def WindowConfig(self):
        self.window.wm_title('Exploratory Data Analysis Program')

    def mainScreen(self):
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        self.rightFrame = tk.Frame(self.window, relief='raised', borderwidth=1)
        self.rightFrame.grid(column = 1, row = 0, sticky='nwes')
        self.rightFrame.columnconfigure(0, weight=100)

        self.leftFrame = tk.Frame(self.window, relief='raised', borderwidth=1)
        self.leftFrame.grid(column = 0, row = 0, sticky='nwes')
        self.leftFrame.columnconfigure(0, weight=100)

        self.mainTextBox = tk.Text(self.rightFrame, font='Consolas')
        self.mainTextBox.grid(column = 0, row = 0, sticky='nwes')

        self.mainTextBoxScrB = tk.Scrollbar(self.window)
        self.mainTextBoxScrB.configure(command=self.mainTextBox.yview)
        self.mainTextBoxScrB.grid(row=0, column=2, sticky='ns')

        self.leftListBox = tk.Listbox(self.leftFrame, height=1)
        self.leftListBox.grid(column = 0, row = 0, sticky='nwe')

        self.topMenu = tk.Menu(self.window)
        self.window.config(menu=self.topMenu)

        self.fileMenu = tk.Menu(self.topMenu)
        self.topMenu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Connect to database")#, command = self.presenter.onConnect)

        self.dataMenu = tk.Menu(self.topMenu)
        self.topMenu.add_cascade(label="Data", menu=self.dataMenu)
        self.dataMenu.add_command(label="Summary", command=self.presenter.onSummary)

    def mainloop(self):
        self.WindowConfig()
        self.mainScreen()
        ################## DEBUG CODE
        self.leftListBox.insert(tk.END, 'Table One')
        ################## DEBUG CODE
        self.window.mainloop()
    
    def appendText(self, textBox, text):
        textBox.insert(tk.END, text)

def main():
    dm = dataManager()
    pr = presenter()
    g = gui()
    g.presenter = pr
    pr.gui = g
    pr.dataManager = dm
    g.mainloop()

main()