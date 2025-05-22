import tkinter as tk

from tkinter import ttk
from typing import Dict, Any

from tkcalendar import DateEntry
from datetime import datetime
from collections import Counter

import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ExpCategory import ExpCategory
from FileManager import FileManager

""" KLASA OKNA ZE STATYSTYKAMI """
class StatsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        """ USTAWIENIA OKNA """
        self.title("Statystyki")
        self.geometry("1000x600")
        self.resizable(False, False)

        """ RAMKA ZE STATYSTYKAMI """
        self.stats_frame = tk.LabelFrame(self, text="Statystyki opisowe", borderwidth=1)
        self.stats_frame.pack(side="left", fill="y", padx=10, pady=10)

        """ ODCZYT PLIKU """
        self.dataframe = FileManager.read()

        """ OBLICZENIE STATYSTYK """
        self.stats = self.compute_stats()
        most_common_cat = max(self.stats["cat_counter"], key=self.stats["cat_counter"].get)

        """ ETYKIETY ZE STATYSTYKAMI """
        ttk.Label(self.stats_frame, text=f"Liczba wydatków: {self.stats["expenses_count"]}")
        ttk.Label(self.stats_frame, text=f"Suma wydatków: {self.stats["expenses_sum"]:.2f} zł")
        ttk.Label(self.stats_frame, text=f"Średnia dzienna: {self.stats["daily_avg"]:.2f} zł")
        ttk.Label(self.stats_frame, text=f"Najmniejszy wydatek: {self.stats["expense_min"]:.2f} zł")
        ttk.Label(self.stats_frame, text=f"Największy wydatek: {self.stats["expense_max"]:.2f} zł")
        ttk.Label(self.stats_frame, text=f"Najczęstsza kategoria: {ExpCategory[most_common_cat]}")

        """ ZAPAKOWANIE PRZYGOTOWANYCH ETYKIET DO RAMKI """
        for child in self.stats_frame.winfo_children():
            child["font"] = tk.font.Font(size=12)
            child.pack(anchor="w", padx=10, pady=10)

        """ RAMKA Z WYKRESAMI """
        self.charts_frame = tk.LabelFrame(self, text="Wykresy", borderwidth=1)
        self.charts_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        """ ZAKŁADKI DLA WYKRESÓW """
        self.tabs_widget = ttk.Notebook(self.charts_frame)

        self.piechart_tab = ttk.Frame(self.tabs_widget)
        self.tabs_widget.add(self.piechart_tab, text="Rozkład kategorii")

        self.barplot_tab = ttk.Frame(self.tabs_widget)
        self.date_select_frame = ttk.Frame(self.barplot_tab)
        self.tabs_widget.add(self.barplot_tab, text="Wydatki z okresu")

        self.histplot_tab = ttk.Frame(self.tabs_widget)
        self.tabs_widget.add(self.histplot_tab, text="Wydawane kwoty")

        self.tabs_widget.pack(fill="both", padx=5, pady=5)

        """ WYKRES KOŁOWY """
        self.draw_piechart()

        """ WYBÓR ZAKRESU DAT DLA WYKRESU SŁUPKOWEGO """
        ttk.Label(self.date_select_frame, text="Data od:")
        self.date_from = DateEntry(self.date_select_frame, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date_from.set_date(datetime.today() - pd.DateOffset(months=2))
        self.date_from.bind("<<DateEntrySelected>>", self.on_date_change)

        ttk.Label(self.date_select_frame, text="Data do:")
        self.date_to = DateEntry(self.date_select_frame, date_pattern="YYYY-MM-dd", firstweekday="monday")
        self.date_to.set_date(datetime.today())
        self.date_to.bind("<<DateEntrySelected>>", self.on_date_change)

        for child in self.date_select_frame.winfo_children():
            child.pack(side="left", padx=5, pady=5)

        """ WYKRES SŁUPKOWY """
        self.date_select_frame.pack()
        self.draw_barplot()

        """ HISTOGRAM """
        self.draw_histplot()

    """ METODA OBLICZAJĄCA WYBRANE STATYSTYKI OPISOWE """
    def compute_stats(self) -> Dict[str, Any]:
        stats = {"expenses_count": self.dataframe["Kwota"].count(),
                 "expenses_sum": round(self.dataframe["Kwota"].sum(), 2)}

        days = (self.dataframe["Data"].max() - self.dataframe["Data"].min()).days + 1
        stats["daily_avg"] = round(stats["expenses_sum"] / days, 2)

        stats["expense_min"] = self.dataframe["Kwota"].min()
        stats["expense_max"] = self.dataframe["Kwota"].max()
        stats["cat_counter"] = Counter(self.dataframe["Kategoria"])

        return stats

    """ METODA RYSUJĄCA WYKRES KOŁOWY """
    def draw_piechart(self) -> None:
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.pie(self.stats["cat_counter"].values(),
               labels=[str(ExpCategory[label]) for label in self.stats["cat_counter"].keys()],
               autopct="%1.1f%%",
               shadow=True
               )
        ax.set_title("Procentowy udział kategorii wydatków")
        ax.axis("equal")

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.piechart_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    """ METODA RYSUJĄCA WYKRES SŁUPKOWY """
    def draw_barplot(self) -> None:
        filtered_data = self.dataframe[(self.dataframe["Data"] >= self.date_from.get()) &
                                       (self.dataframe["Data"] <= self.date_to.get())].copy()
        filtered_data = filtered_data.groupby(["Data"])["Kwota"].sum().reset_index()

        fig = Figure(figsize=(6, 5))
        ax = fig.add_subplot(1, 1, 1)

        sns.barplot(filtered_data, x="Data", y="Kwota", ax=ax)
        ax.bar_label(ax.containers[0], fontsize=8)
        ax.set_title("Dzienna suma wydatków z zadanego okresu")
        ax.set_xlabel("Data")
        ax.set_ylabel("Kwota")
        ax.tick_params(axis="x", rotation=80)
        ax.grid(True, which="major", axis="both", linestyle="--", alpha=0.7)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.barplot_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    """ METODA AKTUALIZUJĄCA WYKRES SŁUPKOWY PO ZMIANIE ZAKRESU DAT """
    def on_date_change(self, event) -> None:
        for child in self.barplot_tab.winfo_children():
            if isinstance(child, tk.Canvas):
                child.destroy()
                break
        self.draw_barplot()

    """ METODA RYSUJĄCA HISTOGRAM """
    def draw_histplot(self) -> None:
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(1, 1, 1)

        max_amount = self.dataframe["Kwota"].max()
        upper_limit = max_amount + (50 - max_amount%50 + 1)
        bins = np.arange(0, upper_limit, 50)
        sns.histplot(self.dataframe["Kwota"], color="magenta", ax=ax, bins=bins, kde=True)
        ax.set_xticks(bins)
        ax.tick_params(axis="x", rotation=30)
        ax.set_xlim(-25, upper_limit+25)
        ax.set_title("Rozkład wydatków wg kwoty")
        ax.set_xlabel("Kwota")
        ax.set_ylabel("Liczba wydatków")

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.histplot_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)