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
import binascii

skrivnost='1234'

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)
ROOT = os.environ.get('BOTTLE_ROOT', '/')

# odkomentiraj, če želiš sporočila o napakah
debug(True)

@get('/static/<filename:path>')
def static(filename):
     return static_file(filename, root='static')

@get('/')
def index():
    cur.execute("SELECT vrsta, cena FROM ponudba")
    return template('ponudba.html', ponudba=cur, uporabnisko_ime='', geslo1='')

""" def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

def preveri_uporabnika(uporabnisko_ime, geslo1):
    try:
        cur.execute("SELECT * FROM prijava WHERE uporabnik = %s", (uporabnisko_ime, ))
        id,uporabnisko_ime,geslo1,ime,priimek = cur.fetchone()
        salt = geslo1[:64]
        geslo1 = geslo1[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  geslo1.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        if pwdhash == geslo1:
            return [ime]
    except:
        return False """

@get('/dodaj_ponudbo')
def dodaj_ponudbo():
    return template('ponudba2.html', vrsta='', cena='', zaloga='', napaka = None)

@post('/dodaj_ponudbo')
def dodaj_ponudbo_post():
    vrsta = request.forms.vrsta
    cena = request.forms.cena
    zaloga = request.forms.zaloga
    try:
        cur.execute("INSERT INTO ponudba (vrsta, cena, zaloga) VALUES (%s, %s, %s)",
                    (vrsta, cena, zaloga))
        conn.commit()
    except Exception as ex:
        conn.rollback()
        return template('ponudba2.html', vrsta=vrsta, cena=cena, zaloga=zaloga,
            napaka='Zgodila se je napaka: %s' % ex)
    redirect(url('index'))

@get('/povecaj_zalogo')
def povecaj_zalogo():
    return template('povecaj_zalogo.html', id='', zaloga_dodana='', napaka = None)


@post('/povecaj_zalogo')
def povecaj_zalogo_post():
    id = request.forms.id
    zaloga_dodana = request.forms.zaloga_dodana 
    try:
        cur.execute("UPDATE ponudba SET zaloga = zaloga + %s WHERE id = %s",(int(zaloga_dodana), int(id)))
        conn.commit()
    except Exception as ex:
        conn.rollback()
        return template('povecaj_zalogo.html', id='', zaloga_dodana='',
        napaka='Zgodila se je napaka: %s' % ex)

    redirect(url('index'))

@get('/spremeni_placo')
def spremeni_placo():
    return template('spremeni_placo.html', id='', spremeni_placo='', napaka = None)


@post('/spremeni_placo')
def spremeni_placo_post():
    id = request.forms.id
    spremeni_placo = request.forms.spremeni_placo 
    try:
        cur.execute("UPDATE zaposleni SET placa = placa + %s WHERE id = %s",(int(spremeni_placo), int(id)))
        conn.commit()
    except Exception as ex:
        conn.rollback()
        return template('spremeni_placo.html', id='', spremeni_placo='',
        napaka='Zgodila se je napaka: %s' % ex)

    redirect(url('index'))


def ustvari_tabelo_narocila():
    cur.execute("""
        CREATE TABLE narocila (
            id SERIAL PRIMARY KEY,
            uporabnisko_ime TEXT NOT NULL,
            vrsta TEXT NOT NULL,
            datum DATE NOT NULL,
            kolicina INTEGER NOT NULL,
            cena TEXT NOT NULL
        );
    """)
    conn.commit()
#ni na php
#dodaj datume
@get('/oddaj_narocilo')
def oddaj_narocilo():
   return template('oddaj_narocilo.html', uporabnisko_ime='',vrsta='',kolicina='', napaka = None)

