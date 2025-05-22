import pandas as pd

""" KLASA STATYCZNA DO ZARZĄDZANIA PLIKIEM Z DANYMI """
class FileManager:
    """ NAZWA PLIKU Z DANYMI """
    FILENAME: str = "expenses.csv"

    """ METODA ODCZYTUJĄCA DANE Z PLIKU I ZWRACAJĄCA DATAFRAME """
    @staticmethod
    def read() -> pd.DataFrame:
        file_data = pd.read_csv(FileManager.FILENAME, sep=";")
        file_data["Data"] = pd.to_datetime(file_data["Data"])
        return file_data

    """ METODA DODAJĄCA NOWY WPIS NA KOŃCU PLIKU """
    @staticmethod
    def append(line: str) -> None:
        with open(FileManager.FILENAME, "a") as file:
            file.write(line)

    """ METODA MODYFIKUJĄCA ISTNIEJĄCY WPIS W PLIKU """
    @staticmethod
    def modify(original: str, modified: str) -> None:
        with open(FileManager.FILENAME, "r") as file:
            lines = file.readlines()

        with open(FileManager.FILENAME, "w") as file:
            for line in lines:
                if line == str(original):
                    file.write(modified)
                else:
                    file.write(line)

    """ METODA USUWAJĄCA PODANY WPIS Z PLIKU """
    @staticmethod
    def delete(line: str) -> None:
        FileManager.modify(original=line, modified="")