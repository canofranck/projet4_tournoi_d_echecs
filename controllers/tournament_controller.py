from models.tournament_model import Tournament
from models.player_model import Player
from controllers.round_controller import roundController
from views.tournament_view import TournamentView
import constantes
from constantes import TO_LAUNCH, IN_PROGRESS


class TournamentController:
    """Contrôleur pour la gestion des tournois."""

    def __init__(self):
        """Initialise le contrôleur des tournois."""
        self.tournaments = []
        self.tournament_view = TournamentView()

    def load_tournaments(self):
        """Charge les tournois depuis le fichier et met à jour self.tournaments."""
        self.tournaments = Tournament.load_tournaments()

    def run_tournament_menu(self, main_view):
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
        while True:
            choice = self.tournament_view.display_tournament_menu()

            if choice == constantes.TOURNAMENT_MENU_NOUVEAU:
                self.create_tournament()
            elif choice == constantes.TOURNAMENT_MENU_AFFICHER:
                self.display_tournaments()
            elif choice == constantes.TOURNAMENT_MENU_LANCER:
                self.launch_tournament_menu()
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
        print("Création d'un nouveau tournoi...")
        tournament_data = self.tournament_view.get_tournament_data()
        tournament_name = tournament_data['tournament_name']
        location = tournament_data['location']
        tournament_date = tournament_data['tournament_date']
        number_of_tours = tournament_data['number_of_tours']
        description = tournament_data['description']
        # Utilisez la méthode select_players_for_tournament pour permettre à l'utilisateur de sélectionner les joueurs
        players_ids = self.select_players_for_tournament()

        new_tournament = Tournament(
            tournament_name=tournament_name,
            location=location,
            tournament_date=tournament_date,
            number_of_tours=number_of_tours,
            description=description,
            players_ids=players_ids
        )
        self.tournaments.append(new_tournament)
        new_tournament.save()
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
        # controller appel le model
        tournaments = Tournament.load_tournaments()
        # controller appeler la vue pour afficher les tournois
        self.tournament_view.afficher_list(tournaments)

    def select_players_for_tournament(self):
        """Permet à l'utilisateur de sélectionner les joueurs pour un tournoi."""
        players = Player.load_players()

        selected_players = []
        print("Liste des joueurs disponibles:")
        for i, player in enumerate(players, start=1):
            print(f"{i}. {player.first_name} {player.last_name} ({player.player_id})")

        while True:
            try:
                selection = input("Entrez les numéros des joueurs sélectionnés, séparés par des virgules: ")
                selected_indices = [int(index) - 1 for index in selection.split(',')]
                selected_players = [players[index] for index in selected_indices]
                break
            except (ValueError, IndexError):
                print("Saisie invalide. Veuillez réessayer.")

        return [player.player_id for player in selected_players]

    def launch_tournament_menu(self):
        """Affiche les tournois existants et non terminés, puis permet de lancer un tournoi."""
        self.load_tournaments()
        # Filtrer les tournois non terminés
        ongoing_tournaments = [t for t in self.tournaments if t.etat_tournoi == TO_LAUNCH]

        if not ongoing_tournaments:
            TournamentView.display_no_available_tournaments()
            return
        print("Tournois en cours dans lauch tournament :")
        for i, tournament in enumerate(ongoing_tournaments, start=1):
            print(f"{i}. {tournament.tournament_name}")
        TournamentView.display_ongoing_tournaments(ongoing_tournaments)

        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi à lancer : "))
            if 1 <= choice <= len(ongoing_tournaments):
                selected_tournament_index = choice - 1
                print(f"Avant la boucle : {ongoing_tournaments[selected_tournament_index].tournament_name}")
                selected_tournament = ongoing_tournaments[selected_tournament_index]
                print(f"Avant le lancement : {selected_tournament.tournament_name}")
                self.start_selected_tournament(selected_tournament)
            else:
                TournamentView.display_invalid_choice()
        except ValueError:
            TournamentView.display_invalid_choice()

    def start_selected_tournament(self, tournament):
        """Démarre le tournoi sélectionné."""
        print(f"Au début de la méthode start_selected_tournament : {tournament.tournament_name}")

        # Modifiez l'état du tournoi
        if tournament.etat_tournoi == TO_LAUNCH:
            tournament.start_tournament(tournament.tournament_id)

            # Obtenez la liste des joueurs inscrits au tournoi
            players_ids = tournament.players_ids

            # Appel au contrôleur de round pour débuter l'entrée des résultats
            round_controller = roundController()
            round_controller.start_rounds(tournament, tournament.tournament_id, players_ids)

            print("Le tournoi a été lancé avec succès.")
        elif tournament.etat_tournoi == IN_PROGRESS:
            print("Le tournoi est déjà en cours.")
        else:
            print("Le tournoi ne peut pas être lancé dans son état actuel. dans start selected tournament")

