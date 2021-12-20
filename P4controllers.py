import abc
import datetime
from dataclasses import dataclass
import dbtools
import P4models
import P4views


class Controller(abc.ABC):
    """
    Gère la relation avec db tools (stockage et récupération d'information)
    Appelle les méthodes des modèles (création d'objets, gestion du tournoi...)
    Appelle les vues suivantes et déclenche les actions
    """

    def add_new(self):
        raise NotImplementedError

    def adapt_answers(self):
        """
        Vérifie et corrige la teneur des données (types, longeur, etc)
        Pour transmettre correctement au modèle pour qu'il créé un objet
        """
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
                report = ReportManager(name)
                if "du tournoi" in name:
                    manager = TournamentManager()
                    chosen_tournament = manager.choose_tournament()
                    report.react_to_answer(chosen_tournament[1])
                else:
                    report.react_to_answer()
                requested_manager = ManagerFactory("Menu rapports").make_menu()

            elif name.startswith("Selectionner les joueurs"):
                tournament = TournamentManager()
                tournament.select_players()
                requested_manager = ManagerFactory("Menu tournois").make_menu()

            elif name == "Lancer le tournoi":
                tournament = PlayTournament()
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


@dataclass
class FormManager(Controller):
    name: str
    questions: tuple
    view: P4views.View
    start: int = 1

    def react_to_answer(self):
        """lance un formulaire en fonction de la demande de l'utilisateur"""
        answers = self.view.show()
        if "joueur" in self.name:
            PlayerManager(answers).execute()
        elif "tournoi" in self.name:
            TournamentManager(answers).execute()
        else:
            print(f"Je ne sais pas quoi faire avec {self.name} ")


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


@dataclass
class ReportManager(Controller):
    """
    Classe de production des rapports. En lien avec les classes du module dbtools.
    Il y a deux types de rapports :
    - ceux qui concernent toute la base de donnée (tournoi = None).
    Par exemple : les listes avec tous les joueurs.
    - ceux qui concernent un tournoi spécifique, pour lesquels il faut préciser le tournoi.
    """
    name: str
    start: int = 1

    def react_to_answer(self, tournament=None):
        """Affiche un rapport en fonction de la demande de l'utilisateur:"""
        infos = dbtools.Report()

        # rapports liés à un tournois:
        if tournament is not None:
            tournament_players = infos.get_tournament_players(tournament)
            controleurs_tournoi = [
                ("Liste des joueurs par ordre alphabétique", infos.sort_by_name(tournament_players)[1]),
                ("Liste des joueurs par classement", infos.sort_by_rating(tournament_players)[1]),
                ("Liste des matchs", infos.get_tournament_matches(tournament)),
                ("Liste des tours (déroulé du tournoi)",  infos.get_tournament_shiftsinfos(tournament))
            ]
            for controleur in controleurs_tournoi:
                if self.name == controleur[0]:
                    infos = controleur[1]
                    view = P4views.ReportView(self.name, infos)
                    view.show()
            
        # rapport généraux:
        elif tournament is None:
            controleurs = [
                ("Liste des tournois", infos.get_tournaments_list()),
                ("Liste des joueurs par ordre alphabétique", infos.sort_by_name(infos.get_players_list())[1]),
                ("Liste des joueurs par classement", infos.sort_by_rating(infos.get_players_list())[1]),
            ]
            for controleur in controleurs:
                if self.name == controleur[0]:
                    view = P4views.ReportView(self.name, controleur[1])
                    view.show()


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
        self.adapt_answers()
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

    def choose_tournament(self):
        """
        Montre la liste des tournois pour permettre d'en choisir un.
        """
        db = dbtools.Database()
        tournoi_choisi = self.select_tournament()
        tournoi_dict: dict = db.get_dict_from_db(tournoi_choisi)
        tournoi: P4models.Tournament = P4models.Tournament(*tournoi_dict.values())
        print(tournoi)
        tournoi_dict: dict = db.get_dict_from_db(tournoi_choisi)
        nom_du_tournoi: str = tournoi_dict["name"]
        return(tournoi, nom_du_tournoi)

    def select_players(self):
        """
        Montre la liste des tournois pour choisir à quel tournoi on ajoute des joueurs.
        Puis demande de saisir un nom. Ajoute le nom (ça devrait suffir) à la liste players dans ce tournoi.
        Réagit si le nom y est déjà et prévient si la liste contient un nombre pair ou impair de joueurs.
        """
        db = dbtools.Database()
        tournoi_complet = self.choose_tournament()
        tournoi = tournoi_complet[0]  # check après modif
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


class PlayTournament(Controller):
    def __init__(self):
        pass

    def play_tournament(self):
        db = dbtools.Database()
        manager = TournamentManager()
        tournoi_choisi = manager.select_tournament()
        tournoi_dict: dict = db.get_dict_from_db(tournoi_choisi)
        instance_de_tournament: P4models.Tournament = P4models.Tournament(*tournoi_dict.values())
        total_scores = instance_de_tournament.initialize_total_scores()
        tournoi: str = tournoi_dict["name"]
        vue = P4views.TournamentView(name=f"Lancement du {tournoi}")
        vue.show()

        if not len(tournoi_dict["players"]) % 2 == 0:
            print("Le nombre de joueurs n'est pas pair. Impossible de lancer le tournoi.")
            return MenuManager.back_to_main_menu()

        shift = instance_de_tournament.which_shift()
        matches = shift.create_pairs_shift1()

        while True:
            for match in matches:
                match = P4models.Match(match[0], match[1])
                print(match)
            shift.update_infos(matches=matches)
            instance_de_tournament.add_to_matches(matches=matches)  # précédemment ({"matches" = matches})
            start_time = P4views.TournamentView.start_shift(shift)
            shift.update_infos(start_time=start_time)
            end_time = P4views.TournamentView.end_shift(shift)
            shift.update_infos(end_time=end_time)
            scores = P4views.TournamentView.get_scores(shift, matches)
            total_scores.update(scores[1])  # [0] = liste de tuple, [1] = dict
            shift.update_infos(scores=scores[1])

            # à ce stade le dict des infos du tour est complet, on le passe au tournoi dans la db:
            shift_infos = shift.infos
            instance_de_tournament.add_to_shifts(shift_infos=shift_infos)

            shift = instance_de_tournament.which_shift(shift.shift_number)
            view = P4views.TournamentView()

            if shift is False:  # ajouter une vue pour récapituler le tournoi?
                view.final()
                break
            else:
                view.shift_show(nbr=shift.shift_number)
                matches = shift.create_pairs2(total_scores=total_scores)
                continue

        return MenuManager.back_to_main_menu()
