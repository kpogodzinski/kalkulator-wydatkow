import tkinter as tk
from tkinter import ttk
from collections import Counter

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ExpCategory import ExpCategory


class StatsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Statystyki")
        self.geometry("800x500")
        self.resizable(False, False)

        """ RAMKA ZE STATYSTYKAMI """
        stats_frame = tk.LabelFrame(self, text="Statystyki opisowe", borderwidth=1)
        stats_frame.pack(side="left", fill="y", padx=10, pady=10)

        """ ODCZYT PLIKU """
        file = pd.read_csv("expenses.csv", sep=";")
        file["Data"] = pd.to_datetime(file["Data"])

        """ OBLICZENIE STATYSTYK """
        expenses_count = file["Kwota"].count()
        expenses_sum = file["Kwota"].sum()

        days = (file["Data"].max() - file["Data"].min()).days + 1
        daily_avg = round(expenses_sum / days, 2)

        expense_max = max(file["Kwota"])
        cat_counter = Counter(file["Kategoria"])
        most_common_cat = max(cat_counter, key=cat_counter.get)

        """ ETYKIETY ZE STATYSTYKAMI """
        ttk.Label(stats_frame, text=f"Liczba wydatków: {expenses_count}")
        ttk.Label(stats_frame, text=f"Suma wydatków: {expenses_sum}")
        ttk.Label(stats_frame, text=f"Średnia dzienna: {daily_avg}")
        ttk.Label(stats_frame, text=f"Największy wydatek: {expense_max}")
        ttk.Label(stats_frame, text=f"Najczęstsza kategoria: {ExpCategory[most_common_cat]}")

        for child in stats_frame.winfo_children():
            child["font"] = tk.font.Font(size=10)
            child.pack(anchor="w", padx=5, pady=5)

        """ RAMKA Z WYKRESAMI """
        charts_frame = tk.LabelFrame(self, text="Wykresy", borderwidth=1)
        charts_frame.pack(side="right", fill="both", expand=1, padx=10, pady=10)

        """ ZAKŁADKI DLA WYKRESÓW """
        tabs_widget = ttk.Notebook(charts_frame)
        piechart_tab = ttk.Frame(tabs_widget)

        tabs_widget.add(piechart_tab, text="Rozkład kategorii")
        tabs_widget.pack(fill="both", padx=5, pady=5)

        """ WYKRES KOŁOWY """
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.pie(cat_counter.values(),
               labels=[str(ExpCategory[label]) for label in cat_counter.keys()],
               autopct="%1.1f%%",
               textprops={"size": "small"},
               shadow=True
        )
        ax.set_title("Rozkład kategorii")
        ax.axis="equal"

        canvas = FigureCanvasTkAgg(fig, master=piechart_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


