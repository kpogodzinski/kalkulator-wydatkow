import tkinter as tk
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
        cols = ("Data", "Kwota", "Kategoria", "Uwagi")
        widths = (100, 100, 150, 250)
        expenses_list = ttk.Treeview(self, columns=cols, show="headings")
        for col, width in zip(cols, widths):
            expenses_list.heading(col, text=col)
            expenses_list.column(col, width=width)
        expenses_list.pack()

        new_exp_btn = ttk.Button(self, text="Nowy wydatek", command=new_expense)
        new_exp_btn.pack()
        self.mainloop()


