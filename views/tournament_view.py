from constantes import TO_LAUNCH, IN_PROGRESS


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

    @staticmethod
    def display_ongoing_tournaments(tournaments):
        """Affiche les tournois en cours."""
        print("Tournois en cours :\n")
        for tournament in tournaments:
            TournamentView.display_tournament(tournament)
        print()

    @staticmethod
    def display_invalid_choice():
        """Affiche un message en cas de choix invalide."""
        print("Choix invalide.")

    @staticmethod
    def display_tournament_launched(tournament_name):
        """Affiche le message indiquant que le tournoi a été lancé avec succès."""
        print(f"Le tournoi '{tournament_name}' a été lancé avec succès.\n")

    @staticmethod
    def display_tournament(tournament):
        """Affiche les détails du tournoi."""
        if tournament.etat_tournoi == TO_LAUNCH:
            etat = "À lancer"
        elif tournament.etat_tournoi == IN_PROGRESS:
            etat = "En cours"
        else:
            etat = "Terminé"

        details = (
                    f"{tournament.tournament_id}. {tournament.tournament_name} ({etat})"
                    f" - {tournament.location} - {tournament.tournament_date}\n"
                  )
        print(details)

    @staticmethod
    def display_tournament_in_progress():
        """Affiche un message indiquant qu'un tournoi est déjà en cours."""
        print("Le tournoi est déjà en cours. Vous ne pouvez pas le lancer à nouveau.\n")

    @staticmethod
    def display_tournament_cannot_start():
        """Affiche un message indiquant qu'un tournoi ne peut pas être lancé."""
        print("Le tournoi ne peut pas être lancé. Vérifiez s'il est déjà terminé ou en cours.\n")

    @staticmethod
    def display_no_available_tournaments():
        """Affiche un message indiquant qu'aucun tournoi n'est disponible."""
        print("Aucun tournoi n'est disponible.\n")
