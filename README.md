# Kalkulator wydatków
Prosty program do zarządzania wydatkami z graficznym interfejsem użytkownika, napisany w języku Python.

Program przystosowany do uruchamiania w systemie Windows. Nie był testowany na systemach Linux.

## Wymagania
Wymagane pakiety zostały umieszczone w pliku _requirements.txt_. Są to:
- `numpy 2.1.3`,
- `pandas 2.2.3`,
- `seaborn 0.13.2`,
- `matplotlib 3.10.1`,
- `tkcalendar 1.6.1`.

## Przygotowanie i instalacja
Sklonuj repozytorium i przejdź do folderu projektu:
```bash
git clone https://github.com/kpogodzinski/kalkulator-wydatkow.git
cd kalkulator-wydatkow
```

W folderze z projektem utwórz środowisko wirtualne:
```bash
python -m venv .venv
```

Aktywuj utworzone środowisko:
```bash
.venv\Scripts\activate
```

Zainstaluj potrzebne pakiety:
```bash
pip install -r requirements.txt
```

## Uruchamianie
Znajdując się w głównym folderze projektu, uruchom plik _main.py_:
```bash
python main.py
```

## Problemy
Jeśli program nie uruchamia się z powodu braku Tcl, upewnij się, że masz zainstalowaną bibliotekę Tcl/Tk w Pythonie.

Jeśli błąd występuje nadal, dodaj do systemu zmienną środowiskową TCL_LIBRARY ze ścieżką wskazującą na folder z biblioteką, np. `C:\Program Files\Python313\tcl\tcl8.6`