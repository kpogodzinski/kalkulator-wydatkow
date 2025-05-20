import tkinter as tk

from tkinter import ttk
from tkcalendar import DateEntry

from ExpCategory import ExpCategory
from Models.Expense import Expense

""" KLASA OKIENKA EDYCJI WYDATKU """
class EditExpenseWindow(tk.Toplevel):
    def __init__(self, master=None, on_close=None, expense=None):
        super().__init__(master)
        self.expense = expense
        self.on_close = on_close

        """ USTAWIENIA OKNA """
        if expense is None:
            self.title("Nowy wydatek")
        else:
            self.title("Edytuj wydatek")
        self.geometry("300x400")
        self.resizable(False, False)

        """ RAMKA-KONTENER DLA ELEMENTÓW """
        self.container = tk.Frame(self)

        """ ETYKIETY I POLA DO WYPEŁNIENIA SZCZEGÓŁÓW WYDATKU """
        ttk.Label(self.container, text="Data:")
        self.date = DateEntry(self.container, date_pattern="YYYY-MM-dd", firstweekday="monday")

        ttk.Label(self.container, text="Kwota:")
        self.amount = ttk.Entry(self.container)

        ttk.Label(self.container, text="Kategoria:")
        self.category = ttk.Combobox(self.container, values=[cat.value for cat in ExpCategory])

        ttk.Label(self.container, text="Uwagi:")
        self.notes = ttk.Entry(self.container)

        """ WYPEŁNIENIE PÓL W PRZYPADKU EDYTOWANIA ISTNIEJĄCEGO WYDATKU """
        if expense:
            self.date.set_date(expense.date)
            self.amount.insert(0, expense.amount)
            self.category.insert(0, str(ExpCategory[expense.category]))
            self.notes.insert(0, expense.notes)

        """ PRZYCISK DO ZAPISANIA WYDATKU """
        button = ttk.Button(self.container, default="active",
                   command=lambda: self.save_expense(self.date.get(), self.amount.get(),
                                                     self.category.get(), self.notes.get()))
        if expense is None:
            button["text"] = "Dodaj"
        else:
            button["text"] = "Zapisz"

        """ ZAPAKOWANIE PRZYGOTOWANYCH ELEMENTÓW DO KONTENERA """
        for child in self.container.winfo_children():
            if type(child) == ttk.Button:
                child.pack(anchor='e', padx=5, pady=5)
            else:
                child.pack(anchor='w', padx=5, pady=5)
        self.container.pack(fill='x', padx=10, pady=10)

    """ METODA ZAPISUJĄCA WYDATEK """
    def save_expense(self, date, amount, category, notes):
        new_expense = Expense(date=date, amount=amount, category=ExpCategory(category).name, notes=notes)
        if self.expense is None:
            self.__append_to_file__(new_expense)
        else:
            self.__modify_entry_in_file__(new_expense)

        self.on_close()
        self.destroy()

    """ METODA DOPISUJĄCA WPIS NA KOŃCU PLIKU """
    def __append_to_file__(self, expense):
        file = open("expenses.csv", "a")
        file.write(str(expense))
        file.close()

    """ METODA MODYFIKUJĄCA ISTNIEJĄCY WPIS W PLIKU """
    def __modify_entry_in_file__(self, expense):
        with open("expenses.csv", "r") as file:
            lines = file.readlines()

        with open("expenses.csv", "w") as file:
            for line in lines:
                if line == str(self.expense):
                    file.write(str(expense))
                else:
                    file.write(line)