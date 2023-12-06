from models.tournament_model import Tournament
from models.player_model import Player
from views.tournament_view import TournamentView
import constantes


class TournamentController:
    """Contrôleur pour la gestion des tournois."""

    def __init__(self):
        """Initialise le contrôleur des tournois."""
        self.tournaments = []
        self.tournament_view = TournamentView()
        # Chargez les tournois à partir du fichier JSON lors de l'initialisation
        # self.load_tournaments('tournaments.json')

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
