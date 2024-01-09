![chess_club](_img/echec.jpg)

# Projet 4 Tournoi Echecs
***logiciel de gestion de tournoi d'échecs.***

Développé sous Windows 10  et Python version 3.10.11


## Table des matières

1. [Installation du projet](#chapitre1)
    1. [Windows](#chapitre1-1)
    1. [MacOS et Linux](chapitre1-2)
    3. [Générer un rapport flake8](chapitre1-3)
2. [menus du programme](chapitre2)
    1. [Menu principal](#section2-1)
    2. [Exemple de Rapports](#section2-2)
3. [Exemples d'affichage](#section3)


<div id='chapitre1'></div>

## 1. Initialisation du projet

<div id='chapitre1-1'></div>


#### i. Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone https://github.com/canofranck/projet4_tournoi_d_echecs

###### Activer l'environnement virtuel
    $ cd Repertoire_du_projet
    $ python -m venv env 
    $ ~env\scripts\activate
    
###### Installer les packages requis
    $ pip install -r requirements.txt

###### Lancer le programme
    $ python main.py


<div id='chapitre1-2'></div>

---------

#### ii. MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone  https://github.com/canofranck/projet4_tournoi_d_echecs

###### Activer l'environnement virtuel
    $ cd Repertoire_du_projet
    $ python3 -m venv env 
    $ source env/bin/activate
    
###### Installer les packages requis
    $ pip install -r requirements.txt

###### Lancer le programme
    $ python3 main.py


<div id='chapitre1-3'></div>

----------

#### iii. Générer un rapport flake8

    $ flake8 --format=html --htmldir=flake8-report --exclude=env .


**Vous trouverez le rapport dans le dossier 'flake8-report'**


![latest_report](_img/flake8.jpg)

<div id='chapitre2'></div>

## 2. Options des menus

<div id='chapitre2-1'></div>

#### i. Menu Principal
![main_menu](_img/menu_main.jpg)

<div id='chapitre2-2'></div>

#### ii. Menu des rapports
![main_menu](_img/menu_reports.jpg)

<div id='chapitre3'></div>

## 3. Exemples d'affichage
#### Matchs d'une ronde :
![round](_img/round.jpg)

#### Rapport des joueurs :
![report_player](_img/reports_player.jpg)

#### Rapport des rounds :
![report_round](_img/reports_round.jpg)
