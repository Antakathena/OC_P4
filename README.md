# OC_P4
OC_P4 est un programme python 3 de gestion de tournois d'échec, orienté POO, appliquant le pattern MVC.

## Infos Générales :
Gestion tournois d'échec. OC_P4 utilise TinyDB pour conserver les informations sur les joueurs et les tournois.
Il est composé de 4 modules :
- dbtools, qui contient les classes et fonctions liées à la database et aux rapports
- P4models.py, comportant les modèles métier (classes liées aux joueurs et aux tournois)
- P4controllers.py, qui gère les interactions entre les modèles et les vues
- P4views.py, où se trouvent les classes et constantes liées à l'affichage

## Utilité :
Destiné à des organisateurs de tournoi d'échec, le programme permet d'enregistrer les joueurs,
d'enregistrer des tournois et de faire jouer un tournoi selon les règles du tournoi suisse.
Les informations sur les joueurs et les tournois sont conservées dans un fichier json au moyen de TinyDB.
L'utilisateur peut afficher la liste des joueurs par classement,
la liste des joueurs par ordre alphabétique,
la liste des tournois, ou des informations spécifiques sur les tournois joués (joueurs, matchs, tours et résultats)

## Fonctionnalités :

### Fonctions :
- P4models.py prévoit la structure des objets joueurs, tournois, rounds et matchs (dataclasses python 3.9 et supp)
NB : les algorithmes de répartition des joueurs en matchs sont dans la classe shift (structure et organisation des rounds)
- dbtools.py comprend les fonctions de sauvegarde , de récupération et de modification des objets dans la database,
y compris des outils de serialisation et déserialisation des dates automatiques (les datetimes ne sont pas aceptés par Tinydb)
- P4views comprends les classes qui créént les vues ainsi que les constantes MENU_CHOICES, FORMS_FIELDS et REPORTS,
qui permettent d'avoir à un même endroit les informations que ces listes contiennent et de les modifier facilement.
- P4controllers.py est organisé comme suit :
    - les classes MenuManager et FormManager, redirigent vers le bon controleur en fonction de la demande (input)
    - la classe ManagerFactory, créé les objets menu ou questionnaire (classes précitées) au besoin
    - la classe ReportManager, qui affiche le bon rapport si c'est la demande
    - les classes PlayerManager et TournamentManager assistent à l'enregistrement de nouveaux éléments
    - la classe PlayTournament s'occupe des interactions entre modules liées au déroulement du tournoi.

### Main :
P4main.py
Affiche l'accueil et le menu principal,
la suite dépend du choix de l'utilisateur.

## Instruction de démarrage :
Python 3.9 ou supérieur (dataclasses)
Dans un terminal, utiliser les commandes suivantes :

$ python3 -m venv env (créé un dossier env dans le répértoire où vous vous trouvez)

$ source env/bin/activate (sous linux) ou env\Scripts\activate.bat (pour activer l'environnement virtuel sous windows)

$ git clone https://github.com/Antakathena/OC_P4

$ cd ../chemin/du/dossier (de la copie de OC_P4 dans votre dossier env)

$ pip install -r requirements.txt

$ python P4main.py