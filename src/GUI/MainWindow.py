import calendar
import tkinter as tk

from typing import Optional, List
from tkinter import ttk
from tkinter import messagebox as mb

from pandas import DataFrame
from tkcalendar import DateEntry

from FileManager import FileManager
from Models.Expense import Expense
from ExpCategory import ExpCategory
from GUI.EditExpenseWindow import EditExpenseWindow
from GUI.StatsWindow import StatsWindow

""" TABLICA NAZW MIESIĘCY """
MONTHS = ["", "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
                "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

""" KLASA GŁÓWNEGO OKNA APLIKACJI """
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        """ USTAWIENIA OKNA """
        self.title("Kalkulator wydatków")
        self.geometry("700x600")
        self.resizable(width=False, height=False)

        """ RAMKA Z DANYMI """
        self.expenses_frame = tk.Frame(self)
        self.expenses_frame.pack(fill="both", padx=10, pady=10)
        ttk.Label(self.expenses_frame, text="Lista wydatków", font="24").pack(padx=10, pady=5)

        self.dataframe: Optional[DataFrame] = None
        self.sort_state: dict[Optional[str], Optional[str]] = {"column": None, "direction": None}
        self.reload_file()

        """ TABELKA Z WYDATKAMI """
        self.tree = ttk.Treeview(self.expenses_frame, selectmode="browse")
        self.tree["columns"] = list(self.dataframe.columns)
        self.tree["show"] = "headings"
        widths = (100, 100, 150, 250)

        for col, width in zip(self.dataframe.columns, widths):
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col))
            self.tree.column(col, width=width)

        """ SCROLLBAR DO TABELKI """
        scroll = ttk.Scrollbar(self.expenses_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.refresh_tree()

        """ PRZYCISKI DO ZARZĄDZANIA WYDATKAMI ORAZ DO OTWARCIA STATYSTYK """
        new_exp_btn = ttk.Button(self.expenses_frame, text="Nowy wydatek", command=self.new_expense)
        new_exp_btn.pack(side="left", padx=10, pady=5)

        modify_exp_btn = ttk.Button(self.expenses_frame, text="Edytuj wydatek", command=self.edit_expense)
        modify_exp_btn.pack(side="left", padx=10, pady=5)

        delete_exp_btn = ttk.Button(self.expenses_frame, text="Usuń wydatek", command=self.delete_expense)
        delete_exp_btn.pack(side="left", padx=10, pady=5)

        stats_btn = ttk.Button(self.expenses_frame, text="Statystyki", command=self.open_stats)
        stats_btn.pack(side="right", padx=10, pady=5)

        """ RAMKA Z FILTRAMI """
        self.filters_frame = tk.Frame(self)
        self.filters_frame.pack(fill="both", padx=10, pady=10)
        ttk.Label(self.filters_frame, text="Filtry", font="24").pack(anchor='w', padx=10, pady=5)

        """ FILTR WG KATEGORII """
        self.cat_frame = tk.Frame(self.filters_frame)
        ttk.Label(self.cat_frame, text="Kategoria:")
        self.category = ttk.Combobox(self.cat_frame, values=[cat.value for cat in ExpCategory])

        for child in self.cat_frame.winfo_children():
            child.pack(side="left", padx=5, pady=5)

        self.cat_frame.pack(anchor="w")

        """ FILTR WG ROKU/MIESIĄCA/DNIA """
        self.date_type = tk.StringVar()
        self.date_frame = tk.Frame(self.filters_frame)
        default_radio = ttk.Radiobutton(self.date_frame, text="Data", value="date",
                                        variable=self.date_type, command=self.radio_select)

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
        self.range_frame = tk.Frame(self.filters_frame)
        ttk.Radiobutton(self.range_frame, text="Zakres dat", value="range",
                        variable=self.date_type, command=self.radio_select)

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
        search_btn = ttk.Button(self.filters_frame, text="Szukaj",
                                command=lambda: self.search(date_from=self.date_from.get(),
                                                            date_to=self.date_to.get(),
                                                            category=self.category.get(),
                                                            year=self.year.get(),
                                                            month = self.month.get(),
                                                            day=self.day.get()))
        search_btn.pack(side="left", padx=5, pady=5)
        clear_btn = ttk.Button(self.filters_frame, text="Wyczyść filtry", command=self.clear_filters)
        clear_btn.pack(side="left", padx=5, pady=5)

        default_radio.invoke()
        self.mainloop()

    """ METODA DO OTWARCIA OKNA DODAWANIA WYDATKU """
    def new_expense(self) -> None:
        child = EditExpenseWindow(master=self, on_close=self.on_edit_close)
        child.grab_set()
        self.wait_window(child)

    """ METODA DO OTWARCIA OKNA EDYCJI WYDATKU """
    def edit_expense(self) -> None:
        try:
            expense = self.get_expense_from_tree()
            child = EditExpenseWindow(master=self, on_close=self.on_edit_close, expense=expense)
            child.grab_set()
            self.wait_window(child)
        except IndexError as e:
            print(f"ERROR -- edit_expense: {e}")

    """ METODA DO USUWANIA WYDATKU """
    def delete_expense(self) -> None:
        try:
            expense = self.get_expense_from_tree()
            confirmed = mb.askquestion(title="Potwierdzenie", message="Czy na pewno chcesz usunąć wskazany wydatek?")
            if confirmed == "no":
                return
            FileManager.delete(str(expense))
            self.reload_file()
            self.refresh_tree()
        except IndexError as e:
            print(f"ERROR -- delete_expense: {e}")

    """ METODA OTWIERAJĄCA OKNO ZE STATYSTYKAMI """
    def open_stats(self) -> None:
        child = StatsWindow(master=self)
        child.grab_set()
        self.wait_window(child)

    """ METODA WYWOŁYWANA PO ZAMKNIĘCIU OKNA DODAWANIA/EDYCJI """
    def on_edit_close(self) -> None:
        self.reload_file()
        self.refresh_tree()

    """ METODA ŁADUJĄCA DANE Z PLIKU """
    def reload_file(self) -> None:
        self.dataframe = FileManager.read()

        if self.sort_state["column"] and self.sort_state["direction"]:
            ascending = self.sort_state["direction"] == "asc"
            self.dataframe.sort_values(by=self.sort_state["column"], ascending=ascending, inplace=True)
        else:
            self.dataframe.sort_values(by=["Data"], ascending=False, inplace=True)

    """ METODA ODŚWIEŻAJĄCA DANE W TABELI """
    def refresh_tree(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for _, row in self.dataframe.iterrows():
            values = list(row)
            values[0] = values[0].strftime("%Y-%m-%d")
            values[2] = str(ExpCategory[values[2]])
            self.tree.insert("", tk.END, values=values)
        self.tree.pack(fill="both", padx=10, pady=10)

    """ METODA SORTUJĄCA DANE W TABELI WG KOLUMNY """
    def sort_by_column(self, col) -> None:
        current = self.sort_state

        if current["column"] == col:
            if current["direction"] is None:
                current["direction"] = "asc"
            elif current["direction"] == "asc":
                current["direction"] = "desc"
            else:
                current["direction"] = None
                current["column"] = None
        else:
            current["column"] = col
            current["direction"] = "asc"

        if current["direction"] is None:
            self.reload_file()
        else:
            ascending = current["direction"] == "asc"
            self.dataframe.sort_values(by=col, ascending=ascending, inplace=True)

        self.refresh_tree()

        for heading in self.tree["columns"]:
            label = heading
            if heading == current["column"]:
                arrow = {"asc": "▲", "desc": "▼"}.get(current["direction"], "")
                label += f" {arrow}"
            self.tree.heading(heading, text=label, command=lambda _col=heading: self.sort_by_column(_col))

    """ METODA ZWRACAJĄCA OBIEKT EXPENSE Z ZAZNACZONEGO WIERSZA W TABELI """
    def get_expense_from_tree(self) -> Expense:
        selected = self.tree.focus()
        entry = self.tree.item(selected)["values"]
        expense = Expense(date=entry[0], amount=entry[1], category=ExpCategory(entry[2]).name, notes=entry[3])
        return expense

    """ METODA WYSZUKUJĄCA WYDATKI SPEŁNIAJĄCE USTAWIONE FILTRY """
    def search(self, date_from=None, date_to=None,
               category=None, year=None, month=None, day=None) -> None:
        self.reload_file()

        if year != "":
            if month != "":
                m = MONTHS.index(month)
                month = str(m) if m > 9 else f"0{m}"
                if day != "":
                    day = day if int(day) > 9 else f"0{day}"
                    self.dataframe = self.dataframe[(self.dataframe["Data"].dt.year == int(year)) &
                                                    (self.dataframe["Data"].dt.month == int(month)) &
                                                    (self.dataframe["Data"].dt.day == int(day))]
                else:
                    self.dataframe = self.dataframe[(self.dataframe["Data"].dt.year == int(year)) &
                                                    (self.dataframe["Data"].dt.month == int(month))]
            else:
                self.dataframe = self.dataframe[self.dataframe["Data"].dt.year == int(year)]

        if date_from != "" and date_to != "":
            self.dataframe = self.dataframe[(self.dataframe["Data"] >= date_from) & (self.dataframe["Data"] <= date_to)]

        if category != "":
            self.dataframe = self.dataframe[self.dataframe["Kategoria"] == ExpCategory(category).name]
        self.refresh_tree()

    """ METODA CZYSZCZĄCA POLA W FILTRACH PO DACIE """
    def clear_day(self) -> None:
        self.day.delete(0, "end")
        self.month.delete(0, "end")
        self.year.delete(0, "end")

    """ METODA CZYSZCZĄCA POLA W FILTRACH PO ZAKRESIE DAT """
    def clear_range(self) -> None:
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")

    """ METODA CZYSZCZĄCA WSZYSTKIE FILTRY """
    def clear_filters(self) -> None:
        self.reload_file()
        self.clear_day()
        self.clear_range()
        self.category.delete(0, "end")
        self.refresh_tree()

    """ METODA ZWRACAJĄCA LISTĘ LAT ZNAJDUJĄCYCH SIĘ W DANYCH """
    def get_years(self) -> List[str]:
        years = set()
        for child in self.tree.get_children():
            date = self.tree.item(child, "values")[0]
            date_split = date.split("-")
            years.add(date_split[0])
        return sorted(list(years))

    """ METODA ZWRACAJĄCA LISTĘ NAZW MIESIĘCY """
    def get_months(self) -> List[str]:
        return MONTHS[1:]

    """ METODA ZWRACAJĄCA LISTĘ DNI MIESIĄCA W ZALEŻNOŚCI OD MIESIĄCA I ROKU """
    def get_days(self) -> List[str]:
        try:
            days = calendar.monthrange(int(self.year.get()), MONTHS.index(self.month.get()))
        except ValueError as e:
            print(f"ERROR -- get_days: {e}; Returning default range: [1;31]")
            return [str(i) for i in range(1, 32)]
        return [str(i) for i in range(1, days[1]+1)]

    """ METODA AKTUALIZUJĄCA LISTĘ DNI MIESIĄCA W COMBOBOXIE PO WYBRANIU ROKU LUB MIESIĄCA """
    def update_days(self, *args) -> None:
        self.day["values"] = self.get_days()

    """ METODA OBSŁUGUJĄCA ZMIANĘ WYBORU RADIOBUTTONA """
    def radio_select(self) -> None:
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