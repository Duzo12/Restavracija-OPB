#NEK DRUG COMMIT 3
# uvozimo ustrezne podatke za povezavo
from . import auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv

testna_sprem = 7
def ustvari_tabelo_zaposleni():
    cur.execute("""
        CREATE TABLE zaposleni (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            telefon TEXT NOT NULL,
            placa INTEGER NOT NULL,
            rojstvo DATE NOT NULL
        );
    """) #morda bi pri telefon dodal unique, DATE se vstavlja v obliki 'YYYY-MM-DD'
    conn.commit()

def pobrisi_tabelo_zaposleni():
    cur.execute("""
        DROP TABLE zaposleni;
    """)
    conn.commit()

def uvozi_podatke_zaposleni():
    cur.execute( """
        INSERT INTO zaposleni (ime, priimek, telefon, placa, rojstvo) VALUES ('Nejc', 'Duscak', '070 256 331', '1500', '1998-01-07');
        INSERT INTO zaposleni (ime, priimek, telefon, placa, rojstvo) VALUES ('Maks', 'Perbil', '040 456 133', '1200', '1998-02-12');
        INSERT INTO zaposleni (ime, priimek, telefon, placa, rojstvo) VALUES ('Jan', 'Črne', '031 262 381', '1200', '1997-04-30');
    """)
    conn.commit()

def ustvari_tabelo_narocniki():
    cur.execute("""
        CREATE TABLE narocniki (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            kraj TEXT NOT NULL,
            naslov TEXT NOT NULL,
            telefon TEXT UNIQUE NOT NULL,
            uporabnisko_ime TEXT UNIQUE NOT NULL,
            geslo1 TEXT NOT NULL,
            geslo2 TEXT NOT NULL
        );
    """)
    conn.commit()

def pobrisi_tabelo_narocniki():
    cur.execute("""
        DROP TABLE narocniki;
    """)
    conn.commit()

def uvozi_podatke_narocniki():
    cur.execute( """
        INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, uporabnisko_ime, geslo1, geslo2) VALUES ('Nejc', 'Duscak', 'Ljubljana', 'Ulica 1', '070 256 331', 'nd', 'geslo', 'geslo');
        INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, uporabnisko_ime, geslo1, geslo2) VALUES ('Jan', 'Črne', 'Litija', 'Ulica 2', '031 262 381', 'jc', 'geslo', 'geslo');
        INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, uporabnisko_ime, geslo1, geslo2) VALUES ('Maks', 'Perbil', 'Vrhnika', 'Ulica 3', '040 456 133', 'mp', 'geslo', 'geslo');
    """)
    conn.commit()

def ustvari_tabelo_ponudba():
    cur.execute("""
        CREATE TABLE ponudba (
            id SERIAL PRIMARY KEY,
            vrsta TEXT NOT NULL,
            cena INTEGER NOT NULL,
            zaloga INTEGER NOT NULL
        );
    """)
    conn.commit()
    
def pobrisi_tabelo_ponudba():
    cur.execute("""
        DROP TABLE ponudba;
    """)
    conn.commit()

def uvozi_podatke_ponudba():
    cur.execute("""
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Hamburger', 6, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Pizza', 8, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Čevapčiči', 7, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Pommes Frittes', 2, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Kebab', 3, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Burek', 2, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Taquitosi', 4, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Pohan piščanec', 7, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Sladoled', 3, 4);
    """)
    conn.commit()

def ustvari_tabelo_narocila():
    cur.execute("""
        CREATE TABLE narocila (
            id SERIAL PRIMARY KEY,
            uporabnisko_ime TEXT NOT NULL,
            vrsta TEXT NOT NULL,
            datum DATE NOT NULL,
            kolicina INTEGER NOT NULL,
            cena INTEGER NOT NULL
        );
    """)
    conn.commit()
#ni na php
#se datumi

# def uvozi_podatke():
#     with open("podatki/obcine.csv", encoding="UTF-8") as f:
#         rd = csv.reader(f)
#         next(rd) # izpusti naslovno vrstico
#         for r in rd:
#             r = [None if x in ('', '-') else x for x in r]
#             cur.execute("""
#                 INSERT INTO obcina
#                 (ime, povrsina, prebivalstvo, gostota, naselja,
#                 ustanovitev, pokrajina, stat_regija, odcepitev)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 RETURNING id
#             """, r)
#             rid, = cur.fetchone()
#             print("Uvožena občina %s z ID-jem %d" % (r[0], rid))
#     conn.commit()

# def prebivalci(stevilo):
#     cur.execute("""
#         SELECT ime, prebivalstvo, ustanovitev FROM obcina
#         WHERE prebivalstvo >= %s
#     """, [stevilo])
#     for ime, prebivalstvo, ustanovitev in cur:
#         print(f"{ime} z {prebivalstvo} prebivalci, ustanovljena leta {ustanovitev}")

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
