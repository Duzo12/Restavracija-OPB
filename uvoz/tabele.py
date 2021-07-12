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
            placa FLOAT (2) NOT NULL CHECK (placa >= 600),
            rojstvo DATE NOT NULL,
            up_ime TEXT NOT NULL UNIQUE,
            geslo TEXT NOT NULL UNIQUE
        );
    """) #morda bi pri telefon dodal unique, DATE se vstavlja v obliki 'YYYY-MM-DD'
    conn.commit()

def pobrisi_tabelo_zaposleni():
    cur.execute("""
        DROP TABLE zaposleni;
    """)
    conn.commit()

def uvozi_podatke_zaposleni():
    cur.execute("""
        INSERT INTO zaposleni (ime, priimek, telefon, placa, rojstvo, up_ime, geslo) VALUES ('Nejc', 'Duscak', '070 256 331', 1500.00, '1998-01-07', 'nejcduscak', 'geslo1');
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
            telefon TEXT NOT NULL,
            up_ime TEXT NOT NULL UNIQUE,
            geslo TEXT NOT NULL UNIQUE
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
        INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, up_ime, geslo) VALUES ('Nejc', 'Duscak', 'Ljubljana', 'Ulica 1', '070 256 331', 'nd', 'geslo11');
        INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, up_ime, geslo) VALUES ('Jan', 'Črne', 'Litija', 'Ulica 2', '031 262 381', 'jc', 'geslo22');
        INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, up_ime, geslo) VALUES ('Maks', 'Perbil', 'Vrhnika', 'Ulica 3', '040 456 133', 'mp','geslo33');
    """)
    conn.commit()

def ustvari_tabelo_ponudba():
    cur.execute("""
        CREATE TABLE ponudba (
            id SERIAL PRIMARY KEY,
            vrsta TEXT NOT NULL UNIQUE,
            cena FLOAT (2) NOT NULL CHECK (cena > 0),
            zaloga INTEGER NOT NULL CHECK (zaloga >=0)
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
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Hamburger', 6.00, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Pizza', 8.50, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Čevapčiči', 7.00, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Pommes Frittes', 2.00, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Kebab', 3, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Burek', 2.50, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Taquitosi', 4, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Pohan piščanec', 5.50, 4);
        INSERT INTO ponudba (vrsta, cena, zaloga) VALUES ('Sladoled', 2.50, 4);
    """)
    conn.commit()

def ustvari_tabelo_narocila():
    cur.execute("""
        CREATE TABLE narocila (
            st_narocila SERIAL PRIMARY KEY,
            id_narocnika INTEGER REFERENCES narocniki(id),
            id_ponudbe INTEGER REFERENCES ponudba(id),
            datum_narocila DATE NOT NULL DEFAULT now(),
            cas_narocila TIME NOT NULL DEFAULT now(),
            kolicina INTEGER NOT NULL CHECK (kolicina > 0)
        );
    """) #SQL Server accepts time values in the following formats: 14:30, 14:30:20, 14:30:20:145943, 2 PM, 2:30 PM, 2:30:20 PM 2:30:20.145943 PM.
    conn.commit()

def pobrisi_tabelo_narocila():
    cur.execute("""
        DROP TABLE narocila;
    """)
    conn.commit()

def podeli_pravice():
    cur.execute("""
        GRANT ALL ON DATABASE sem2021_nejcd TO janc WITH GRANT OPTION;
        GRANT ALL ON SCHEMA public TO janc WITH GRANT OPTION;
        GRANT ALL ON DATABASE sem2021_nejcd TO maksp WITH GRANT OPTION;
        GRANT ALL ON SCHEMA public TO maksp WITH GRANT OPTION;
        GRANT CONNECT ON DATABASE sem2021_nejcd TO javnost;
        GRANT USAGE ON SCHEMA public TO javnost;
        GRANT ALL ON ALL TABLES IN SCHEMA public TO nejcd WITH GRANT OPTION;
        GRANT ALL ON ALL TABLES IN SCHEMA public TO janc WITH GRANT OPTION;
        GRANT ALL ON ALL TABLES IN SCHEMA public TO maksp WITH GRANT OPTION;
        GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO nejcd WITH GRANT OPTION;
        GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO janc WITH GRANT OPTION;
        GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO maksp WITH GRANT OPTION;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost WITH GRANT OPTION;
        GRANT INSERT ON narocila TO javnost;
        GRANT INSERT ON narocniki TO javnost;
        GRANT INSERT ON ponudba TO javnost;
        GRANT UPDATE ON ponudba TO javnost;
        GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;
    """)
#ni na php
#se datumi
#GRANT INSERT ON ponudba TO javnost; izbrisi ko naredimo locljivost po uporabnikih

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
rolbak = cur.execute("ROLLBACK")
