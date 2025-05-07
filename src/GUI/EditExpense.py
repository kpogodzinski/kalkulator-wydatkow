import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry

from ExpCategory import ExpCategory
from Expense import Expense


class EditExpense(tk.Toplevel):
    def __init__(self, master=None, on_close=None, expense=None):
        super().__init__(master)
        self.expense = expense
        self.on_close = on_close

        if expense is None:
            self.title("Nowy wydatek")
        else:
            self.title("Edytuj wydatek")
        self.geometry("300x400")
        self.resizable(False, False)

        container = tk.Frame(self)

        ttk.Label(container, text="Data:")
        date = DateEntry(container, date_pattern="YYYY-MM-dd", firstweekday="monday")

        ttk.Label(container, text="Kwota:")
        amount = ttk.Entry(container)

        ttk.Label(container, text="Kategoria:")
        category = ttk.Combobox(container, values=[cat.value for cat in ExpCategory])

        ttk.Label(container, text="Uwagi:")
        notes = ttk.Entry(container)

        if expense:
            date.set_date(expense.date)
            amount.insert(0, expense.amount)
            category.insert(0, str(ExpCategory[expense.category]))
            notes.insert(0, expense.notes)

        button = ttk.Button(container, default="active",
                   command=lambda: self.save_expense(date.get(), amount.get(), category.get(), notes.get()))
        if expense is None:
            button["text"] = "Dodaj"
        else:
            button["text"] = "Zapisz"

        for child in container.winfo_children():
            if type(child) == ttk.Button:
                child.pack(anchor='e', padx=5, pady=5)
            else:
                child.pack(anchor='w', padx=5, pady=5)
        container.pack(fill='x', padx=10, pady=10)

    def save_expense(self, date, amount, category, notes):
        new_expense = Expense(date=date, amount=amount, category=ExpCategory(category).name, notes=notes)
        if self.expense is None:
            self.__append_to_file__(new_expense)
        else:
            self.__modify_entry_in_file__(new_expense)

        self.on_close()
        self.destroy()

    def __append_to_file__(self, expense):
        file = open("expenses.csv", "a")
        file.write(str(expense))
        file.close()

    def __modify_entry_in_file__(self, expense):
        with open("expenses.csv", "r") as file:
            lines = file.readlines()

        with open("expenses.csv", "w") as file:
            for line in lines:
                if line == str(self.expense):
                    file.write(str(expense))
                else:
                    file.write(line)