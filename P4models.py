
import abc
from dataclasses import dataclass, field
import datetime
import itertools
from pprint import pprint
from tinydb import Query, operations
import dbtools

db = dbtools.db


@dataclass  # changer pour protocol?
class Model(abc.ABC):
    """Classe abstraite: définit les méthodes communes à tous les modèles"""

    @abc.abstractmethod
    def __str__(self):
        """Défini l'apparence de l'objet pour l'utilisateur."""
        raise NotImplementedError


@dataclass
class Player(Model):
    """
    Classe des joueurs.
    Dataclass définit automatiquement les init, repr etc."""
    name: str
    firstname: str
    birthdate: datetime  # = field(default = datetime.datetime.strptime("01/01/1950", "%d/%m/%Y"))
    gender: str = field(default="h")
    rating: int = field(default=0)

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        age = dbtools.Serialization.calculate_age(value)
        if age < 18 or age > 99:
            raise ValueError
        self._birthdate = value

    def __str__(self):
        if self.gender == "h":
            titre = "Monsieur"
            birthdate_indication = "né le"
            ranking_indication = "classé"
        else:
            titre = "Madame"
            birthdate_indication = "née le"
            ranking_indication = "classée"
        return f"{titre} {self.firstname} {self.name},{birthdate_indication}\
{self.birthdate.strftime('%d/%m/%Y')},{ranking_indication} {self.rating}"


@dataclass
class Tournament(Model):
    """
    Définit la classe des tournois.
    Les joueurs sont ajoutés après création depuis la db.
    La liste des matchs et les infos sur les tours sont ajoutés au cours du tournoi.
    shifts = liste de dict contenant pour chaque round le début, la fin,
    la liste de tuples des matchs du round avec les scores
    exemple:
    [{round: 1, début: x , fin: x , matches: [j1-j5, j2-j6, j3-j7, j4-j8], scores:
    [(joueur1, score, joueur5, score), (joueur2 score, joueur6, score), etc] }
    """
    name: str
    location: str
    start_date: datetime = datetime.datetime.strptime("01/01/2025", "%d/%m/%Y")
    end_date: datetime = datetime.datetime.strptime("01/01/2025", "%d/%m/%Y")
    number_of_rounds: int = 4
    timecontrol: str = "bullet/blitz/coup rapide"
    description: str = ""
    players: list = field(default_factory=list)
    matches: list = field(default_factory=list)
    shifts: list = field(default_factory=list)

    def __str__(self):
        return f"{self.name}, à {self.location},\
 du: {self.start_date.strftime('%d/%m/%Y')} au: {self.end_date.strftime('%d/%m/%Y')},\
 {self.number_of_rounds} tours, contrôle du temps: {self.timecontrol}. {self.description}"

    def add_to_playerslist(self, joueur):
        Recherche = Query()
        # vérifier ici si joueur n'est pas dans la db
        if joueur.upper() in self.players:
            return False
        else:
            db.update(operations.add("players", [joueur.upper()]), Recherche.name == self.name)
            self.players.append(joueur)
            return True

    def which_shift(self, shift_number=0):
        """
        La fonction définit le numéro d'ordre du round au début de chaque tour
        On lui passe un objet tournoi et le numéro du tour précédent.
        Elle renvoie l'instance de Shift (nom du tournoi, numéro du tour)"""

        if shift_number <= int(self.number_of_rounds):
            shift_number += 1
            shift = Shift(self.name, shift_number)
            shift.update_infos({"Tournament": self.name, "shift_number": shift_number})
            return shift
        else:
            return False

    def add_to_matches(self, matches: list):
        """Ajoute la liste de tuples des matchs à la liste complète des matchs du tournoi."""
        Recherche = Query()
        db.update(operations.add("matches", matches), Recherche.name == self.name)
        return True

    def add_to_shifts(self, shift_infos: dict):
        """Ajoute le dictionnaire avec toutes les infos d'un tour à shift"""
        shift_infos = dbtools.Serialization.serialize_all_times(shift_infos)
        Recherche = Query()
        db.update(operations.add("shifts", [shift_infos]), Recherche.name == self.name)
        return True

    def initialize_total_scores(self) -> dict:
        total_scores = {}
        for player in self.players:
            total_scores[player] = 0
        return total_scores

    def reset_tournament(self):
        """Réinitialiser un tournoi après des tests"""
        tournoi = self.name
        # Rapidement mettre à jour une valeur:
        database.change("name", tournoi, "players", [
            'ATOME',
            'BARDOT',
            'CRUZ',
            'DOUILLET',
            'ELITE',
            'FEZ',
            'GEANT',
            'HIBOU'
            ]
            )
        database.change("name", tournoi, "matches", [])
        database.change("name", tournoi, "shifts", [])


