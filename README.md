Télécharger les informations et cours des OPCVM sans frais d'entrée/sortie disponibles via Boursorama.

## Données

- `boursorama/boursorama_opcvm.jl` : informations générales sur les OPCVM au format [JSON Lines](http://jsonlines.org/)

```javascript
{
    "url_identifier": "MP-809642",
    "nom": "Allianz Immo D",
    "devise": "EUR",
    "identifiant": "FR0000011967 - Allianz Global Investors GmbH",
    "actif net": "29.02.20 / 64 829.75",
    "date de création": "21.06.1971",
    "société de gestion": "Allianz Global Investors GmbH",
    "groupe de gestion": "Allianz Global Investors",
    "catégorie Morningstar": "Immobilier - Indirect Europe",
    "forme juridique": "SICAV",
    "affectation des résultats": "Distribution",
    "fonds de fonds": "Non",
    "frais d'entrée": "0.00 %",
    "frais de sortie": "0.00 %",
    "frais courants": "1.2 %",
    "souscription min. initiale": "0 EUR"
}
```

- `opcvm_cours/[identifiant de l'OPCVM].csv` : cours de l'OPCVM au format CSV

    [date en nombre de jours depuis le 1er janvier 1970];[date au format ISO 8601];[cours]

    17962;2019-03-07;69.97

## Installation

    virtualenv -p /usr/bin/python3 env
    source env/bin/activate
    pip install -r requirements.txt

## Utilisation

Création du fichier `boursorama/boursorama_opcvm.jl`

    cd boursorama/
    scrapy crawl opcvm
    
    boursorama/boursorama_opcvm.jl

Création des fichiers `opcvm_cours/[identifiant de l'OPCVM].csv`

    python opcvm_cours.py
