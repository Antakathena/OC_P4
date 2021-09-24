# setup?
from typing import List
"""
From Python 3.9 (PEP 585) onwards tuple, list and various other classes are now generic types.
Using these rather than their typing counterpart is now preferred.
From Python 3.9 you can now just do:

def f(points: tuple[float, float]):
    return map(do_stuff, points)
    
"""
import datetime
# constantes?

PLAYERS = []
TOURNAMENTS = []

# fonctions globales?

# un module pour models, un pour views, un pour controlls?

class Player:
    """
    définit la classe Player, qui permet:
    d'enregistrer et de modifier les informations sur les joueurs
    """
    def __init__(self, name, firstname, birthdate, gender, rating):
        """constructeur de Player"""
        print("Création d'un joueur...")
    
        self.name = name
        self.firstname = firstname
        self.birthdate = birthdate
        self.gender = gender
        self.rating = rating

    @staticmethod
    def _init_debug():
        joueur1 = Player("ATOME", "Adam", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "homme", 1010 )
        joueur2 = Player( "BARDOT", "Brigitte", datetime.datetime.strptime("01/02/1980", "%d/%m/%Y"), "femme", 220 )
        joueur3 = Player("CRUZ", "Chloé", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "femme", 1003 ) 
        joueur4 = Player("DOUILLET", "David", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "homme", 4000 )
        joueur5 = Player("ELITE", "Eddy", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "homme", 150 )
        joueur6 = Player("FEZ", "Françoise", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "femme", 1600 )
        joueur7 = Player("GEANT", "George", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "homme", 1070 )
        joueur8 = Player("HULOT", "Harry", datetime.datetime.strptime("01/01/1970", "%d/%m/%Y"), "homme", 1008 )
        for j in (joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8):
            PLAYERS.append(j)

    @property
    def birthdate(self):
        return self._birthdate
    
    @birthdate.setter
    def birthdate(self, value):
        assert isinstance(value, datetime.datetime), "Le contrôleur aurait du convertir cette donnée en datetime"
        self._birthdate = value


class Tournament:
    """
    définit la classe Tournament, qui permet :
    de créer un nouveau tournoi
    d'organiser et de conserver les informations des tournois
    d'assembler les joueurs en paire selon les règles du tournoi Suisse (créé les nouveaux matchs)

    """
    def __init__(self, c_tournament_name, c_location, c_dates, c_players: List[Player], c_number_of_rounds,
                c_timecontrol, c_description = None) :

        self.tournament_name = c_tournament_name
        self.location = c_location
        self.dates = c_dates
        self.players = c_players
        self.number_of_rounds = c_number_of_rounds
        self.timecontrol = c_timecontrol
        self.description = c_description
        self.rounds = []

    @property
    def nb_players(self):
        return len(self.players)

    @property
    def players(self):
        return self._players

    @nb_players.setter
    def players(self, players):
        if len(players) % 2 != 0:
            raise Exception("Le nombre de joueurs dans un tournoi doit être pair")
        self._players = players

    def create_pairs(self, players):
        """ Créé des paires basées sur le classement des joueurs pour le round 1 puis sur leurs résultats"""
        # ordonner la liste du plus fort au moins fort + enumerate?
        playerslist_by_rank = sorted(players, key = players[2])
        
        # si round 1 :
           
            # divise la liste (split) en 2 et associe 1-5, 2-6, etc (zip)
            # retourne une liste des paires des matchs du round 1
        # créer une liste où viendront s'ajouter tous les matchs joués (il nous faut les paires de joueurs déjà sorties)
        # pour chaque joueur récupérer le score des rounds précédents, les additionner
        # sinon (autre round que 1) :
            # classer les joueurs en fonction de leur score
            # si égalité ajoute le classement pour comparer chaque paire d'ex-equo
            # retourne une liste ordonnée
            # associe alors 1-2, 3-4 etc. (split et zip) = liste round n°x
            # compare la liste créée et celles des rounds précedents)
            # si le match 1 n'a pas eu lieu, il est ajouté à la nouvelle liste
            # si le match n°2 n'a pas eu lieu, idem, etc.
            # sinon, si le match a eu lieu, apparie avec le joueur avec le prochain joueur avec lequel il n'a pas encore joué dans la liste
                # alors, créé une liste des joueurs non appareillés, réapparie les joueurs à partir de là 
        # retourne 4 paires (en général) pour un round qui doivent aller dans match
        # split puis zip




class Round:
    """
    définit la classe Round, qui permet:
    d'enregistrer automatiquement le début du tour (date et heure)
    d'enregistrer automatiquement la fin du tour (date et heure)
    """
    def __init__(self, c_round_number, c_matchs_list, c_start_datetime, c_end_datetime):
        self.round_number = c_round_number
        self.matchs_list = c_matchs_list
        self.start_datetime = c_start_datetime
        self.end_datetime = c_end_datetime




class Match:
    """
    définit la classe Match, qui permet:
    d'enregistrer les parties jouées et les scores
    """
    def __init__(self, joueur_x, score_joueur_x, joueur_y, score_joueur_y):
        self.joueur_x = joueur_x
        self.score_joueur_x = score_joueur_x
        self.joueur_y = joueur_y
        self.score_joueur_y = score_joueur_y

    def record_score(self, score_x, score_y):
        """ permet de saisir les scores des 2 joueurs du match à la fin de la partie et les ajoute aux listes"""




class Report:
    """
    définit la classe Report, qui permet :
    d'afficher des listes contenant les informations conservées
    """
    def __init__(self):
       pass





if __name__ == "__main__":
    pass

if __debug__: # True si le programme a été appelé SANS l'option -o
    Player._init_debug()