@dataclass
class Shift(Model):
    """
    Définit la classe des tours/rondes (chess game is played in shifts), qui référence:
    le nom du tournoi en cours et  le numéro d'ordre du tour (à passer en arg)
    Et, définis au cours du round:
    début du tour (date et heure), fin du tour (date et heure), liste des matchs, scores
    qui sont ajoutés aux infos du tournoi.
    """
    tournament: str
    shift_number: int
    infos: dict = field(default_factory=dict)

    def __str__(self):
        return f"Tour n°{self.shift_number} du {self.tournament}"

    def update_infos(self, dico=None, **to_add_to_infos):
        """ Ajoute les elt d'un dico au dico infos"""
        if dico is None:
            self.infos.update(to_add_to_infos)
        else:
            # assert isinstance(dico, dict) # print("Attention: changement de syntaxe pour matches = matches et **")
            self.infos.update(dico)
        return True

    def create_pairs_shift1(self) -> list:  # (modèle -> controleur -> vue)
        """Renvoie la liste des tuples de matchs du round"""
        database = dbtools.Database()
        tournoi_dict: dict = database.get_dict_from_db(self.tournament)
        info = dbtools.Report()
        players = tournoi_dict["players"]
        info.sort_by_rating(players)
        half = len(players) // 2
        first_half = players[:half]
        second_half = players[half:]
        if len(players) % 2 != 0:
            raise Exception("Impossible de générer des appairages avec un nombre impair de joueurs")
        # liste des matchs
        matches = []
        for first_half, second_half in zip(first_half, second_half):
            # print(f"Match {first_half} vs {second_half}")
            match = first_half, second_half
            matches.append(match)
        return matches

    def create_pairs2(self, total_scores):
        players_by_scores = self.sort_by_scores(total_scores)
        sorted_list_by_score_and_rating = self.sort_by_score_and_rating(players_by_scores)
        sorted_names_list = self.simplify_list(sorted_list_by_score_and_rating)
        suggested_matches = self.suggested_matches(sorted_names_list)
        played_matches = self.get_played_matches()
        played_matches = self.change_list_to_tuple(played_matches)
        already_played = self.matches_not_ok(suggested_matches, played_matches)
        if already_played is False:
            return suggested_matches
        else:
            other_propositions = self.propose_other_matches(sorted_names_list, played_matches)
            return other_propositions

    def sort_by_scores(self, total_scores):
        """
        Entrée: variable total_scores (dict. k = joueur, v = score total durant ce tournoi)
        Sortie: liste de dict. (k = 'name', 'fistname', 'rating', 'total_score')

        """
        # récupérer les scores_totaux des joueurs:
        players_total_scores = total_scores
        database = dbtools.Database()
        tournoi_dict: dict = database.get_dict_from_db(self.tournament)

        # récupérer les noms complets avec classement:
        info = dbtools.Report()
        players = tournoi_dict["players"]
        players = info.sort_by_name(players)[0]

        # assembler les deux pour trier avec la clé qu'on veut:
        for dico_joueur in players:
            for k, v in players_total_scores.items():
                to_add = {"total_score": v}
                if k in dico_joueur.values():
                    dico_joueur.update(to_add)

        # trier par score:
        players_by_scores = sorted(players, key=lambda k: k["total_score"], reverse=True)
        return players_by_scores

    def sort_by_score_and_rating(self, players_by_scores):
        # trouver les joueurs avec le même score:
        def get_score(player):
            return player["total_score"]
        players_group = itertools.groupby(players_by_scores, get_score)

        # trier ceux avec un score égal selon leur classement:
        groups = []  # -> liste de listes correspondant aux joueurs qui ont eu le même score
        for _, group in players_group:
            groups.append(list(group))

        sorted_list_by_score_and_rating = []  # -> dict des joueurs trié par scores égaux et classement
        for group in groups:
            order_by_rating = sorted((group), key=lambda k: k["rating"], reverse=True)
            for j in order_by_rating:
                sorted_list_by_score_and_rating.append(j)
        return sorted_list_by_score_and_rating

    def simplify_list(self, list_of_dict):
        """
        On ne garde que les noms des joueurs triés
        par scores puis classement pour un même score
        """
        sorted_names_list = []
        for elt in list_of_dict:
            name = elt.get('name')
            sorted_names_list.append(name)
        return sorted_names_list

    def suggested_matches(self, sorted_names_list):
        """liste des matchs proposés: associer les joueurs par 2"""
        joueurs_x = sorted_names_list[0::2]
        joueurs_y = sorted_names_list[1::2]
        suggested_matches = []
        for joueurs_x, joueurs_y in zip(joueurs_x, joueurs_y):
            suggested_match = joueurs_x, joueurs_y
            suggested_matches.append(suggested_match)
        return suggested_matches

    def get_played_matches(self):
        database = dbtools.Database()
        tournoi_dict: dict = database.get_dict_from_db(self.tournament)
        played_matches = tournoi_dict["matches"]
        return played_matches

    def change_list_to_tuple(self, played_matches):
        played_matches_tuples = []
        for elt in played_matches:
            match = tuple(elt)
            played_matches_tuples.append(match)
        return played_matches_tuples
        # à remonter pour ne faire qu'une fois.
        # Et pourquoi ils ne sont pas en tuple dans la liste d'instance?

    def matches_not_ok(self, suggested_matches, played_matches):
        """
        Entrée: une liste de tuples
        Renvoie True si les matches proposés n'ont pas été joués, False sinon
        """
        set_propositions = set(suggested_matches)
        result = set.intersection(set_propositions, set(played_matches))
        print(f'matchs déjà joués dans les proposés: {result}')
        if len(result) != 0:
            return True
        else:
            return False

    def propose_other_matches(self, sorted_names_list, played_matches):
        """ Si des matches parmis les proposés ont déjà été joués
        on repart de la liste complète pour pouvoir associer tout le monde"""
        suggested_matches = []
        protagonists = sorted_names_list[0::2]
        search_opponent = len(protagonists)
        antagonists = sorted_names_list[1::2]
        joueur_x = protagonists.pop(0)
        antagonist = antagonists[0]
        test_opponent = antagonists[:]
        while len(suggested_matches) < search_opponent:
            # for _ in range(search_opponent):
            match = (joueur_x, antagonist)
            print(f'Match proposé: {match}')
            if not self.matches_not_ok([match], played_matches):
                # if len(set.intersection(played_matches, set(match))) == 0:
                antagonists.remove(antagonist)
                suggested_matches.append(match)
                test_opponent = antagonists[:]
                if len(protagonists) > 0:
                    joueur_x = protagonists.pop(0)
                if len(antagonists) > 0:
                    antagonist = antagonists[0]
            else:
                test_opponent.remove(antagonist)
                antagonist = test_opponent[0]
                continue
        assert len(suggested_matches) == 4
        return suggested_matches

        # trouver l'index de chaque dans la liste:
        # player_place_in_list_by_score = sorted_list.index(player)


