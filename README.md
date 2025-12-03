# Boulder-Buddy

## Tällä hetkellä toimivat ominaisuudet

- Käyttäjätunnusten luonti
- Sisään-/uloskirjautuminen
- Käyttäjä voi merkitä reitin kiivetyksi ja lisätä kommentin
- Käyttäjä näkee 10 kiipeämäänsä reittiä etusivulla
- Mahdollisuus etsiä ja tutkia muita käyttäjiä
- Mahdollisuus katsoa tilastoja omista suorituksista
- Mahdollisuus muokata kommentteja
- Ilmoitukset virhetilanteista 
- (Reittien/salien muokkaus tavallisen käyttäjän näkökulmasta ei järkevää: 
tarkoituksena että käyttäjä on asiakkaan roolissa, jossa sekä reitit, että salit
ovat adminien lisäämiä. Joskin tällä hetkellä kovakoodattavia.)

## Kehityskohteita tulevaisuudessa
- Admin käyttäjäryhmä, joka pystyy hallinnoimaan salien ja reittien lisäämistä

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