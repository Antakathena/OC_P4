import abc


class View(abc.ABC):
    @abc.abstractmethod
    def draw(self):
        """ méthode appelée par un contrôleur, affiche des choses à l'écran, les renvoie au contrôleur"""
        raise NotImplementedError


class MenuView(View):
    def __init__(self, start):
        self.start = start
        super().__init__()

    def bind(self, controller):
        self.controller = controller

    def draw(self):
        for i, choice in enumerate(self.controller.choices, start=self.start):
            choice.itemview.draw(position=i)
        return input("Votre choix : ")


class TransitionMenuView(MenuView):
    def __init__(self, next_menuview, transition_sentence):
        self.next_menuview = next_menuview
        self.transition_sentence = transition_sentence

    def bind(self, controller):
        self.next_menuview.bind(controller)

    def draw(self):
        print(self.transition_sentence)
        return self.next_menuview.draw() #choice : None = return oublié


class ChoiceView(View):
    def __init__(self, name):
        self.name = name

    def draw(self, position):
        print(f'{position}/ {self.name}')


class FromView(View):
    pass


class ReportView(View):
    pass


class PlayerView(View):
    """ Affiche les infos venant du model Player"""
    pass


class TournamentView(View):
    """ Affiche les infos venant du model Tournament"""
    def __init__(self, tournament):
        self.tournament = tournament
    
    def t_players_view_infos(self):
        """ affiche les fiches infos des joueurs du tournoi"""
        for tp in self.tournament.players: # réutilisation de PLayerView
            print("\nFiche du joueur:")
            for key, value in tp.items():
                print(f"{key} : {value}")

    def draw(self):
        self.t_players_view_infos()


"""
# Brouillon :
class MainMenu(MenuView):
    def View_Main_Menu():
        print(
        "\n \n Programme de gestion de tournois d'échec \n\n Menu Principal\n")

        main_menu = {}
        main_menu['1'] = "Créer un nouveau tournoi" 
        main_menu['2'] = "Ajouter un joueur"
        main_menu['3'] = "Afficher un rapport"
        main_menu['4'] = "Modifier le classement d'un joueur"
        main_menu['5'] = "Quitter"

        while True: 
            options = main_menu.keys()
            for entry in options: 
                print(entry, main_menu[entry])

            selection = input("\nVeuillez indiquer votre choix:") 
            if selection =='1': 
                print("Nouveau tournoi")
            elif selection == '2': 
                print("Nouveau joueur")
            elif selection == '3':
                print("Liste des rapports disponibles")
            elif selection == '4':
                print("Modifier le rang d'un joueur")
            elif selection == '5':
                print("Quitter") 
                break
            else: 
                print("\nChoix non valide. Veuillez indiquer le chiffre de la selection. \n\nMenu Principal:\n") 

    """