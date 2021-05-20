#NEK DRUG COMMIT 3
# uvozimo ustrezne podatke za povezavo
from . import auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv

def ustvari_tabelo_zaposleni():
    cur.execute("""
        CREATE TABLE zaposleni (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            telefon INTEGER NOT NULL,
            placa NUMERIC NOT NULL,
            rojstvo INTEGER NOT NULL
        );
    """)
    conn.commit()

def pobrisi_tabelo_zaposleni():
    cur.execute("""
        DROP TABLE zaposleni;
    """)
    conn.commit()

def uvozi_podatke_zaposleni():
    cur.execute( """
        INSERT INTO zaposleni (id, ime, priimek, telefon, placa, rojstvo) VALUES (1, 'Nejc', 'Duscak', 0321, 41566, 1852)
    """)
    conn.commit()

def ustvari_tabelo_narocniki():
    cur.execute("""
        CREATE TABLE narocniki (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            naslov TEXT NOT NULL
        );
    """)
    conn.commit()

def pobrisi_tabelo_narocniki():
    cur.execute("""
        DROP TABLE narocniki;
    """)
    conn.commit()

def uvozi_podatke_narocniki():
    cur.execute("""
        INSERT INTO narocniki (id, ime, priimek, naslov) VALUES (1, 'Nejc', 'Duscak', 'Zavrti 22A')
    """)
    conn.commit()


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
