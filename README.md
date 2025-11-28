# Boulder-Buddy

Sovellus jolla käyttäjä voi:
- Luoda tunnuksen ja kirjautua sisään
- Lisätä suoritettuja reittejä
- Tarkastella muiden suorittamia reittejä
- Luokitella tehtyjä reittejä, vaikeuden, salin, yms. mukaan

## Sovelluksen asennus ja käyttöönotto

Aloita asentamalla venv (varmista että käytössäsi on python3):

```
$ python3 venv venv
``` 

Käynnistä virtuaaliympäristö:

```
$ source venv/bin/activate
```


Asenna flask-kirjasto

```
    $ pip install flask
```

Alusta tietokanta komennolla (luo tietokantatiedoston ja lataa skeeman):

```
    $ flask init-database
```


Saat luotua testidataa sovelluksen testaamista varten komennolla:

```
    $ flask create-test-data
```

Käynnistä sovellus komennolla:

```
    $ flask run
```

Tarvittaessa tietokannan saa puhdistettua kokonaan komennolla:

```
    $ flask delete-all
```

## Tällä hetkellä toimivat ominaisuudet

- Käyttäjätunnusten luonti
- Sisään-/uloskirjautuminen
- Käyttäjä voi merkitä reitin kiivetyksi
- Käyttäjä näkee 10 kiipeämäänsä reittiä etusivulla
- Mahdollisuus etsiä ja tutkia muita käyttäjiä
- Mahdollisuus katsoa tilastoja omista suorituksista