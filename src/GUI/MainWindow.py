import tkinter as tk
import pandas as pd
from tkinter import ttk

from tkcalendar import DateEntry

from ExpCategory import ExpCategory
from GUI.NewExpense import NewExpense


def new_expense():
    NewExpense()



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file = None
        self.title("Kalkulator wydatków")
        self.geometry("700x500")
        self.resizable(width=False, height=False)


        expenses = tk.LabelFrame(self, borderwidth=0)
        expenses.pack(fill="both", padx=10, pady=10)
        ttk.Label(expenses, text="Lista wydatków", font="24").pack(padx=10, pady=10)

        self.reload_file()

        self.tree = ttk.Treeview(expenses)
        self.tree["columns"] = list(self.file.columns)
        self.tree["show"] = "headings"
        widths = (100, 100, 150, 250)
        for col, width in zip(self.file.columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        self.refresh_tree()

        new_exp_btn = ttk.Button(expenses, text="Nowy wydatek", command=new_expense)
        new_exp_btn.pack()

        filters = tk.LabelFrame(self, borderwidth=0)
        filters.pack(fill="both", padx=10, pady=10)

        filters.columnconfigure(list(range(0,8)), weight=1, uniform="Silent_Creme")
        ttk.Label(filters, text="Filtry", font="24").grid(columnspan=8, padx=10, pady=10)

        ttk.Radiobutton(filters, text="Zakres dat", value="range").grid(column=0, row=1)
        ttk.Label(filters, text="Data od:").grid(column=0, row=2)
        self.date_from = DateEntry(filters, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date_from.delete(0, "end")
        self.date_from.grid(column=1, row=2)

        ttk.Label(filters, text="Data do:").grid(column=2, row=2)
        self.date_to = DateEntry(filters, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date_to.delete(0, "end")
        self.date_to.grid(column=3, row=2)

        ttk.Label(filters, text="Kategoria").grid(column=0, row=3)
        self.category = ttk.Combobox(filters, values=[cat.value for cat in ExpCategory])
        self.category.grid(column=1, row=3)

        search_btn = ttk.Button(filters, text="Szukaj",
                                command=lambda: self.search(date_from=self.date_from.get(),
                                                            date_to=self.date_to.get(),
                                                            category=self.category.get()))
        search_btn.grid(column=0, row=9)
        clear_btn = ttk.Button(filters, text="Wyczyść filtry", command=self.clear_filters)
        clear_btn.grid(column=1, row=9)

        self.mainloop()

    def reload_file(self):
        self.file = pd.read_csv("expenses.csv", sep=";", date_format="%yyyy-%MM-%dd")
        self.file.sort_values(by=["Data"], ascending=False, inplace=True)
    
    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for _, row in self.file.iterrows():
            values = list(row)
            values[2] = ExpCategory[values[2]]
            self.tree.insert("", tk.END, values=values)
        self.tree.pack(fill="both", padx=10, pady=10)

    def search(self, date_from=None, date_to=None, category=None, day=None, month=None, year=None):
        self.reload_file()
        if not date_from is None and date_to is None:
            self.file = self.file[(self.file.Data >= date_from) & (self.file.Data <= date_to)]
        if category is not None:
            self.file = self.file[self.file.Kategoria == ExpCategory(category).name]
        self.refresh_tree()

    def clear_filters(self):
        self.reload_file()
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")
        self.category.delete(0, "end")
        self.refresh_tree()