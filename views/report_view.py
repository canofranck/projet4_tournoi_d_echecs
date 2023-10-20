class ReportView:
    @staticmethod
    def display_report_menu():
        """
        Affiche le menu des rapports.
        Returns:
            str: Le choix de l'utilisateur.
        """
        print("\nMenu de Rapports :")
        print("1. Liste de tous les joueurs par ordre alphabétique")
        print("2. Liste de tous les tournois")
        print("3. Détails d'un tournoi donné")
        print("4. Liste des joueurs d'un tournoi par ordre alphabétique")
        print("5. Liste de tous les tours d'un tournoi et de tous les matchs du tournoi")
        print("6. Revenir au menu principal")
        return input("Choisissez une option : ")

    @staticmethod
    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée pour les rapports.
        """
        print("Option invalide. Veuillez choisir une option valide pour les rapports.")

    # Ajoutez d'autres fonctions pour l'affichage des différents rapports ici
    @staticmethod
    def prompt_save_report():
        """
        Demande à l'utilisateur s'il souhaite sauvegarder le rapport.
        Returns:
            str: La réponse de l'utilisateur (O/N).
        """
        return input("Voulez-vous sauvegarder ce rapport ? (O/N) : ")

    @staticmethod
    def get_file_name_to_save():
        """
        Demande à l'utilisateur d'entrer le nom du fichier pour sauvegarder le rapport.
        Returns:
            str: Le nom du fichier de rapport.
        """
        return input("Entrez le nom du fichier de rapport : ")

    @staticmethod
    def display_report_saved_message(file_path):
        """
        Affiche un message indiquant que le rapport a été sauvegardé avec succès.
        Args:
            file_path (str): Le chemin du fichier où le rapport a été sauvegardé.
        """
        print(f"Rapport sauvegardé avec succès dans {file_path}")

    @staticmethod
    def display_report_not_saved_message():
        """
        Affiche un message indiquant que le rapport n'a pas été sauvegardé.
        """
        print("Le rapport n'a pas été sauvegardé.")
