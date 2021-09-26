from player import *

TOURNAMENTS = []


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