@dataclass
class Match:
    """
    définit la classe Match
    """
    joueur_x: str
    joueur_y: str
    score_joueur_x: float = field(default=None)
    score_joueur_y: float = field(default=None)

    def __str__(self):
        if self.score_joueur_x > self.score_joueur_y:
            return f"Match {self.joueur_x} contre {self.joueur_y}. {self.joueur_x} vainqueur."
        elif self.score_joueur_x < self.score_joueur_y:
            return f"Match {self.joueur_x} contre {self.joueur_y}. {self.joueur_y} vainqueur."
        else:
            return f"Match {self.joueur_x} contre {self.joueur_y}"


if __name__ == "__main__":

    print("\n\n----------Essais sur Database:----------\n")

    database = dbtools.Database()
    rapport = dbtools.Report()
    tournois = rapport.get_tournaments_list()
    joueurs = rapport.get_players_list()
    # print(f"tournois dans la db : {tournois}")
    # print(f"joueurs dans la db : {joueurs}")

    tournoi = "Tournoi des Reines"
    tournoi = tournoi.upper()

    def reset_tournament(tournoi):
        """Réinitialiser un tournoi après des tests"""
        # Rapidement mettre à jour une valeur:
        database.change("name", tournoi, "players", [
            'ATOME',
            'BARDOT',
            'CRUZ',
            'DOUILLET',
            'ELITE',
            'FEZ',
            'GEANT',
            'HIBOU'
            ])
        database.change("name", tournoi, "matches", [])
        database.change("name", tournoi, "shifts", [])
        # database.change("name", tournoi, "number_of_rounds",4)

    reset_tournament(tournoi)
    # database.delete(tournoi)

    info = database.get_dict_from_db(tournoi)
    pprint(info)

    """
    joueurs = [
        Player("ATOME", "Adam", datetime.datetime.strptime("01/01/1971", "%d/%m/%Y"), "h", 2001 ),
        Player("BARDOT", "Brigitte", datetime.datetime.strptime("01/02/1972", "%d/%m/%Y"), "f", 1002 ),
        Player("CRUZ", "Chloé", datetime.datetime.strptime("01/01/1973", "%d/%m/%Y"), "f", 2003 ),
        Player("DOUILLET", "David", datetime.datetime.strptime("01/01/1974", "%d/%m/%Y"), "h", 2004 ),
        Player("ELITE", "Eddy", datetime.datetime.strptime("01/01/1975", "%d/%m/%Y"), "h", 1005 ),
        Player("FEZ", "Françoise", datetime.datetime.strptime("01/01/1976", "%d/%m/%Y"), "f", 2006 ),
        Player("GEANT", "George", datetime.datetime.strptime("01/01/1977", "%d/%m/%Y"), "h", 1007 ),
        Player("HIBOU", "Harry", datetime.datetime.strptime("01/01/1978", "%d/%m/%Y"), "h", 2008 )
        ]
    for joueur in joueurs:
        database.insert(joueur)
        print(joueur)
    """

    # database.change("name", "HULOT", "name","HIBOU")
