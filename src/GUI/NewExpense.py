import tkinter as tk
from calendar import firstweekday
from tkinter import ttk
from tkcalendar import DateEntry

from ExpCategory import ExpCategory
from Expense import Expense


class NewExpense(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nowy wydatek")
        self.geometry("300x400")
        self.resizable(False, False)

        ttk.Label(self, text="Data").grid(column=0, row=1)
        date = DateEntry(self, date_pattern="dd.MM.YYYY", firstweekday="monday")
        date.grid(column=1, row=1)

        ttk.Label(self, text="Kwota").grid(column=0, row=0)
        amount = ttk.Entry(self)
        amount.grid(column=1, row=0)

        ttk.Label(self, text="Kategoria").grid(column=0, row=2)
        category = ttk.Combobox(self, values=[cat.value for cat in ExpCategory])
        category.grid(column=1, row=2)

        ttk.Label(self, text="Uwagi").grid(column=0, row=3)
        notes = ttk.Entry(self)
        notes.grid(column=1, row=3)

        ttk.Button(self, text="Dodaj",
                   default="active",
                   command=lambda: self.add_expense(amount.get(), date.get(), category.get(), notes.get())
                   ).grid(column=5, row=5)
        self.mainloop()

    def add_expense(self, amount, date, category, notes):
        expense = Expense(amount, date, category, notes)
        print(expense)
