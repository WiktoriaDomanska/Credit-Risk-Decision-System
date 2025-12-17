import sqlite3
import random
import pandas as pd
from datetime import datetime

# Konfiguracja
DB_NAME = "system_kredytowy.db"
RAPORT_FILE = "raport_analityczny.csv"

# Funkcje pomocnicze (generator danych)
def generate_pesel(year_range_start = 1950, year_range_end = 2000):
    """Generuje losowy, poprawny semantycznie numer PESEL (bez sumy kontrolnej dla uproszczenia)."""
    year = random.randint(year_range_start, year_range_end)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    # Formatowanie roku i miesiąca dla numeru PESEL
    y_str = str(year)[2:]
    if year >= 2000:
        m_str = f"{month + 20:02}"
    else:
        m_str = f"{month:02}"
    d_str = f"{day:02}"

    random_part = f"{random.randint(1000, 99999)}"
    return f"{y_str}{m_str}{d_str}{random_part}"

def calculate_age_from_pesel(pesel):
    """"Wyciąga rok urodzenia z numeru PESEL i liczy wiek."""
    year_prefix = int(pesel[0:2])
    month = int(pesel[2:4])

    current_year = datetime.now().year

    if month > 20: # osoby urodzone po 2000 roku
        birth_year = 2000 + year_prefix
    else:
        birth_year = 1900 + year_prefix

    return current_year - birth_year

# Logika biznesowa (Silnik Ryzyka)
def calculate_scoring(age, income, employment_type, bik_status):
    """
    Algorytm punktowy (zgodny z BPMN):
    Start: 0 pkt
    Wiek: 25-50 lat (+20 pkt)
    Dochód: > 5000 (+50 pkt), > 10000 (+100 pkt)
    Zatrudnienie: B2B/Umowa o pracę (+50 pkt)
    BIK: Negatywny (-1000 pkt - dyskwalifikacja)
    """
    points = 0

    # Wiek
    if 25 <= age <= 50:
        points += 20

    # Dochód
    if income > 10000:
        points += 100
    elif income > 5000:
        points += 50

    # Zatrudnienie
    if employment_type in ['Umowa o pracę', 'B2B']:
        points += 50

    # BIK
    if bik_status == 'NEGATYWNY':
        points -= 1000
    else:
        points += 100

    return points

# Główny program
def main():
    print("Uruchamianie systemu kredytowego")

    # Połączenie z bazą danych
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tworzenie tabel
    cursor.executescript("""
    DROP TABLE IF EXISTS decyzje_systemowe;
    DROP TABLE IF EXISTS wnioski;
    DROP TABLE IF EXISTS klienci;

    CREATE TABLE klienci (
        id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
        imie VARCHAR(50),
        nazwisko CHAR(50),
        pesel CHAR(11),
        ulica VARCHAR(100),
        numer_domu VARCHAR(20),
        kod_pocztowy VARCHAR(10),
        miasto VARCHAR(50),
        miesieczny_dochod DECIMAL(10, 2),
        zatrudnienie_typ VARCHAR(50)
    );

    CREATE TABLE wnioski (
        id_wniosku INTEGER PRIMARY KEY AUTOINCREMENT,
        id_klienta INT,
        kwota_kredytu DECIMAL(10, 2),
        ilosc_rat INT,
        data_zlozenia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_klienta) REFERENCES klienci(id_klienta)
    );

    CREATE TABLE decyzje_systemowe (
        id_decyzji INTEGER PRIMARY KEY AUTOINCREMENT,
        id_wniosku INT,
        status_bik VARCHAR(20),
        wyliczony_scoring INT,
        decyzja_koncowa VARCHAR(20),
        data_decyzji TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_wniosku) REFERENCES wnioski(id_wniosku)
    );
    """)
    print("Utworzono bazę danych i tabele.")

    # Symulacja - generowanie 100 wniosków
    imiona = ["Anna", "Jan", "Piotr", "Katarzyna", "Michał", "Maria", "Paweł", "Agnieszka"]
    nazwiska = ["Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński"]
    miasta = ["Warszawa", "Kraków", "Wrocław", "Poznań", "Gdańsk", "Częstochowa"]
    typy_umowy = ["Umowa o prace", "B2B", "Umowa Zlecenie", "Bezrobotny"]

    print("Przetwarzanie wniosków.")

    for _ in range(100):
        # Dane klienta
        imie = random.choice(imiona)
        nazwisko = random.choice(nazwiska)
        pesel = generate_pesel()
        dochod = random.randint(2000, 15000)
        umowa = random.choice(typy_umowy)
        miasto = random.choice(miasta)

        # Insert klient
        cursor.execute("""
            INSERT INTO klienci (imie, nazwisko, pesel, ulica, numer_domu, kod_pocztowy, miasto, miesieczny_dochod, zatrudnienie_typ)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (imie, nazwisko, pesel, "Polna", str(random.randint(1, 100)), "00-001", miasto, dochod, umowa))

        id_klienta = cursor.lastrowid

        # Dane wniosku
        kwota = random.randint(1000, 100000)
        raty = random.randint(6, 48)

        # Insert wniosek
        cursor.execute("""
            INSERT INTO wnioski (id_klienta, kwota_kredytu, ilosc_rat)
            VALUES (?, ?, ?)
        """, (id_klienta, kwota, raty))

        id_wniosku = cursor.lastrowid

        # Silnik Ryzyka

        # Pobranie danych potrzebnych do decyzji
        wiek = calculate_age_from_pesel(pesel)

        # Symulacja BIK (losowo 15% ludzi ma negatywny status BIK)
        status_bik = "NEGATYWNY" if random.random() < 0.15 else "OK"

        # Obliczenie Scoringu
        score = calculate_scoring(wiek, dochod, umowa, status_bik)

        # Decyzja
        decyzja = "PRZYZNANO" if score > 200 else "ODMOWA"

        # Insert decyzja
        cursor.execute("""
            INSERT INTO decyzje_systemowe (id_wniosku, status_bik, wyliczony_scoring, decyzja_koncowa)
            VALUES (?, ?, ?, ?)
        """, (id_wniosku, status_bik, score, decyzja))

    conn.commit()
    print("Przetworzono 100 klientów.")
    
    # Eksport wyników do Excela/CSV
    query = """
    SELECT
        k.imie, k.nazwisko, k.pesel, k.miesieczny_dochod, k.zatrudnienie_typ, w.kwota_kredytu, d.status_bik, d.wyliczony_scoring, d.decyzja_koncowa
    FROM decyzje_systemowe d
    JOIN wnioski w ON d.id_wniosku = w.id_wniosku
    JOIN klienci k ON w.id_klienta = k.id_klienta
    """
    
    df = pd.read_sql_query(query, conn)
    df.to_csv(RAPORT_FILE, index=False)
    print(f"Raport zapisany do pliku: {RAPORT_FILE}")
    print("\nPrzykładowe wyniki:")
    print(df.head(10))
    
    conn.close()

if __name__ == "__main__":
  main()
