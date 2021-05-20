#SAMO DA VIDIM KAKO DELUJE COMMIT 2
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import debug
from bottleext import get, post, run, request, template, redirect, static_file, url

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2 neki sprem
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# odkomentiraj, če želiš sporočila o napakah
debug(True)

@get('/static/<filename:path>')
def static(filename):
     return static_file(filename, root='static')

@get('/')
def index():
    cur.execute("SELECT * FROM narocniki ORDER BY priimek, ime")
    return template('narocniki.html', narocnik=cur)

@get('/registracija')
def registracija():
    return template('registracija.html', ime='', priimek='', naslov='', napaka = None)

@post('/registracija')
def registracija_post():
     ime = request.forms.ime
     priimek = request.forms.priimek
     naslov = request.forms.naslov
     try:
         cur.execute("INSERT INTO narocniki (ime, priimek, naslov) VALUES (%s, %s, %s)",
                     (ime, priimek, naslov))
         conn.commit()
     except Exception as ex:
         conn.rollback()
         return template('registracija.html', ime=ime, priimek=priimek, naslov=naslov,
                         napaka='Zgodila se je napaka: %s' % ex)
     redirect(url('index'))
    
######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
