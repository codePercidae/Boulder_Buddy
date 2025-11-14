# Boulder-sovellus

Sovellus jolla käyttäjä voi:
- Luoda tunnuksen ja kirjautua sisään
- Lisätä suoritettuja reittejä
- Tarkastella muiden suorittamia reittejä
- Luokitella tehtyjä reittejä, vaikeuden, salin, yms. mukaan

## Sovelluksen asennus

Aloita asentamalla flask-kirjasto

```
    $ pip install flask
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