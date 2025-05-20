from enum import Enum

""" ENUMERATOR DLA SKRÓCONYCH NAZW KATEGORII """
class ExpCategory(Enum):
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Kultura i rozrywka"
    SHOPPING = "Codzienne zakupy"
    FOOD = "Jedzenie poza domem"
    EDUCATION = "Edukacja"
    HEALTH = "Zdrowie i uroda"
    HOUSING = "Opłaty mieszkaniowe"
    OTHER = "Inne wydatki"

    def __str__(self):
        return self.value