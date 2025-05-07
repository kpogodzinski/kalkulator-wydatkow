import calendar
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkcalendar import DateEntry

from ExpCategory import ExpCategory
from Expense import Expense
from GUI.EditExpense import EditExpense

MONTHS = ["", "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
                "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        """ USTAWIENIA OKNA """
        self.file = pd.read_csv("expenses.csv", sep=";", date_format="%yyyy-%MM-%dd")
        self.title("Kalkulator wydatków")
        self.geometry("700x600")
        self.resizable(width=False, height=False)

        """ RAMKA Z DANYMI """
        expenses_frame = tk.LabelFrame(self, borderwidth=0)
        expenses_frame.pack(fill="both", padx=10, pady=10)
        ttk.Label(expenses_frame, text="Lista wydatków", font="24").pack(padx=10, pady=5)
        self.reload_file()

        """ TABELKA Z WYDATKAMI """
        self.tree = ttk.Treeview(expenses_frame, selectmode="browse")
        self.tree["columns"] = list(self.file.columns)
        self.tree["show"] = "headings"
        widths = (100, 100, 150, 250)

        for col, width in zip(self.file.columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        scroll = ttk.Scrollbar(expenses_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.refresh_tree()

        new_exp_btn = ttk.Button(expenses_frame, text="Nowy wydatek", command=self.new_expense)
        new_exp_btn.pack(side="left", padx=10, pady=5)

        modify_exp_btn = ttk.Button(expenses_frame, text="Edytuj wydatek", command=self.edit_expense)
        modify_exp_btn.pack(side="left", padx=10, pady=5)

        """ RAMKA Z FILTRAMI """
        filters_frame = tk.LabelFrame(self, borderwidth=0)
        filters_frame.pack(fill="both", padx=10, pady=10)
        ttk.Label(filters_frame, text="Filtry", font="24").pack(anchor='w', padx=10, pady=5)

        """ FILTR WG KATEGORII """
        cat_frame = tk.Frame(filters_frame)
        ttk.Label(cat_frame, text="Kategoria:")
        self.category = ttk.Combobox(cat_frame, values=[cat.value for cat in ExpCategory])

        for child in cat_frame.winfo_children():
            child.pack(side="left", padx=5, pady=5)

        cat_frame.pack(anchor="w")

        """ FILTR WG ROKU/MIESIĄCA/DNIA """
        self.date_type = tk.StringVar()
        self.date_frame = tk.Frame(filters_frame)
        default_radio = ttk.Radiobutton(self.date_frame, text="Data", value="date", variable=self.date_type, command=self.radio_select)

        ttk.Label(self.date_frame, text="Rok:")
        self.__year_var = tk.StringVar()
        self.year = ttk.Combobox(self.date_frame, width=6, values=self.get_years(), textvariable=self.__year_var)
        self.__year_var.trace_add("write", self.update_days)

        ttk.Label(self.date_frame, text="Miesiąc:")
        self.__month_var = tk.StringVar()
        self.month = ttk.Combobox(self.date_frame, width=10, values=self.get_months(), textvariable=self.__month_var)
        self.__month_var.trace_add("write", self.update_days)

        ttk.Label(self.date_frame, text="Dzień:")
        self.day = ttk.Combobox(self.date_frame, width=3, values=self.get_days())

        for child in self.date_frame.winfo_children():
            if type(child) == ttk.Radiobutton:
                child.pack(anchor="w", padx=5, pady=5)
            else:
                child.pack(side="left", padx=5, pady=5)

        self.date_frame.pack(anchor="w")

        """ FILTR WG ZAKRESU DAT """
        self.range_frame = tk.Frame(filters_frame)
        ttk.Radiobutton(self.range_frame, text="Zakres dat", value="range", variable=self.date_type, command=self.radio_select)

        ttk.Label(self.range_frame, text="Data od:")
        self.date_from = DateEntry(self.range_frame, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date_from.delete(0, "end")

        ttk.Label(self.range_frame, text="Data do:")
        self.date_to = DateEntry(self.range_frame, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date_to.delete(0, "end")

        for child in self.range_frame.winfo_children():
            if type(child) == ttk.Radiobutton:
                child.pack(anchor="w", padx=5, pady=5)
            else:
                child.pack(side="left", padx=5, pady=5)

        self.range_frame.pack(anchor="w")

        """ PRZYCISKI DO FILTROWANIA """
        search_btn = ttk.Button(filters_frame, text="Szukaj",
                                command=lambda: self.search(date_from=self.date_from.get(),
                                                            date_to=self.date_to.get(),
                                                            category=self.category.get(),
                                                            year=self.year.get(),
                                                            month = self.month.get(),
                                                            day=self.day.get()))
        search_btn.pack(side="left", padx=5, pady=5)
        clear_btn = ttk.Button(filters_frame, text="Wyczyść filtry", command=self.clear_filters)
        clear_btn.pack(side="left", padx=5, pady=5)

        default_radio.invoke()
        self.mainloop()

    def new_expense(self):
        EditExpense(master=self, on_close=self.on_edit_close)

    def edit_expense(self):
        try:
            expense = self.get_expense_from_tree()
            EditExpense(master=self, on_close=self.on_edit_close, expense=expense)
        except IndexError as e:
            print(e)

    def on_edit_close(self):
        self.reload_file()
        self.refresh_tree()

    def reload_file(self):
        self.file = pd.read_csv("expenses.csv", sep=";", date_format="%yyyy-%MM-%dd")
        self.file.sort_values(by=["Data"], ascending=False, inplace=True)
    
    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for _, row in self.file.iterrows():
            values = list(row)
            values[2] = str(ExpCategory[values[2]])
            self.tree.insert("", tk.END, values=values)
        self.tree.pack(fill="both", padx=10, pady=10)

    def get_expense_from_tree(self):
        selected = self.tree.focus()
        entry = self.tree.item(selected)["values"]
        expense = Expense(date=entry[0], amount=entry[1], category=ExpCategory(entry[2]).name, notes=entry[3])
        return expense

    def search(self, date_from=None, date_to=None, category=None, year=None, month=None, day=None):
        self.reload_file()

        if year != "":
            if month != "":
                m = MONTHS.index(month)
                month = str(m) if m > 9 else f"0{m}"
                if day != "":
                    day = day if int(day) > 9 else f"0{day}"
                    self.file = self.file[self.file.Data == f"{year}-{month}-{day}"]
                else:
                    self.file = self.file[self.file.Data.str[:-3] == f"{year}-{month}"]
            else:
                self.file = self.file[self.file.Data.str[:4] == f"{year}"]

        if date_from != "" and date_to != "":
            self.file = self.file[(self.file.Data >= date_from) & (self.file.Data <= date_to)]

        if category != "":
            self.file = self.file[self.file.Kategoria == ExpCategory(category).name]
        self.refresh_tree()

    def clear_day(self):
        self.day.delete(0, "end")
        self.month.delete(0, "end")
        self.year.delete(0, "end")

    def clear_range(self):
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")

    def clear_filters(self):
        self.reload_file()
        self.clear_day()
        self.clear_range()
        self.category.delete(0, "end")
        self.refresh_tree()

    def get_years(self):
        years = set()
        for child in self.tree.get_children():
            date = self.tree.item(child, "values")[0]
            date_split = date.split("-")
            years.add(date_split[0])
        return list(years)

    def get_months(self):
        return MONTHS[1:]

    def get_days(self):
        try:
            days = calendar.monthrange(int(self.year.get()), MONTHS.index(self.month.get()))
        except ValueError as e:
            print(e)
            return [str(i) for i in range(1, 32)]
        return [str(i) for i in range(1, days[1]+1)]

    def update_days(self, *args):
        self.day["values"] = self.get_days()

    def radio_select(self):
        if self.date_type.get() == "date":
            for child in self.date_frame.winfo_children():
                child["state"] = tk.ACTIVE
            for child in self.range_frame.winfo_children():
                if type(child) != ttk.Radiobutton:
                    self.clear_range()
                    child["state"] = tk.DISABLED

        elif self.date_type.get() == "range":
            for child in self.date_frame.winfo_children():
                if type(child) != ttk.Radiobutton:
                    self.clear_day()
                    child["state"] = tk.DISABLED
            for child in self.range_frame.winfo_children():
                child["state"] = tk.ACTIVE