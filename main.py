import controllers
from controllers import PrintController
from menu import Menu, Choice, MainMenu
from view import MenuView, ChoiceView

"""
menu_tournoi = Menu(
    "Menu Tournoi",
    choices=[Choice(PrintController("Toto"), ChoiceView("Afficher toto"))]
)
menu_principal = Menu(
    "Menu principal",
   choices=[Choice(menu_tournoi, ChoiceView("Aller au menu toto")), 
            Choice(PrintController("Tata"), ChoiceView("Afficher tata"))]
)

menu_principal.execute_action()
"""

MainMenu().execute_action()
