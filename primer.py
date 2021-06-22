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
    cur.execute("SELECT vrsta, cena FROM ponudba")
    return template('ponudba.html', ponudba=cur)

@get('/registracija')
def registracija():
    return template('registracija.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='', napaka = None)


@post('/registracija')
def registracija_post():
     ime = request.forms.ime
     priimek = request.forms.priimek
     kraj = request.forms.kraj
     naslov = request.forms.naslov
     telefon = request.forms.telefon
     uporabnisko_ime = request.forms.uporabnisko_ime
     geslo1 = request.forms.geslo1
     geslo2 = request.forms.geslo2
     if geslo1 == geslo2:
        try:
            cur.execute("INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, uporabnisko_ime, geslo1, geslo2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (ime, priimek, kraj, naslov, telefon, uporabnisko_ime, geslo1, geslo2))
            conn.commit()
        except Exception as ex:
            conn.rollback()
            return template('registracija.html', ime=ime, priimek=priimek, kraj=kraj, naslov=naslov, telefon=telefon, uporabnisko_ime=uporabnisko_ime, geslo1=geslo1, geslo2=geslo2,
                napaka='Zgodila se je napaka: %s' % ex)
        redirect(url('index'))

@get('/prijava')
def prijava():
    return template('prijava.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='', napaka = None)

@post('/prijava')
def prijava_post():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    if uporabnisko_ime is None or geslo is None:
        nastaviSporocilo('Uporabniško ima in geslo morata biti neprazna') 
        redirect('/prijava')
        return
    cur = baza.cursor()    
    hashBaza = None
    try: 
        hashBaza = cur.execute("SELECT geslo FROM oseba WHERE uporabnisko_ime = ?", (uporabnisko_ime, )).fetchone()
        hashBaza = hashBaza[0]
    except:
        hashBaza = None
    if hashBaza is None:
        nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
        redirect('/prijava')
        return
    if hashGesla(geslo) != hashBaza:
        nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
        redirect('/prijava')
        return
    response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
    redirect('/uporabnik')

    
    
######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
