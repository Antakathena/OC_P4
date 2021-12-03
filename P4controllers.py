import abc
import datetime
from dataclasses import dataclass
import P4models
import dbtools
import P4views


class Controller(abc.ABC):
    """Gère le stockage et la récupération d'information -> méthodes de recherche et de stockage en db
    Appelle les vues suivantes et déclenche les actions"""
    # Est-ce qu'il faut mettre des @abc.abstractmethod avant chaque?
    def __init__(self):
        self.player = P4models.Player()
        self.tournament = P4models.Tournament()

    def add_new(self):
        raise NotImplementedError

    def change(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def get_infos(self):
        """récupère dans le modèle ou la database les infos nécessaires à l'action"""
        raise NotImplementedError

    def correct_infos(self):
        """vérifier et corrige la teneur des données (types, longeur, etc)"""
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError


@dataclass
class MenuManager(Controller):
    name: str
    choices: tuple
    view: P4views.View
    start: int = 1

    def initial_manager(self):
        """On commence forcément par un menu."""
        answer = self.view.show()
        name = self.choices[answer]

        requested_manager = ManagerFactory(name).make_menu()
        return requested_manager

    def react_to_answer(self, requested_manager: Controller):
        """Récupère la réponse de l'utilisateur depuis la vue du menu.
        Créé un controleur en fonction de la demande de l'utilisateur."""

        name = requested_manager.name

        while True:
            answer = requested_manager.view.show()
            name = requested_manager.choices[answer]

            if name.startswith("Menu"):
                requested_manager = ManagerFactory(name).make_menu()
            elif name.startswith("Liste"):
                report = ReportManager()
                report.react_to_answer()
                requested_manager = ManagerFactory("Menu Rapports").make_menu()
            elif name.startswith("Selectionner les joueurs"):
                tournament = TournamentManager()
                tournament.select_players()
                requested_manager = ManagerFactory("Menu tournois").make_menu()
            elif name == "Lancer le tournoi":
                tournament = TournamentManager()
                tournament.play_tournament()
            else:
                requested_manager = ManagerFactory(name).make_form()
                answers = requested_manager.view.show()
                if "joueur" in name:
                    PlayerManager(answers).execute()
                    requested_manager = ManagerFactory("Menu joueurs").make_menu()
                if "tournoi" in name:
                    TournamentManager(answers).execute()
                    requested_manager = ManagerFactory("Menu tournois").make_menu()

    @staticmethod
    def back_to_main_menu():
        back_to_menu = ManagerFactory("Menu principal").make_menu()
        requested_manager = back_to_menu.initial_manager()
        MenuManager.react_to_answer(back_to_menu, requested_manager)


class ReportManager(Controller):
    """
    Obligatoires pour init: nom du rapport,
    optionnel: tournoi (si infos tournoi).
    Vue d'office reportview ou pas?
    """

    name: str
    start: int = 1
    tournament: str = None

    def react_to_answer(self):
        """Affiche un rapport en fonction de la demande de l'utilisateur:"""
        infos = dbtools.Report()
        view = P4views.ReportView(self.name)

        # rapports liés à un tournois:
        if self.tournament is not None:
            database = dbtools.Database()
            tournoi_dict: dict = database.get_dict_from_db(self.tournament)
            tournament_players = tournoi_dict["players"]
            controleurs = [
                ("Liste des joueurs par ordre alphabétique", infos.sort_by_name(tournament_players)[1]),
                ("Liste des joueurs par classement", infos.sort_by_rating(tournament_players)[1]),
                ("Liste des matchs", tournoi_dict["matches"])
                ("Liste des tours (déroulé du tournoi)", tournoi_dict["shifts"])
            ]
        # rapport généraux:
        else:
            controleurs = [
                ("Liste des tournois", infos.get_tournaments_list()),
                ("Liste des joueurs par ordre alphabétique", infos.sort_by_name(infos.get_players_list())[1]),
                ("Liste des joueurs par classement", infos.sort_by_rating(infos.get_players_list())[1]),
            ]

        for controleur in controleurs:
            if self.name == controleur[0]:
                action = view.show(controleur[1])
                return action()
            else:
                print("Pas de contrôleur associé à ce nom")
                return False


@dataclass
class FormManager(Controller):
    name: str
    questions: tuple
    view: P4views.View
    start: int = 1

    def react_to_answer(self):
        """lance un formulaire en fonction de la demande de l'utilisateur"""
        answers = self.view.show()
        print(answers)
        if "joueur" in self.name:
            PlayerManager(answers).execute()
            # et revenir au menu joueur
        elif "tournoi" in self.name:
            TournamentManager(answers).execute()
            # et revenir au menu tournoi
        else:
            print(f"Je ne sais pas encore quoi faire avec {self.name} ")


@dataclass
class ManagerFactory:
    """
    Réuni les informations et créé les controleurs pour les UI
    donc la base des Menus, Questionnaires et Rapports.

    """
    name: str
    start: int = 1

    def make_menu(self):
        return MenuManager(
            self.name,
            choices=P4views.MENUS_CHOICES[self.name],
            view=P4views.MenuView(self.name),
            start=self.start
        )

    def make_form(self):
        return FormManager(
            self.name,
            questions=P4views.FORMS_FIELDS[self.name],
            view=P4views.FormView(self.name),
            start=self.start
        )


class PlayerManager(Controller):

    def __init__(self, answers=None):
        self.answers = answers

    def adapt_answers(self):
        """Paramètres de Player = name, firstname, birthdate, gender, rating"""
        self.answers[0] = self.answers[0].upper()
        self.answers[1] = self.answers[1].capitalize()
        self.answers[4] = int(self.answers[4])

    def add_new(self):
        self.adapt_answers()
        try:
            player = P4models.Player(*self.answers)
        except ValueError:
            print("Informations non valides. Le joueur doit avoir entre 18 et 99 ans.")
        else:
            database = dbtools.Database()
            database.insert(dataclass_instance_to_insert=player)
            # _logger.debug("Joueur ajouté à la base ...")
            print(f"\n Joueur ajouté à la base de donnée: {player}\n")

    def execute(self):
        self.add_new()


class TournamentManager(Controller):
    def __init__(self, answers=None):
        self.answers = answers

    def adapt_answers(self):
        """
        Adapte les réponses au modèle.
        Pour rappel, les paramètres de base du tournoi sont:
        Nom, Lieu, Date de début, Date de fin, Nombre de tours,
        Contrôle du temps, Description
        """
        today = datetime.datetime.now()
        vue = P4views.ErrorMessages()
        self.answers[0] = self.answers[0].upper()
        self.answers[1] = self.answers[1].capitalize()
        if self.answers[2] > self.answers[3]:
            vue.show(0)
            MenuManager.back_to_main_menu()
        if self.answers[2] < today:
            vue.show(1)
            MenuManager.back_to_main_menu()
        if self.answers[4] == "":
            self.answers[4] = 4

    def add_new(self):
        try:
            tournament = P4models.Tournament(*self.answers)
        except ValueError:
            print("La date de début du tournoi n'est pas valide. Veuillez la vérifier.")
        else:
            database = dbtools.Database()
            database.insert(dataclass_instance_to_insert=tournament)
            print(f"\nAjout d'un tournoi à la base de donnée: {tournament}\n")

    def execute(self):
        """Ajoute un joueur dans la db depuis le formulaire"""
        self.adapt_answers()
        self.add_new()

    def select_tournament(self):
        tournamentslist = dbtools.Report.get_tournaments_list()
        tournamentslist.append("Menu principal")
        choices = tournamentslist
        vue = P4views.MenuView(name="Selectionner un tournoi:", choices=choices)
        answer = vue.show()
        if answer == len(tournamentslist) - 1:
            MenuManager.back_to_main_menu()
        else:
            tournoi_choisi = choices[answer]
            return tournoi_choisi

    def select_players(self):
        """Montre la liste des tournois pour choisir à quel tournoi on ajoute des joueurs.
        Puis demande de saisir un nom. Ajoute le nom (ça devrait suffir) à la liste players dans ce tournoi.
        Réagit si le nom y est déjà et prévient si la liste contient un nombre pair ou impair de joueurs."""
        db = dbtools.Database()
        tournoi_choisi = self.select_tournament()
        tournoi_dict: dict = db.get_dict_from_db(tournoi_choisi)
        tournoi: P4models.Tournament = P4models.Tournament(*tournoi_dict.values())
        print(tournoi)
        while True:
            players = [x for x in tournoi.players]
            P4views.PrepTournamentView.players_list(players)
            # on fait choisir parmis les joueurs dans la db:
            infos = dbtools.Report()
            players_in_db = infos.get_players_list()
            choices = infos.sort_by_name(players_in_db)[1]
            vue = P4views.MenuView(name="Selectionner le joueur", choices=choices)
            answer = vue.show()
            joueur_choisi = infos.sort_by_name(players_in_db)[0][answer]
            joueur_choisi = joueur_choisi["name"]

            if db.check_if_in_db(joueur_choisi):
                if not tournoi.add_to_playerslist(joueur=joueur_choisi):
                    print("Impossible d'ajouter ce joueur (déjà ajouté).")
                print(f"{joueur_choisi} ajouté aux joueurs du tournoi")
            answer = input("Selectionner un autre joueur? O/n")
            if answer == "O":
                continue
            else:
                break

    def play_tournament(self):
        db = dbtools.Database()
        tournoi_choisi = self.select_tournament()
        tournoi_dict: dict = db.get_dict_from_db(tournoi_choisi)
        instance_de_tournament: P4models.Tournament = P4models.Tournament(*tournoi_dict.values())
        total_scores = instance_de_tournament.initialize_total_scores()
        tournoi: str = tournoi_dict["name"]
        vue = P4views.TournamentView(name=f"Lancement du {tournoi}")
        vue.show()

        if not len(tournoi_dict["players"]) % 2 == 0:
            print("Le nombre de joueurs n'est pas pair. Impossible de lancer le tournoi.")
            return MenuManager.back_to_main_menu()

        # on peut rajouter une vue début du tour qui indique "Tour n°{shift_number} et liste des matchs":
        shift = instance_de_tournament.which_shift()  # on créé un objet round
        matches = shift.create_pairs_shift1()  # liste de tuples

        while True:
            for match in matches:
                print(f"match: {str(match)}")
            shift.update_infos(matches=matches)  # utile?
            instance_de_tournament.add_to_matches(matches=matches)  # avt intervention c'était ({"matches" = matches})
            start_time = P4views.TournamentView.start_shift(shift)  # à ajouter à infos
            shift.update_infos(start_time=start_time)
            end_time = P4views.TournamentView.end_shift(shift)
            shift.update_infos(end_time=end_time)
            scores = P4views.TournamentView.get_scores(shift, matches)  # [0] = liste de tuple, [1] = dict
            total_scores.update(scores[1])
            print(total_scores)
            shift.update_infos(scores=scores[1])  # attention: changé de scores[0] tupple vide!
            # à ce stade le dict des infos du tour est complet, on le passe au tournoi dans la db.
            shift_infos = shift.infos
            instance_de_tournament.add_to_shifts(shift_infos=shift_infos)

            shift = instance_de_tournament.which_shift(shift.shift_number)

            if shift is False:  # ça veut dire qu'on a fini le dernier tour.
                print("\nFélicitations à tous les participants ! Le tournoi est terminé.\n")
                break
            else:
                matches = shift.create_pairs2(total_scores=total_scores)
                continue

        return MenuManager.back_to_main_menu()
