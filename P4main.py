import P4controllers
import P4views


def main():
    """ Main function: affiche l'accueil puis le menu principal."""

    welcome = P4views.Welcome()
    welcome.show()

    menu_principal = P4controllers.ManagerFactory("Menu principal").make_menu()
    requested_manager = menu_principal.initial_manager()
    P4controllers.MenuManager.react_to_answer(menu_principal, requested_manager)


if __name__ == "__main__":

    main()
