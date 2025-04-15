import tkinter as tk
import pandas as pd
from tkinter import ttk
from GUI.NewExpense import NewExpense


def new_expense():
    NewExpense()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator wydatków")
        self.geometry("700x500")
        self.resizable(width=False, height=False)

        ttk.Label(self, text="Lista wydatków", font="24").pack()

        file = pd.read_csv("expenses.csv", sep=";", date_format="%yyyy-%MM-%dd")
        expenses_list = ttk.Treeview(self)
        expenses_list["columns"] = list(file.columns)
        expenses_list["show"] = "headings"
        widths = (100, 100, 150, 250)
        for col, width in zip(file.columns, widths):
            expenses_list.heading(col, text=col)
            expenses_list.column(col, width=width)

        for _, row in file.iterrows():
            expenses_list.insert("", tk.END, values=list(row))

        expenses_list.pack()


        new_exp_btn = ttk.Button(self, text="Nowy wydatek", command=new_expense)
        new_exp_btn.pack()
        self.mainloop()


