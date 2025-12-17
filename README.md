# System Oceny Ryzyka Kredytowego (Credit Risk Decision System)

> **Status:** Projekt Ukończony (Completed)

Projekt hybrydowy łączący **Analizę Systemową** z **Data Science**. Celem było zaprojektowanie pełnego procesu kredytowego (od wymagań biznesowych po architekturę techniczną) oraz implementacja symulatora, który automatycznie ocenia zdolność kredytową klienta na podstawie zdefiniowanych reguł.

## Zakres projektu
Projekt demonstruje kompetencje w trzech kluczowych obszarach:

1.  **Analiza Systemowa & Procesowa:**
    * Model procesu biznesowego (**BPMN**) – wizualizacja ścieżki od złożenia wniosku do decyzji.
    * Projekt architektury (**UML Sequence**) – techniczny projekt komunikacji REST API i zapytań SQL.
    * Projekt bazy danych (**ERD**) – struktura tabel dla klienta, wniosków i decyzji.

2.  **Inżynieria Danych & Python:**
    * Stworzenie silnika decyzyjnego w **Pythonie**.
    * Implementacja algorytmu scoringowego.
    * Generowanie syntetycznych danych (100+ wniosków) i praca z bazą **SQLite**.

3.  **Raportowanie:**
    * Automatyczny eksport wyników decyzyjnych do formatu **CSV/Excel**.

## Logika Biznesowa (Algorytm Scoringowy)
System podejmuje decyzje na podstawie punktacji. Wniosek jest akceptowany po przekroczeniu **200 punktów**.

| Kryterium | Zasada | Punkty |
| :--- | :--- | :--- |
| **BIK** | Status NEGATYWNY | **-1000 (Odrzucenie)** |
| **Wiek** | 25 - 50 lat | +20 pkt |
| **Dochód** | > 5000 PLN | +50 pkt |
| **Dochód** | > 10000 PLN | +100 pkt |
| **Zatrudnienie** | UoP lub B2B | +50 pkt |

## Technologie
* **Analiza:** BPMN 2.0, UML, SQL, Lucidchart
* **Kod:** Python 3.12 (Biblioteki: `sqlite3`, `pandas`, `random`, `datetime`)
* **Baza Danych:** SQLite (wbudowana)

## Struktura Repozytorium
* `/docs` – Dokumentacja wizualna (Diagramy BPMN, UML, Schematy).
* `/src` – Kod źródłowy aplikacji (plik `main.py`).
* `/sql` – Skrypty tworzące strukturę bazy danych.
* `raport_analityczny.csv` – Wynik działania systemu (dane do analizy).

## Uruchamianie projektu
Wymagany zainstalowany Python.

1.  Pobranie repozytorium.
2.  Instalacja biblioteki pandas:
    ```bash
    pip install pandas
    ```
3.  Uruchomienie skryptu głównego:
    ```bash
    python src/main.py
    ```
4.  System utworzy plik bazy danych `system_kredytowy.db` oraz wygeneruje raport `raport_analityczny.csv`.
