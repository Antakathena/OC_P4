
# avec une fonction :

def Afficher_Menu_Principal():
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

""" Or as a class"""

class Menu:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items or []

    def add_item(self, item):
        self.items.append(item)
        if item.parent != self:
            item.parent = self

    def remove_item(self, item):
        self.items.remove(item)
        if item.parent == self:
            item.parent = None

    def draw(self):
        print(self.label)
        for item in self.items:
            item.draw()


class Item:
    def __init__(self, name, function, parent=None):
        self.name = name
        self.function = function
        self.parent = parent
        if parent:
            parent.add_item(self) # use add_item instead of append, since who
                                  # knows what kind of complex code you'll have
                                  # in add_item() later on.

    def draw(self):
        # might be more complex later, better use a method.
        print("    " + self.name)