@post('/oddaj_narocilo')
def oddaj_narocilo():
    uporabnisko_ime = request.forms.uporabnisko_ime
    vrsta = request.forms.vrsta
    kolicina = request.forms.kolicina
    try:
        cur.execute("SELECT cena FROM ponudba WHERE id = %s" %int(vrsta))
        cena_izdelka = cur.fetchone()[0]
        cur.execute("UPDATE ponudba SET zaloga = zaloga - %s WHERE id = %s",(int(kolicina),int(vrsta)))
        cur.execute("INSERT INTO narocila(stevilka_narocila, uporabnisko_ime,vrsta,kolicina,cena) VALUES(DEFAULT, %s,%s,%s,%s)",
                    (uporabnisko_ime, vrsta, kolicina, int(kolicina)*cena_izdelka))
        conn.commit()   
    except Exception as ex: 
        conn.rollback()
        return template('oddaj_narocilo.html', uporabnisko_ime='',vrsta='',kolicina='',
        napaka='Zgodila se je napaka: %s' % ex)
    redirect(url('indeks'))




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

def javiNapaka(napaka = None):
    sporocilo = request.get_cookie('napaka', secret=skrivnost)
    #if napaka is None:
        #response.delete_cookie('napaka')
    #else:
        #path doloca za katere domene naj bo napaka, default je cela domena
        #response.set_cookie('napaka', napaka, path="/", secret=skrivnost)
    return sporocilo

@get('/prijava')
def prijava():
    
    napaka = javiNapaka()
    #uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret=skrivnost)

    return template('prijava.html', 
                    naslov='Prijava', 
                    napaka=napaka,
                    uporabnisko_ime='', 
                    geslo1='')

@post('/prijava')
def prijava_post():
    #poberimo vnesene podatke
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo1 = request.forms.geslo1
    
    hashGeslo = None
    try: 
        ukaz = ("SELECT geslo FROM narocniki WHERE uporabnisko_ime = (%s)")
        cur.execute(ukaz, (uporabnisko_ime,))
        hashGeslo = cur.fetchone()
        hashGeslo = hashGeslo[0]
    except:
        hashGeslo = None
    if hashGeslo is None:
        javiNapaka('Niste še registrirani')
        redirect('{0}prijava'.format(ROOT))
        return
    if hashGesla(geslo1) != hashGeslo:
        javiNapaka('Geslo ni pravilno')
        redirect('{0}prijava'.format(ROOT))
        return
    #response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
    #return template('uporabnik.html', uporabnisko_ime=uporabnisko_ime, geslo1=geslo1,
                #napaka='Zgodila se je napaka: %s' % ex)
    redirect(url('registracija'))

""" @get('/prijava')
def prijava():
    return template('prijava.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='', napaka = None)

@post('/prijava')
def prijava_post():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo1 = request.forms.geslo1
    preveri = preveri_uporabnika(uporabnisko_ime, geslo1)
    if preveri:
        ime, status = preveri
        cur.execute("SELECT id FROM prijava WHERE ime LIKE %s", (ime,))
        ID = cur.fetchall()
        ID = ID[0][0]
        #response.set_cookie('id', ID, secret=skrivnost)
        #response.set_cookie('account', ime, secret=skrivnost)
        #response.set_cookie('username', uporabnisko_ime, secret=skrivnost)
        #response.delete_cookie('napaka')
        #response.set_cookie('dovoljenje', status, secret=skrivnost)
        return template('uporabnik.html')
    else:
        napaka = 'Uporabniško ime in geslo se ne ujemata'
        #response.set_cookie('napaka', napaka, secret=skrivnost) """
        
#21

""" @post('/prijava')
def prijava_post():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    if uporabnisko_ime is None or geslo is None:
        print('Uporabniško ima in geslo morata biti neprazna') 
        redirect('/prijava')
        return
    cur = baza.cursor()    
    hashBaza = None
    try: 
        hashBaza = cur.execute("SELECT geslo FROM narocnik WHERE uporabnisko_ime = ?", (uporabnisko_ime, )).fetchone()
        hashBaza = hashBaza[0]
    except:
        hashBaza = None
    if hashBaza is None:
        print('Uporabniško geslo ali ime nista ustrezni') 
        redirect('/prijava')
        return
    if hashGesla(geslo) != hashBaza:
        print('Uporabniško geslo ali ime nista ustrezni') 
        redirect('/prijava')
        return
    #response.set_cookie('uporabnisko_ime', uporabnisko_ime) #, secret=skrivnost
    redirect('/uporabnik')
 """
    
    
######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
