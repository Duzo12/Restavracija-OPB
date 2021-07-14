print('SERVER SE JE ZAGNAL')
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
    nastaviSporocilo('Pozdravljeni v Duzo Restavracija. V kolikor še niste naš član se prosim registrirajte.')
    napaka = request.get_cookie('sporocilo', secret=skrivnost)
    #uporabnik = request.get_cookie('account', secret=skrivnost)
    #registracija = request.get_cookie('registracija', secret=skrivnost)
    #napaka = request.get_cookie('napaka', secret=skrivnost)
    #status = request.get_cookie('dovoljenje', secret=skrivnost)

    #nastaviSporocilo('Pozdravljeni v Duzo Restavracija. V kolikor še niste naš član se prosim registrirajte')
    #cur.execute("SELECT vrsta, cena FROM ponudba")
    return template('zacetna_stran.html', uporabnisko_ime='', geslo='', napaka = napaka)

#def preveriUporabnika(): 
#    username = request.get_cookie("username", secret=skrivnost)
#    if username:
#        cur = baza.cursor()    
#        uporabni = None
#        try: 
#            uporabnik = cur.execute("SELECT * FROM oseba WHERE username = ?", (username, )).fetchone()
#        except:
#            uporabnik = None
#        if uporabnik: 
#            return uporabnik
#    redirect('/prijava')


#def hashGesla(s):
#    m = hashlib.sha256()
#    m.update(s.encode("utf-8"))
#    return m.hexdigest()


@post('/')
def prijava():
    uporabnik = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    #print(uporabnik)
    #print(geslo)
    if uporabnik == '' or geslo == '':
        print('podatki manjkajo')
        nastaviSporocilo('Uporabniško ima in geslo morata biti neprazna') 
        redirect('/')
        return
    hashBaza_zaposlen = None
    hashBaza_narocnik = None
    try: 
        cur.execute("SELECT geslo FROM zaposleni WHERE up_ime = %s", (uporabnik, ))
        hashBaza_zaposlen = cur.fetchone()[0]
        #print(hashBaza_zaposlen)
    except:
        hashBaza_zaposlen = None
    try:
        cur.execute("SELECT geslo FROM narocniki WHERE up_ime = %s", (uporabnik, ))
        hashBaza_narocnik = cur.fetchone()[0]
        #print(hashBaza_narocnik)
    except:
        hashBaza_narocnik = None
    if hashBaza_narocnik is None and hashBaza_zaposlen is None:
        #print('ne obstaja niti narocnik, niti zaposlen')
        nastaviSporocilo('Uporabniško ime ali geslo ni ustrezno') 
        redirect('/')
        return
    if hashBaza_zaposlen is None:
        #print('zaposlen is None')
        #if hashBaza_narocnik is None:
        #    print('narocnika ne obstaja')
        #    nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
        #    redirect('/')
        #    return
        if password_hash(geslo) != hashBaza_narocnik:
            #print('geslo narocnik se ne ujema')
            nastaviSporocilo('Uporabniško ime ali geslo ni ustrezno') 
            redirect('/')
            return
        #print('narocnika smo uspesno prijavili')
        response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
        nastaviSporocilo("{0} pozdravljen! Preglej našo današnjo ponudbo in če želiš, oddaj naročilo.".format(uporabnik))
        redirect('/ponudba')
    #if hashBaza_narocnik is not None:
    #        nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
    #        redirect('/')
    #        return
    #if hashGesla(geslo) != hashBaza_narocnik:
    #    nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
    #    redirect('/')
    #    return
    response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
    print('zaposlenega smo uspešno prijavili')
    nastaviSporocilo("{0} pozdravljen!".format(uporabnik))
    redirect('/vodenje_restavracija')

@get('/ponudba')
def ponudba():
    uporabnik = request.get_cookie('uporabnik', secret=skrivnost)
    nastaviSporocilo("{0} pozdravljen! Preglej našo današnjo ponudbo in če želiš, oddaj naročilo.".format(uporabnik))
    napaka = request.get_cookie('sporocilo', secret=skrivnost)
    cur.execute("SELECT vrsta, cena FROM ponudba WHERE zaloga > 0")
    return template('ponudba3.html', ponudba=cur, napaka = napaka)

@get('/vodenje_restavracija')
def vodenje_restavracije():
    uporabnik = request.get_cookie('uporabnik', secret=skrivnost)
    napaka = request.get_cookie('sporocilo', secret=skrivnost)
    return template('vodenje_restavracije.html', napaka = napaka)


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
    print(id)
    print(zaloga_dodana)
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
        #return template('registracija.html', ime='', priimek='', kraj='', naslov='', telefon='', uporabnisko_ime='', geslo1='', geslo2='',
        #    napaka = 'Gesli se ne ujemata')
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





    
######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
