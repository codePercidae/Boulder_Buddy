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
- Käyttäjä näkee 10 kiipeämäänsä reittiä etusivulla (tarkoituksena olla viimeisimmät 10 kiivettyä, mutta ei ollut aikaa viedä sitä loppuun ennen palautusta)

## HUOM
Jos syystä tai toisesta flask skriptit eivät toimi, tee seuraava:

1. Luo juurihakemistoon tiedosto boulder.db
2. Aja komento `sqlite3 boulder.db < schema.sql`
3. Aja komento `python3 seed.py`
4. Suorita funktio test()