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
        """   
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
            self._players = players # là j'ai peut-être fait une anerie, debuggage explosif
            #mais je ne comprends pas cette dernière ligne
        """
    def __repr__(self):
            return f"({self.tournament_name}, {self.location}, {self.dates}, {self.players}, {self.number_of_rounds}, {self.description})"
            
    def __str__(self):
            return f"({self.tournament_name}, {self.location}, {self.dates},{self.players}, {self.number_of_rounds}, {self.description})"

    def tournament_players(self, c_players) -> list :
        tournament_players = []
        for p in c_players:
            player_data = p.player_serialization()
            tournament_players.append(player_data)

        for tp in tournament_players:
            print("\n\nFiche du joueur:")
            for key, value in tp.items():
                print(f"{key} : {value}")

    def create_pairs(self, tournament_players): 
        """Créé des paires basées sur le classement des joueurs pour le round 1 puis sur leurs résultats"""
        # si round 1  key =lambda k: k["rang"] :

        players_by_rating = sorted(tournament_players, key =["rang"])
        half = len(players_by_rating)//2
        first_half = players_by_rating[:half]
        second_half = players_by_rating[half:]
        for first_half, second_half in zip(first_half, second_half):
            print(f"Match entre {first_half} et {second_half}")

        
    def t_serialization(self):
        keys = ("nom","lieu","dates","joueurs du tournoi","contrôle du temps", "nombre de tours", "description")
        values = str(self)
        values_list = values.split(',')
        dict_for_t = dict(zip(keys,values_list))
        return dict_for_t

    @staticmethod
    def _init_debug():
        test_tournament1 = Tournament("Tournoi de Paris", "Paris", "Du 10 au 12 juin 2022", PLAYERS, "blitz", 4,"C'est pas gagné!")
        # problème : la description est prise pour le nombre de round si on ne les précise pas
        test_tournament2 = Tournament("Tournoi des Tsars",  "Moscou", "Le 15 Août 2022", PLAYERS, 2,"bagare" )
        for t in (test_tournament1, test_tournament2):
            TOURNAMENTS.append(t)


if __name__ == "__main__":
    print ("\n\nEssais sur Tournament...\n")        

if __debug__: # True si le programme a été appelé SANS l'option -o
    Tournament._init_debug()
    print("\n Voici les informations du tournoi test :\n")    
    for t in TOURNAMENTS:
        
        print(t)

    present_tournament = TOURNAMENTS[0]
    t_infos = present_tournament.t_serialization()
    t_players = t_infos.get("joueurs")
    print(t_players)
    #type_present_t = type(present_tournament)
    #print(type_present_t)
    tournament_players = present_tournament.tournament_players(t_players)
    
    matchs_round1 = present_tournament.create_pairs()



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
