#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import debug
from bottleext import get, post, run, request, template, redirect, static_file, url, response

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2 neki sprem
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import os
import binascii
import hashlib #za kodiranje gesel

skrivnost="S648ZHJ8ghjk7UUU32f"

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)
ROOT = os.environ.get('BOTTLE_ROOT', '/')

# odkomentiraj, če želiš sporočila o napakah
debug(True)

def nastaviSporocilo(sporocilo = None):
    # global napakaSporocilo
    staro = request.get_cookie("sporocilo", secret=skrivnost)
    if sporocilo is None:
        response.delete_cookie('sporocilo') #če funkciji ne podamo ničesar, izbriše piškotek z imenom sporočilo
    else:
        response.set_cookie('sporocilo', sporocilo, path="/", secret=skrivnost)
    return staro

# Mapa za statične vire (slike, css, ...)
static_dir = "./static"


@get('/static/<filename:path>')
def static(filename):
     return static_file(filename, root='static')

@get('/')
def index():
    napaka = request.get_cookie('sporocilo', secret=skrivnost)
    cur.execute("SELECT vrsta, cena FROM ponudba")
    #hamburger = 'Hamburger'
    #cur.execute("SELECT vrsta, cena FROM ponudba WHERE vrsta=%s", (hamburger, ))
    return template('uvodna_stran.html', ponudba=cur, uporabnisko_ime='', geslo1='', napaka = napaka)

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
    cur.execute("SELECT vrsta FROM ponudba")
    ponudba = cur.fetchall()
    return template('povecaj_zalogo2.html', ponudba = ponudba, vrsta_zaloge='', kolicina_nove_zaloge='', napaka = None)
    #return template('povecaj_zalogo.html', id='', zaloga_dodana='', napaka = None)


@post('/povecaj_zalogo')
def povecaj_zalogo_post():
    #id = request.forms.id
    #zaloga_dodana = request.forms.zaloga_dodana
    id = request.forms.vrsta_zaloge
    zaloga_dodana = request.forms.kolicina_nove_zaloge
    try:
        #cur.execute("UPDATE ponudba SET zaloga = zaloga + %s WHERE id = %s",(int(zaloga_dodana), int(id)))
        cur.execute("UPDATE ponudba SET zaloga = zaloga + %s WHERE vrsta = %s",(int(zaloga_dodana), id))
        conn.commit()
    except Exception as ex:
        conn.rollback()
        #return template('povecaj_zalogo.html', id='', zaloga_dodana='',
        #napaka='Zgodila se je napaka: %s' % ex)
        cur.execute("SELECT vrsta FROM ponudba")
        ponudba = cur.fetchall()
        return template('povecaj_zalogo2.html', ponudba=ponudba, vrsta_zaloge='', kolicina_nove_zaloge='',
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


def password_hash(s):
    """Vrni SHA-512 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.sha512()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

@get('/registracija')
def registracija():
    napaka = nastaviSporocilo()
    return template('registracija.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='', napaka = napaka)
    #return template('registracija.html', napaka = napaka)

def preveri_za_narocnika(narocnik):
    try:
        cur.execute("SELECT up_ime FROM narocniki WHERE up_ime = %s", (narocnik, ))
        #uporabnik = cur.fetchone([0])
        narocnik1 = cur.fetchone()
        cur.execute("SELECT up_ime FROM zaposleni WHERE up_ime = %s", (narocnik, ))
        narocnik2 = cur.fetchone()
        if narocnik1==None and narocnik2==None:
            return True
        else:
            return False
    except:
        return False


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
     #jezekdotak=cur.execute("SELECT * FROM narocniki WHERE up_ime=%s", (uporabnisko_ime))
     if preveri_za_narocnika(uporabnisko_ime) == False:
        return template('registracija.html', ime=ime, priimek=priimek, kraj=kraj, naslov=naslov, telefon=telefon, uporabnisko_ime=uporabnisko_ime, geslo1=geslo1, geslo2=geslo2,
                napaka='Uporabnik s tem uporabniškim imenom že obstaja')
        #return template('registracija.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='',
            #napaka = 'Uporabnik s tem uporabniškim imenom že obstaja')
        #nastaviSporocilo('Uporabnik s tem imenom že obstaja') 
        #redirect('/registracija')
     if geslo1 != geslo2:
        return template('registracija.html', ime=ime, priimek=priimek, kraj=kraj, naslov=naslov, telefon=telefon, uporabnisko_ime=uporabnisko_ime, geslo1=geslo1, geslo2=geslo2,
            napaka='Gesli se ne ujemata')
        return template('registracija.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='',
            napaka = 'Gesli se ne ujemata')
        #nastaviSporocilo('Gesli se ne ujemata') 
        #redirect('/registracija')
     else:
        try:
            geslo = password_hash(geslo1)
            cur.execute("INSERT INTO narocniki (ime, priimek, kraj, naslov, telefon, up_ime, geslo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (ime, priimek, kraj, naslov, telefon, uporabnisko_ime, geslo))
            conn.commit()
            #response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
        except Exception as ex:
            conn.rollback()
            return template('registracija.html', ime=ime, priimek=priimek, kraj=kraj, naslov=naslov, telefon=telefon, uporabnisko_ime=uporabnisko_ime, geslo1=geslo1, geslo2=geslo2,
                napaka='Zgodila se je napaka: %s' % ex)
            #nastaviSporocilo('Zgodila se je napaka') 
            #redirect('/registracija')
        nastaviSporocilo('Registracija uspešna. Lahko se prijavite.')
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

#@post('/prijava')
#def prijava_post():
#    #poberimo vnesene podatke
#    uporabnisko_ime = request.forms.uporabnisko_ime
#    geslo1 = request.forms.geslo1
#    
#    hashGeslo = None
#    try: 
#        ukaz = ("SELECT geslo FROM narocniki WHERE uporabnisko_ime = (%s)")
#        cur.execute(ukaz, (uporabnisko_ime,))
#        hashGeslo = cur.fetchone()
#        hashGeslo = hashGeslo[0]
#    except:
#        hashGeslo = None
#    if hashGeslo is None:
#        javiNapaka('Niste še registrirani')
#        redirect('{0}prijava'.format(ROOT))
#        return
#    if hashGesla(geslo1) != hashGeslo:
#        javiNapaka('Geslo ni pravilno')
#        redirect('{0}prijava'.format(ROOT))
#        return
#    #response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
#    #return template('uporabnik.html', uporabnisko_ime=uporabnisko_ime, geslo1=geslo1,
#                #napaka='Zgodila se je napaka: %s' % ex)
#    redirect(url('registracija'))

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
        
#213

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
