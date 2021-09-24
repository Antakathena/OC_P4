import datetime
import models
import menu 
# comment faire pour ajouter des modèles au py_cache?
# peut-on faire un dossier "models" avec un model par fichier, faut-il dedans un fichier init, à quoi ça sert?

"""
class Controller:

    # on commence par initialiser les modèles (?) et la vue : doit afficher le menu principal
    donc la classe menu.

    def __init__(self, menu):
        # models
        self.menu = menu
        # views
        self.view = None
"""   
# pour l'instant fonction   
def Afficher_Menu_Principal():
    
    print("\n \n Programme de gestion de tournois d'échec \n\n Menu Principal\n")
    main_menu = {}
    main_menu['1'] = "Créer un nouveau tournoi" 
    main_menu['2'] = "Ajouter un joueur"
    main_menu['3'] = "Afficher un rapport"
    main_menu['4'] = "Modifier le classement d'un joueur"
    main_menu['5'] = "Quitter"

    while True: 
        options = main_menu.keys()
        for entry in options: 
            print(entry, main_menu[entry])

        selection = input("\nVeuillez indiquer votre choix:") 
        if selection =='1': 
            print("Nouveau tournoi")
        elif selection == '2': 
            print("Nouveau joueur")
        elif selection == '3':
            print("Liste des rapports disponibles")
        elif selection == '4':
            print("Modifier le rang d'un joueur")
        elif selection == '5':
            print("Quitter") 
            break
        else: 
            print("\nChoix non valide. Veuillez indiquer le chiffre de la selection. \n\nMenu Principal:\n") 


    
#def star_new_tournament(self):


def validate_date(date, fmt_date):
    if not date:
        return False
    try:
        datetime.datetime.strptime(date, fmt_date)
        return True
    except ValueError:
        return False


def ask_user_until_valid(question, validator, convertisseur):
    choix = None
    while choix is None or validator(choix) is False:
        choix: str = input(question)
    return convertisseur(choix)

def add_player_infos (self, name, firstname, birthdate, gender, rating) -> list :
    """permet de rentrer les infos du joueur, retourne les infos pour vérification, empêche de valider si le formulaire contient une erreur"""
    player_infos = []

def change_player_rating (self) :
    """permet de changer le classement du joueur à l'issue des matchs"""


def create_tournament():
    name_tournament = input("Nom du tournoi :")
    date = ask_user_until_valid("Date du tournoi :",
                                validator=lambda d: validate_date(d, "%d/%m/%Y"),
                                convertisseur=lambda d: datetime.datetime.strptime(d, "%d/%m/%Y"))
    print(name_tournament, date)
    """Equivalent du lambda: 
    def (d):
        return datetime.datetime.strptime(d, "%d/%m/Y")"""
    models.Tournament(name_tournament, date=date)


def main_menu():
    LISTE_CHOIX = [
        ("Créer nouveau tournoi", create_tournament),
        ("Gérer tournoi existant", lambda: None),
        ("Enregistrer nouveau joueur", lambda: None),
        ("Menu des rapports", lambda: None)
    ] 
    for num, (choix, f_choix)  in enumerate(LISTE_CHOIX, start=1):
        print(f"{num}) {choix}")
    choix_valide = None
    while choix_valide is None:
        choix: str = input("Votre choix ?")
        try:
            choix = int(choix) - 1
        except ValueError:
            print("Veuillez taper un nombre entre 1 et 4")
        try:
            choix_valide = LISTE_CHOIX[choix]
        except IndexError:
            print("Veuillez taper une valeur comprise entre 1 et 4")
    print("Vous avez choisi : ", choix_valide)
    texte_choix, f_choix = choix_valide
    f_choix()

