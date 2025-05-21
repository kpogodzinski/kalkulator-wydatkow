import tkinter as tk

from tkinter import ttk
from tkcalendar import DateEntry

from ExpCategory import ExpCategory
from FileManager import FileManager
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
            self.title("Edycja wydatku")
        self.geometry("300x300")
        self.resizable(False, False)

        """ RAMKA-KONTENER DLA ELEMENTÓW """
        self.container = tk.Frame(self)
        if expense is None:
            ttk.Label(self.container, text="Nowy wydatek", font="24").pack(padx=10, pady=10)
        else:
            ttk.Label(self.container, text="Edycja wydatku", font="24").pack(padx=10, pady=10)

        """ ETYKIETY I POLA DO WYPEŁNIENIA SZCZEGÓŁÓW WYDATKU """
        self.date_frame = tk.Frame(self.container)
        ttk.Label(self.date_frame, text="Data:", width=10).pack(side="left", padx=5, pady=5)
        self.date = DateEntry(self.date_frame, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date.pack(side="left", padx=5, pady=5)

        self.amount_frame = tk.Frame(self.container)
        ttk.Label(self.amount_frame, text="Kwota:", width=10).pack(side="left", padx=5, pady=5)
        self.amount = ttk.Entry(self.amount_frame, width=10)
        self.amount.pack(side="left", padx=5, pady=5)
        ttk.Label(self.amount_frame, text="zł").pack(side="left")

        self.category_frame = tk.Frame(self.container)
        ttk.Label(self.category_frame, text="Kategoria:", width=10).pack(side="left", padx=5, pady=5)
        self.category = ttk.Combobox(self.category_frame, values=[cat.value for cat in ExpCategory])
        self.category.pack(side="left", padx=5, pady=5)

        self.notes_frame = tk.Frame(self.container)
        ttk.Label(self.notes_frame, text="Uwagi:", width=10).pack(side="left", padx=5, pady=5)
        self.notes = ttk.Entry(self.notes_frame, width=50)
        self.notes.pack(side="left", padx=5, pady=5)

        """ WYPEŁNIENIE PÓL W PRZYPADKU EDYTOWANIA ISTNIEJĄCEGO WYDATKU """
        if expense:
            self.date.set_date(expense.date)
            self.amount.insert(0, expense.amount)
            self.category.insert(0, str(ExpCategory[expense.category]))
            self.notes.insert(0, expense.notes)

        """ PRZYCISK DO ZAPISANIA WYDATKU """
        self.button = ttk.Button(self.container,
                                 default="active",
                                 command=lambda: self.save_expense(self.date.get(), self.amount.get(),
                                                                   self.category.get(), self.notes.get()))
        if expense is None:
            self.button["text"] = "Dodaj"
        else:
            self.button["text"] = "Zapisz"

        """ ZAPAKOWANIE PRZYGOTOWANYCH ELEMENTÓW DO KONTENERA """
        for child in self.container.winfo_children()[1:]:
            child.pack(anchor='w', padx=5, pady=5)
        self.button.pack(side="right", padx=5, pady=5)

        self.container.pack(fill="both", expand=True, padx=10, pady=10)

    """ METODA ZAPISUJĄCA WYDATEK """
    def save_expense(self, date, amount, category, notes) -> None:
        amount = amount.replace(",", ".")
        new_expense = Expense(date=date, amount=amount, category=ExpCategory(category).name, notes=notes)

        if self.expense is None:
            FileManager.append(str(new_expense))
        else:
            FileManager.modify(original=str(self.expense), modified=str(new_expense))

        self.on_close()
        self.destroy()