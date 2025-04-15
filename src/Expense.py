import datetime
import ExpCategory

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
        return f"{self.date};{self.amount};{self.category};{self.notes}"

