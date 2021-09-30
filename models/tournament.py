from player import *
from typing import List
"""
From Python 3.9 (PEP 585) onwards tuple, list and various other classes are now generic types.
Using these rather than their typing counterpart is now preferred.
From Python 3.9 you can now just do:

def f(points: tuple[float, float]):
    return map(do_stuff, points)
    
"""
TOURNAMENTS = []

class Tournament:
    """
    définit la classe Tournament, qui permet :
    de créer un nouveau tournoi
    d'organiser et de conserver les informations des tournois
    d'assembler les joueurs en paire selon les règles du tournoi Suisse (créé les nouveaux matchs)

    """
    def __init__(self, c_tournament_name, c_location, c_dates, c_players: list[Player], 
                c_timecontrol, c_number_of_rounds=4, c_description = None) :

        self.tournament_name = c_tournament_name
        self.location = c_location
        self.dates = c_dates
        self.players = c_players
        self.number_of_rounds = c_number_of_rounds
        self.timecontrol = c_timecontrol
        self.description = c_description
        self.rounds = []


    def __repr__(self):
            return f"({self.tournament_name}, {self.location}, {self.dates}, {self.players}, {self.number_of_rounds}, {self.description})"
             
    
    def __str__(self):
            # show the number of players instead of all the list? how?
            return f"({self.tournament_name}, à : {self.location}, {self.dates}, {self.number_of_rounds}, {self.description})"

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

    def create_pairs(self, this_tournament_players): 
        """Créé des paires basées sur le classement des joueurs pour le round 1 puis sur leurs résultats"""
        
        # si round 1 :
        players_by_rating = sorted(this_tournament_players, key =lambda k: k[rating])
        half = len(players_by_rating)//2
        first_half = players_by_rating[:half]
        second_half = players_by_rating[half:]
        for first_half, second_half in zip(first_half, second_half):
            print(f"Match entre {first_half} et {second_half}")

    @staticmethod
    def _init_debug():
        test_tournament = Tournament("Tournoi de Paris", "Paris", "Du 10 au 12 juin 2022", PLAYERS, "blitz") 
        TOURNAMENTS.append(test_tournament)


if __name__ == "__main__":
    print ("\n\nEssais sur Tournament...\n")        

if __debug__: # True si le programme a été appelé SANS l'option -o
    Tournament._init_debug()

    type_de_PLAYERS = type(PLAYERS)
    print(type_de_PLAYERS)
    print(PLAYERS[3])
    type_de_PLAYERS3 = type(PLAYERS[3])
    print(type_de_PLAYERS3)
    infos_joueur = str(PLAYERS[3])
    print(infos_joueur)
    type_de_infos_joueur = type(infos_joueur)
    print(type_de_infos_joueur)

    Tournament.create_dict(playerdata = infos_joueur)

    print("\n\n Voici les informations du tournoi test :\n")    
    for t in TOURNAMENTS:
        print(t)
     
    paires_round1 = test_tournament.create_pairs(PLAYERS = PLAYERS)

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
