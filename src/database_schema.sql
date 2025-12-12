-- PROJEKT: System Oceny Ryzyka Kredytowego
-- PLIK: database_schema.sql
-- OPIS: Struktura tabel dla systemu decyzyjnego (PostgreSQL / Standard SQL)

-- 1. Tabela Klientów
-- Przechowuje dane demograficzne potrzebne do weryfikacji tożsamości.
CREATE TABLE klienci (
  id_klienta SERIAL PRIMARY KEY NOT NULL,
  imie VARCHAR(50) NOT NULL,
  nazwisko VARCHAR(50) NOT NULL,
  pesel CHAR(11) NOT NULL UNIQUE CHECK (LENGTH(pesel) = 11),
  ulica VARCHAR(100),
  numer_domu VARCHAR(20) NOT NULL,
  kod_pocztowy VARCHAR(10) NOT NULL,
  miasto VARCHAR(50) NOT NULL,
  miesieczny_dochod DECIMAL(10, 2) NOT NULL,
  zatrudnienie_typ VARCHAR(50) NOT NULL
);

-- 2. Tabela Wniosków
-- Loguje każdą prośbę wzięcia kredytu przez klienta.
CREATE TABLE wnioski (
  id_wniosku SERIAL PRIMARY KEY NOT NULL,
  id_klienta INT NOT NULL,
  kwota_kredytu DECIMAL(10, 2) NOT NULL CHECK (kwota_kredytu > 0),
  ilosc_rat INT NOT NULL CHECK (ilosc_rat > 0),
  data_zlozenia TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  FOREIGN KEY (id_klienta) REFERENCES klienci(id_klienta)
  );

-- 3. Tabela Decyzji Systemowych
-- Tu zapisywany jest wynik działania algorytmu (logika z diagramu BPMN)
CREATE TABLE decyzje_systemowe (
  id_decyzji SERIAL PRIMARY KEY NOT NULL,
  id_wniosku INT NOT NULL,
  status_bik VARCHAR(20) NOT NULL,
  wyliczony_scoring INT NOT NULL,
  decyzja_koncowa VARCHAR(20) NOT NULL,
  data_decyzji TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_wniosku) REFERENCES wnioski(id_wniosku)
  );
