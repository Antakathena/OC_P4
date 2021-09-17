# setup?
import datetime
# constantes?

# fonctions globales?

# un module pour models, un pour views, un pour controlls?

class Player:
    """
    définit la classe Player, qui permet:
    d'enregistrer et de modifier les informations sur les joueurs
    """
    def __init__(self, c_name, c_firstname, c_birthdate, c_gender, c_rating):
        # attributs = name, firstname, birthdate, gender, rating
        # à transformer en une liste pour chaque joueur?

        print("Création d'un joueur...")
    
        self.name = c_name
        self.firstname = c_firstname
        self.birthdate = c_birthdate
        self.gender = c_gender
        self.rating = c_rating
    
    def add_player():

print ("lancement du programme...")

Joueur1 = Player("Smith", "Joe", 25/12/1980, "homme", 2500 )
print("Prénom de Joueur1 : {}".format (Joueur1.firstname))
print("date de naissance de Joueur1 : {}".format (Joueur1.birthdate))
print("Genre de Joueur1 : {}".format (Joueur1.gender))
print("classement de Joueur1 : {}".format (Joueur1.rating))



class Match:
    """
    définit la classe Match, qui permet:
    d'enregistrer les parties jouées sous forme de liste
    d'enregistrer les scores
    """
    def__init__(self, ):
    pass

class Round :
    """
    définit la classe Round, qui permet:
    d'assembler les joueurs en paire selon les règles du tournoi Suisse (créé les nouveaux matchs)
    d'enregistrer automatiquement le début du tour (date et heure)
    d'enregistrer automatiquement la fin du tour (date et heure)
    """
    def__init__(self):
    pass

class Turnament:
    """
    définit la classe Turnament, qui permet :
    de créer un nouveau tournoi
    d'organiser et de conserver les informations des tournois

    """
    def__init__(self):
    pass

class Report:
    """
    définit la classe Report, qui permet :
    d'afficher des listes contenant les informations conservées
    """
    def__init__(self):
    pass


if __name__ == "__main__":