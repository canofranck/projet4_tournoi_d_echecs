from os import name, system
import constantes


class MainView:
    @staticmethod
    def display_main_menu():
        """
        Affiche le menu principal.
        Returns:
            str: Le choix de l'utilisateur.
        """
        print("\nMenu :")
        print(constantes.MAIN_MENU_JOUEUR, "Gestion des joueurs")
        print(constantes.MAIN_MENU_TOUNOI, "Gestion des tournois")
        print(constantes.MAIN_MENU_REPORTS, "Rapports")
        print(constantes.MAIN_MENU_QUIT, "Quitter")
        return input("Choisissez une option : ")

    @staticmethod
    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée.
        """
        print("Option invalide. Veuillez choisir une option valide.")

    @staticmethod
    def clear_screen():
        """Clear the terminal"""
        # for windows

        if name == "nt":
            _ = system("cls")
        # for mac and linux

        else:
            _ = system("clear")
