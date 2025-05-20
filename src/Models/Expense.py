import datetime
import ExpCategory

""" KLASA REPREZENTUJĄCA OBIEKT WYDATKU """
class Expense:
    def __init__(self,
                date: datetime.date,
                amount: float,
                category: ExpCategory,
                notes: str):
        self.date = date
        self.amount = amount
        self.category = category
        self.notes = notes

    def __str__(self):
        return f"{self.date};{float(self.amount):.2f};{self.category};{self.notes}\n"