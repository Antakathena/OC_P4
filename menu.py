
from controllers import Controller, PrintController
from view import MenuView, ChoiceView, TransitionMenuView


class Menu(Controller):
    def __init__(self, name, choices=None, menu_view=MenuView(1), start=1):
        self.name = name
        self.choices = choices or []
        self.menu_view = menu_view
        self.menu_view.bind(self)
        self.start = start

       
    def execute_action(self):
        while True:
            choice = self.menu_view.draw() # ajouter la vue pour dire comment quitter
            if choice == "q": # une solution pour retourner en arrière
                break
            try:
                choice = self.choices[int(choice) - self.start]
            except (TypeError, ValueError, IndexError):
                continue # retour au début de la boucle, prévoir Item pr break
            choice.execute_action()


class Choice(Controller):
    def __init__(self, controller, itemview):
        self.controller: Controller = controller
        self.itemview = itemview

    def draw(self, i):
        self.itemview.draw(i)

    def execute_action(self):
        self.controller.execute_action()
        

class MainMenu (Menu):
    def __init__(self, name="Menu Principal", choices=None):
        choices = choices or \
            [Choice(TournamentMenu(name="Menu Tournoi",
                    menu_view=TransitionMenuView(MenuView(start=1),
                    "Menu Principal > Menu Tournoi")),
                    ChoiceView("Menu Tournoi")),
             Choice(PlayerMenu(name="Menu Joueur",
                    menu_view=TransitionMenuView(MenuView(start=1),
                    "Menu Principal > Menu Joueur")),
                    ChoiceView("Menu Joueur")),
             Choice(AskReportForm(name="Demander un rapport",
                    menu_view=TransitionMenuView(MenuView(start=1),
                    "Menu Principal > Demander un rapport")),
                    ChoiceView("Demander un rapport")),
             Choice(PrintController("Choix"), ChoiceView("Saisir votre choix, pour quitter : q"))]
        super().__init__(name, choices)


class TournamentMenu(Menu):
    def __init__(self, name="Menu Tournoi", choices=None, menu_view=None, start=1):
        choices = choices or \
            [Choice(TournamentForm(name="Entrer infos tournois",
                    form_view=FormView(start=1)),
                    ChoiceView("Entrer infos tournois")),
                    # doit renvoyer un nouveau formulaire tournoi
             Choice(TournamentForm(name="Modifier infos tournois",
                    form_view=FormView(start=1)),
                    ChoiceView("Modifier infos tournois")),
                    # doit renvoyer la liste des fiches tournois modifiables (non terminés?)
                    # liste qui menera au formulaire du tournoi choisi pour le modifier
             Choice(TournamentPlayersForm(name="Selectionnez les joueurs du tournoi",
                    form_view=FormView(start=1)),
                    ChoiceView("Selectionnez les joueurs du tournoi"))
                    # lance un formulaire qui permet de récupérer un nombre pair de joueurs
                    # dans la db, pas deux fois le même
             Choice(LaunchTournamentMenu(name="Lancer le tournoi", 
                    menu_view=TransitionMenuView(MenuView(start=1),
                    "Menu Tournoi > Lancer le tournoi")),
                    ChoiceView("Lancer le tournoi")),
                    # êtes vous sur de vouloir lancer le tournoi oui/non
             Choice(PrintController("Choix"), ChoiceView("Saisir votre choix, pour quitter : q"))]
        super().__init__(name, choices, menu_view=menu_view, start=start)

class PlayerMenu(Menu):
    def __init__(self, name="Menu Principal", choices=None):
        choices = choices or \
            [Choice(PlayerForm(name="Menu Tournoi",
                    menu_view=TransitionMenuView(MenuView(start=1),
                    "Menu Principal > Menu Tournoi")),
                    ChoiceView("Menu Tournoi")),
    pass

class LaunchTournamentMenu(Menu):
    pass
        
        
"""
menu_tournoi = Menu(
    "Menu Tournoi",
    choices=[Choice(PrintController("Toto"), ChoiceView("Afficher toto"))]
)
menu_principal = Menu(
    "Menu principal",
   choices=[Choice(menu_tournoi, ChoiceView("Aller au menu toto")), 
            Choice(PrintController("Tata"), ChoiceView("Afficher tata"))]
"""



