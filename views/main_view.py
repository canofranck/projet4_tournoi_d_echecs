class MainView:
    @staticmethod
    def display_main_menu():
        """
        Affiche le menu principal.
        Returns:
            str: Le choix de l'utilisateur.
        """
        print("\nMenu :")
        print("1. Gestion des joueurs")
        print("2. Gestion des tournois")
        print("3. Rapports")
        print("4. Quitter")
        return input("Choisissez une option : ")

    @staticmethod
    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée.
        """
        print("Option invalide. Veuillez choisir une option valide.")
