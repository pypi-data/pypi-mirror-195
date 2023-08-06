# Meduse

![image de Meduse](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Medusa_Cameo_Petescia_Berlin_Altes_Museum_27042018_2.jpg/231px-Medusa_Cameo_Petescia_Berlin_Altes_Museum_27042018_2.jpg)

Outil en ligne de commande destiné à réaliser des copies statiques des projets du PDN (Pôle Document Numérique).

## Pré-requis

* Python 3.6 ou plus récent
* wget

## Installation hors développement

```
pip install meduse-CERTIC
```

## Principe

3 étapes:

1. Aspiration des sites avec wget.
2. Modification éventuelle des pages.
3. Indexation des pages, dans Elasticsearch si présent.

## Utilisation

Suivre les instructions affichées avec `meduse --help`

## Exemple

Aspirer un site dans le répertoire courant:

```
meduse mirror http://acme.com/
```

Aspirer un site dans un autre répertoire:

```
meduse mirror http://acme.com/ -d /home/johndoe/sites/acme
```

## Installation de l'environnement pour le développement développement

```
$> python3 -m venv venv
$> . ./venv/bin/activate
$> pip install -r requirements.txt
```
