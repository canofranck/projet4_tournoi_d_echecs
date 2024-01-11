from datetime import datetime
import uuid
import constantes


class TournamentView:
    """Vue pour la gestion des tournois."""

    def display_tournament_menu(self):
        """Affiche le menu des tournois et récupère le choix de l'utilisateur."""
        print("Menu des tournois:")
        print(constantes.TOURNAMENT_MENU_NOUVEAU, "Nouveau tournoi")
        print(constantes.TOURNAMENT_MENU_AFFICHER, "Afficher les tournois")
        print(constantes.TOURNAMENT_MENU_LANCER, "Lancer un tournoi")
        print(constantes.TOURNAMENT_MENU_REPRENDRE, "Reprendre un tournoi en cours")
        print(constantes.TOURNAMENT_MENU_QUIT, "Retour au menu principal")
        choice = input("Veuillez choisir une option: ")
        return choice

    def get_tournament_data(self):
        """Récupère les données d'un nouveau tournoi auprès de l'utilisateur."""
        tournament_data = {}
        while True:
            tournament_data["tournament_name"] = input("Nom du tournoi: ")
            if tournament_data["tournament_name"]:
                break
            else:
                print("Le nom du tournoi ne peut pas être vide. Réessayez.")
        while True:
            tournament_data["location"] = input("Lieu du tournoi: ")
            if tournament_data["location"]:
                break
            else:
                print("Le lieu du tournoi ne peut pas être vide. Réessayez.")
        while True:
            tournament_data["tournament_date"] = input(
                "Date du tournoi: (au format JJ/MM/AAAA) : "
            )
            try:
                # Essayer de convertir la chaîne en objet datetime

                datetime.strptime(tournament_data["tournament_date"], "%d/%m/%Y")
                # La conversion a réussi, la date est valide

                print("La date est conforme.")
                break  # Sortir de la boucle si la date est conforme
            except ValueError:
                # La conversion a échoué, la date n'est pas valide

                print(
                    "Format de date invalide. Assurez-vous d'utiliser "
                    + "le format JJ/MM/AAAA. Réessayez."
                )
        while True:
            try:
                tournament_data["number_of_tours"] = int(input("Nombre de tours: "))
                break
            except ValueError:
                print("Le nombre de tours du  tournoi doit etre un entier. Réessayez.")
        while True:
            tournament_data["description"] = input("Description du tournoi: ")
            if tournament_data["description"]:
                break
            else:
                print("La description du tournoi ne peut pas être vide. Réessayez.")
        gen_id = str(uuid.uuid4())
        tournament_id = gen_id[:6]
        tournament_data["tournament_id"] = tournament_id

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
        for i, tournament in enumerate(tournaments):
            TournamentView.display_tournament(tournament, i)
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
    def display_tournament(tournament, index=None):
        """Affiche les détails du tournoi."""
        if tournament.etat_tournoi == constantes.TO_LAUNCH:
            etat = "TO_LAUNCH"
        elif tournament.etat_tournoi == constantes.IN_PROGRESS:
            etat = "IN_PROGRESS"
        else:
            etat = "FINISH"
        if index is not None:
            details = (
                f"{index + 1}. {tournament.tournament_name} ({etat})"
                f" - {tournament.location} - {tournament.tournament_date}\n"
            )
        else:
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
        print(
            "Le tournoi ne peut pas être lancé. Vérifiez s'il est déjà terminé ou en cours.\n"
        )

    @staticmethod
    def display_no_available_tournaments():
        """Affiche un message indiquant qu'aucun tournoi n'est disponible."""
        print("Aucun tournoi n'est disponible.\n")

    @staticmethod
    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée.
        """
        print("Option invalide. Veuillez choisir une option valide.")
