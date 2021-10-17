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
    def __init__(self, tournament_name, location, dates,timecontrol,
                 number_of_rounds=4, description = None, players: list[Player]=PLAYERS):

        self.tournament_name = tournament_name
        self.location = location
        self.dates = dates
        self.players = players
        self.number_of_rounds = number_of_rounds
        self.timecontrol = timecontrol
        self.description = description
        self.rounds = []
   
    def __repr__(self):
        return f"({self.tournament_name}, {self.location}, {self.dates},{self.timecontrol}, {self.number_of_rounds}, {self.description},{self.players})"
            
    def __str__(self):
        return f"({self.tournament_name}, {self.location}, {self.dates},{self.timecontrol}, {self.number_of_rounds}, {self.description},{self.players})"

    def t_serialization(self):
        keys = ("nom","lieu","dates","contrôle du temps", "nombre de tours", "description")
        values = f"{self.tournament_name}, {self.location}, {self.dates},{self.timecontrol}, {self.number_of_rounds}, {self.description}"
        values_list = values.split(',') # on doit laisser players sous forme de liste séparée
        dict_for_t = dict(zip(keys,values_list))
        return dict_for_t
        
    def tournament_players(self) -> list :
        """ renvoie la liste des dict player_data comprenant nom, prénom, date de naissance, genre, rang """
        tournament_players = []
        for p in self.players:
            player_data = p.player_serialization()
            tournament_players.append(player_data)
        return tournament_players
    
    # def t_players_view_infos déplacé vers view.py

    def create_list_by_rating(self):
        """tri les joueurs du tournoi par classement/rang"""
        players_by_rating = sorted(self._players, key=lambda k: k["rang"], reverse=True)
        # rendre player_by_rating lisible (vue?) ou une classe pour améliorer l'affichage__str__?
                
        return players_by_rating

    def create_pairs_round1(self): 
        """Créé des matchs basés sur le classement des joueurs pour le round 1"""
        # une fonction "split" quand le reste marchera? sert aussi plus tard

        if len(self.players) % 2 != 0:
            raise Exception("Impossible de générer des appairages avec un nombre impair de joueurs")

        half = len(self.players) // 2
        first_half = self.players_by_rating[:half]
        second_half = self.players_by_rating[half:]

        # création des matchs
        matchs_round1 = zip(first_half, second_half)

        # liste des matchs
        pairings = []
        for first_half, second_half in zip(first_half, second_half):
            pairings.append(first_half, second_half)
        return pairings

    def create_pairs2(self, tournament_players):
        pass
        
    @staticmethod
    def _init_debug():
        test_tournament1 = Tournament(
        tournament_name="Tournoi de Paris",
        location="Paris",
        dates="Du 10 au 12 juin 2022",
        players = PLAYERS,
        timecontrol="blitz",
        number_of_rounds=4,
        description="C'est pas gagné!")
        
        test_tournament2 = Tournament(
        tournament_name="Tournoi des Tsars",
        location="Moscou",
        dates="Le 15 août 2022",
        players = PLAYERS,
        timecontrol="bagare", # erreurs exprès à traiter avec except etc
        number_of_rounds=2, # erreurs exprès à traiter avec except etc
        description="")

        for t in (test_tournament1, test_tournament2):
            TOURNAMENTS.append(t)


if __name__ == "__main__":
    print ("\n\nEssais sur Tournament...\n")        

if __debug__: # True si le programme a été appelé SANS l'option -o
    Tournament._init_debug()
    print("\n Voici les informations du tournoi test :\n")    
    present_tournament = TOURNAMENTS[0]
       
    # vue des infos du tournoi en propre sans les joueurs:
    t_infos_dict = present_tournament.t_serialization()
    print("\n\nInfos du présent tournoi:\n")
    for key, value in t_infos_dict.items():
        print(f"{key} : {value}")

    # maintenant les joueurs :
    t_players = present_tournament.tournament_players() # comment il peut récupérer l'info self.player tout seul?
    print("\nLes joueurs du tournoi sont:")
    t_players_view_infos = present_tournament.t_players_view_infos(t_players)
    
    t_players_by_rating = present_tournament.create_list_by_rating(t_players)
    for pbr in t_players_by_rating:
        print(pbr)

    # création des matchs du round 1 :
    matchs_round1 = present_tournament.create_pairs_round1(t_players_by_rating)

    print("Saisie des scores :")
    for pbr in t_players_by_rating: # à remplacer par l'ordre alphabétique ou les paires des matchs
        joueur = str(pbr)[:-9]
        print(f"Veuillez saisir le score de {joueur} :")
        score_joueur = input()
        print(f"Le score de {joueur} est de {score_joueur}") #comment demander validation?
    # et il faut sauver


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
