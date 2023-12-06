class TournamentView:
    """Vue pour la gestion des tournois."""

    def display_tournament_menu(self):
        """Affiche le menu des tournois et récupère le choix de l'utilisateur."""
        print("Menu des tournois:")
        print("1. Nouveau tournoi")
        print("2. Afficher les tournois")
        print("3. Lancer un tournoi")
        print("4. pour. Quitter")
        choice = input("Veuillez choisir une option: ")
        return choice

    def get_tournament_data(self):
        """Récupère les données d'un nouveau tournoi auprès de l'utilisateur."""
        tournament_data = {}
        tournament_data['tournament_name'] = input("Nom du tournoi: ")
        tournament_data['location'] = input("Lieu du tournoi: ")
        tournament_data['tournament_date'] = input("Date du tournoi: ")
        tournament_data['number_of_tours'] = int(input("Nombre de tours: "))
        tournament_data['description'] = input("Description du tournoi: ")
        # tournament_data['players_ids'] = input("Liste des ID des joueurs séparés par des virgules: ").split(',')
        return tournament_data

    def afficher_list(self, tournaments):
        """Affiche la liste des tournois."""
        print("\nListe des tournois:")
        for tournament in tournaments:
            print(f"- {tournament.tournament_name}")
        print()
