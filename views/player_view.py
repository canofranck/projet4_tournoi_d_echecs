class PlayerView:
    @staticmethod
    def display_player_menu():
        """
        Affiche le menu de gestion des joueurs.
        Returns:
            str: Le choix de l'utilisateur.
        """
        print("\nMenu de Gestion des Joueurs :")
        print("1. Ajouter un nouveau joueur")
        print("2. Afficher tous les joueurs")
        print("3. Revenir au menu principal")
        return input("Choisissez une option : ")

    @staticmethod
    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée
        pour la gestion des joueurs.
        """
        print("Option invalide. Veuillez choisir une option valide pour la" +
              "gestion des joueurs.")

    @staticmethod
    def get_player_data():
        """
        Récupère les données d'un nouveau joueur.
        Returns:
            dict: Les données du nouveau joueur.
        """
        last_name = input("Entrez le nom de famille du joueur : ")
        first_name = input("Entrez le prénom du joueur : ")
        birth_date = input("Entrez la date de naissance du joueur" +
                           "(au format JJ/MM/AAAA) : ")
        player_id = input("Entrez l'identifiant du joueur : ")
        # ranking = input("Entrez le classement du joueur : ")
        ranking = 0
        # score_tournament=input("Entrez le score du joueur dans le tournoi: ")
        score_tournament = 0

        return {
            'last_name': last_name,
            'first_name': first_name,
            'birth_date': birth_date,
            'player_id': player_id,
            'ranking': ranking,
            'score_tournament': score_tournament
        }
