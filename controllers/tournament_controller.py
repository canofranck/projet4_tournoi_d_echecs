from models.tournament_model import Tournament
from models.player_model import Player
from controllers.round_controller import roundController
from views.main_view import MainView
from views.tournament_view import TournamentView
import constantes
from constantes import TO_LAUNCH, IN_PROGRESS


class TournamentController:
    """Contrôleur pour la gestion des tournois."""

    def __init__(self):
        """Initialise le contrôleur des tournois."""
        self.tournaments = []
        self.tournament_view = TournamentView()
        self.main_view = MainView()
        self.round_controller = roundController()

    def load_tournaments(self):
        """Charge les tournois depuis le fichier et met à jour self.tournaments."""
        self.tournaments = Tournament.load_tournaments()

    def run_tournament_menu(self):
        """Exécute le menu des tournois.
        Cette méthode permet de gérer les actions du menu des tournois,
        notamment la création de nouveaux tournois, l'affichage de la liste des
        tournois et la sortie du menu.
        Args:
            main_view (obj): La vue principale de l'application.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        self.main_view.clear_screen()
        while True:
            choice = self.tournament_view.display_tournament_menu()

            if choice == constantes.TOURNAMENT_MENU_NOUVEAU:
                self.create_tournament()
            elif choice == constantes.TOURNAMENT_MENU_AFFICHER:
                self.display_tournaments()
            elif choice == constantes.TOURNAMENT_MENU_LANCER:
                self.launch_tournament_menu()
            elif choice == constantes.TOURNAMENT_MENU_REPRENDRE:
                self.resume_tournament_menu()
            elif choice == constantes.TOURNAMENT_MENU_QUIT:
                break
            else:
                self.tournament_view.display_invalid_option_message()

    def create_tournament(self):
        """Crée un nouveau tournoi.
        Cette méthode permet de créer un nouveau tournoi et l'ajoute à la liste
        des tournois.
        Args:
            Aucun argument requis.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        self.main_view.clear_screen()
        print("Création d'un nouveau tournoi...")
        tournament_data = self.tournament_view.get_tournament_data()
        tournament_name = tournament_data["tournament_name"]
        location = tournament_data["location"]
        tournament_date = tournament_data["tournament_date"]
        number_of_tours = tournament_data["number_of_tours"]
        description = tournament_data["description"]
        tournament_id = tournament_data["tournament_id"]
        # Utilise la méthode select_players_for_tournament pour permettre à l'utilisateur de sélectionner les joueurs

        players_ids = self.select_players_for_tournament()

        new_tournament = Tournament(
            tournament_name=tournament_name,
            location=location,
            tournament_date=tournament_date,
            number_of_tours=number_of_tours,
            description=description,
            players_ids=players_ids,
            tournament_id=tournament_id,
        )
        self.tournaments.append(new_tournament)
        new_tournament.save_instance()
        print("Tournoi créer avec succès dans la sauvegarde!")
        return new_tournament

    def display_tournaments(self):
        """Affiche la liste des tournois.
        Cette méthode affiche la liste de tous les tournois par ordre
        alphabétique en fonction de leur nom.
        Args:
            Aucun argument requis.
        Returns:
            output_string (str): Une chaîne de caractères contenant la liste
                                 de tous les tournois.
        Raises:
            Aucune exception n'est levée.
        """
        self.main_view.clear_screen()
        tournaments = Tournament.load_tournaments()
        self.tournament_view.afficher_list(tournaments)

    def select_players_for_tournament(self):
        """Permet à l'utilisateur de sélectionner les joueurs pour un tournoi."""
        players = Player.load_players()

        selected_players = []
        print("Liste des joueurs disponibles:")
        for i, player in enumerate(players, start=1):
            print(f"{i}. {player.first_name} {player.last_name}")

        while True:
            try:
                selection = input(
                    "Entrez les numéros des joueurs sélectionnés, séparés par des virgules: "
                )
                selected_indices = [int(index) - 1 for index in selection.split(",")]
                selected_players = [players[index] for index in selected_indices]
                break
            except (ValueError, IndexError):
                print("Saisie invalide. Veuillez réessayer.")
        return [player.player_id for player in selected_players]

    def launch_tournament_menu(self):
        """Affiche les tournois existants et non terminés, puis permet de lancer un tournoi."""
        self.main_view.clear_screen()
        self.load_tournaments()
        # Filtrer les tournois non terminés

        ongoing_tournaments = [
            t for t in self.tournaments if t.etat_tournoi == TO_LAUNCH
        ]

        if not ongoing_tournaments:
            TournamentView.display_no_available_tournaments()
            return
        TournamentView.display_ongoing_tournaments(ongoing_tournaments)

        try:
            choice = int(
                input("Veuillez sélectionner le numéro du tournoi à lancer : ")
            )
            if 1 <= choice <= len(ongoing_tournaments):
                selected_tournament_index = choice - 1
                selected_tournament = ongoing_tournaments[selected_tournament_index]
                self.start_selected_tournament(selected_tournament)
            else:
                TournamentView.display_invalid_choice()
        except ValueError:
            TournamentView.display_invalid_choice()

    def start_selected_tournament(self, tournament):
        """Démarre le tournoi sélectionné."""

        # Modifie l'état du tournoi

        if tournament.etat_tournoi == TO_LAUNCH:
            tournament.start_tournament(tournament.tournament_id)

            # Obtenir la liste des joueurs inscrits au tournoi

            players_ids = tournament.players_ids

            # Appel au contrôleur de round pour débuter l'entrée des résultats

            self.round_controller.start_rounds(
                tournament, tournament.tournament_id, players_ids
            )

        elif tournament.etat_tournoi == IN_PROGRESS:
            print("Le tournoi est déjà en cours.")
        else:
            print(
                "Le tournoi ne peut pas être lancé dans son état actuel."
            )

    def resume_tournament_menu(self):
        """Affiche les tournois en cours et permet à l'utilisateur de choisir
        le tournoi à reprendre.
        """
        self.main_view.clear_screen()
        self.load_tournaments()
        ongoing_tournaments = [
            t for t in self.tournaments if t.etat_tournoi == IN_PROGRESS
        ]

        if not ongoing_tournaments:
            TournamentView.display_ongoing_tournaments(ongoing_tournaments)
            return
        print("Tournois en cours (IN PROGRESS) :")
        for i, tournament in enumerate(ongoing_tournaments, start=1):
            print(f"{i}. {tournament.tournament_name}")
        try:
            choice = int(
                input("Veuillez sélectionner le numéro du tournoi à reprendre : ")
            )
            if 1 <= choice <= len(ongoing_tournaments):
                selected_tournament_index = choice - 1
                selected_tournament = ongoing_tournaments[selected_tournament_index]
                self.resume_selected_tournament(selected_tournament)
            else:
                TournamentView.display_invalid_choice()
        except ValueError:
            TournamentView.display_invalid_choice()

    def resume_selected_tournament(self, tournament):
        """Reprendre un tournoi sélectionné."""
        # Obtenir la liste des joueurs inscrits au tournoi

        players_ids = tournament.players_ids
        # Appel au contrôleur de round pour reprendre l'entrée des résultats

        self.round_controller.resume_rounds(tournament.tournament_id, players_ids)

    def load_tournaments_with_rounds(self):
        """Charge les tournois avec les informations sur les rounds depuis le fichier
        et met à jour self.tournaments.
        """
        self.tournaments = Tournament.load_tournaments_with_rounds()
