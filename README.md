# Restavracija-OPB
Spletna aplikacija pri premetu OPB

![Diagram-readme](https://user-images.githubusercontent.com/39483369/113877531-14e18500-97b9-11eb-90ed-e28d845aeb94.png)


# OPIS APLIKACIJE
Z aplikacijo bodo lahko uporabniki naročili hrano in pijačo, ob tem pa bodo navedli svoje ime ter naslov na katerega bo naročilo dostavljeno. Podali bodo tudi način plačila in količino izdelka, ki ga želijo, iz dane ponudbe. Aplikacija bo potem preverila ali je izdelek na voljo, in v primeru da je posredolvala naročilo operatorju, ki bo posredoval noročilo kuharjem, te pa pripravljeno hrano dostavljalcem, ki bodo potem hrano dostavili strankam na navedeni naslov. V apikaciji bodo za vodjo restavracije na voljo tudi podatki o zaposlenih ter podatki o vozilih s katerimi se bo dostava izvajala. 

Idejo za našo aplikacijo bomo oblikovali na podlagi spletnega naročanja hrane. Aplikacija bo za začetek posameznika prosila za njegove osebne podatke (ime, priimek in naslov), ter ga nato shranila v bazo podatkov pod zaporedno številko ID-ja. Sledilo bo izbira naročila. Naročnik bo imel na izbiro različne jedi. Za vsako izbiro bo moral navediti tudi količino le-te. Aplikacija bo nato sama preverila ali je dana jed na zalogi, in v tem primeru naročilo potrdilo, v nasprotnem pa zavrnila. Naročilo bo na koncu dostavljeno operaterju, ta ga bo predal kuharju in kuhar dostavljalcu. Dostavljalec pa bo hrano dostavil strankam na dani naslov. V apikaciji bodo za vodjo restavracije na voljo tudi podatki o zaposlenih ter podatki o vozilih s katerimi se bo dostava izvajala. 

Spodaj je podano nekaj poljubnih tabel

## Zaposleni
|*ID*|*Ime*|*Priimek*|*Telefon*|*Plača*|*Rojstvo*|
|----|-----|---------|---------|--------|--------|
|1|Marija|Novak|031234567|1200€|21.11.1990|
|2|Klemen|Koren|529654712|1520€|28.04.1966|
|3|Tine|Robnjak|041857007|5000€|02.01.1988|

## Stranka
|*ID*|*Ime*|*Priimek*|*Naslov*|
|----|-----|---------|---------|
|1|Tone|Pintarič|Zavrti 22A|
|2|Ema|Klinec|Testenova 56|
|3|Tina|Soseda|Janševa 12|

## Prevozno sredstvo
|*ID*|*Tip*|*Znamka*|
|----|-----|---------|
|1|avto|Renault|
|2|avto|Fiat|
|3|kolo|KTM|
|4|motor|Tomos|

## Ponudba
|*ID*|*Vrsta*|
|----|-----|
|1|hamburger|
|2|pizza|
|3|hot-dog|
|4|sladoled|
