import os
import json
from constantes import DATA_FOLDER, FILE_NAME2, TO_LAUNCH, IN_PROGRESS, FINISH
from models.round_model import Round


class Tournament:
    """Use to create an instance of a tournament"""

    FILE_PATH = os.path.join(DATA_FOLDER, FILE_NAME2)
    tournament_counter = 0  # Compteur d'ID statique pour toute la classe

    def __init__(
        self,
        tournament_name="",
        location="",
        tournament_date="",
        number_of_tours=4,
        description="",
        players_ids=None,
        list_of_tours=None,
        tournament_id=None,
        etat_tournoi=None,
    ):
        """Initialize a Tournament instance."""
        self.tournament_name = tournament_name
        self.location = location
        self.tournament_date = tournament_date
        self.number_of_tours = max(number_of_tours, 4)  # Assure un minimum de 4 tours
        self.description = description
        self.players_ids = players_ids if players_ids is not None else []
        self.list_of_tours = list_of_tours if list_of_tours is not None else []
        # Si etat_tournoi est évalué à True (c'est-à-dire qu'il a une valeur autre que False, None, 0, ou une chaîne
        # vide), alors self.etat_tournoi prendra la valeur de etat_tournoi.

        self.etat_tournoi = etat_tournoi or TO_LAUNCH
        self.tournament_id = tournament_id

    @staticmethod
    def load():
        """Load data from the JSON file."""
        if os.path.exists(Tournament.FILE_PATH):
            with open(Tournament.FILE_PATH, "r") as file:
                return json.load(file)
        return []

    def to_dict(self):
        """Convert the Tournament object to a dictionary."""
        list_of_tours_data = []
        for tour in self.list_of_tours:
            if isinstance(tour, Round):
                # Si le tour est une instance de la classe Round

                tour_data = {
                    "round_name": tour.round_name,
                    "start_time": (
                        tour.start_time.isoformat() if tour.start_time else None
                    ),
                    "end_time": tour.end_time.isoformat() if tour.end_time else None,
                    "matches": [
                        (
                            [match.player1.player_id, match.score1],
                            [match.player2.player_id, match.score2],
                        )
                        for match in tour.matches
                    ],
                }
                list_of_tours_data.append(tour_data)
            else:
                # Sinon, ajoutez simplement le tour à la liste

                list_of_tours_data.append(tour)
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "tournament_date": self.tournament_date,
            "number_of_tours": self.number_of_tours,
            "description": self.description,
            "players_ids": self.players_ids,
            "list_of_tours": list_of_tours_data,
            "etat_tournoi": self.etat_tournoi,
            "tournament_id": self.tournament_id,
        }

    def save_instance(self):
        """Save the Tournament object to a JSON file."""
        file_path = Tournament.FILE_PATH
        tournament_dict = self.to_dict()
        # Charge les données existantes à partir du fichier JSON

        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)
        # Ajoute le dictionnaire actuel à la liste existante

        existing_data.append(tournament_dict)
        # Crée le dossier data s'il n'existe pas

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Sauvegarde la liste mise à jour dans un fichier JSON

        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=2)

    @staticmethod
    def load_tournaments():
        """Load the list of tournaments from the JSON file."""
        file_path = Tournament.FILE_PATH

        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return [
                    Tournament.from_dict(tournament_data) for tournament_data in data
                ]
        return []

    @classmethod
    def from_dict(cls, tournament_data):
        """Create an instance of Tournament from a dictionary."""
        return cls(**tournament_data)

    def start_tournament(self, tournament_id):
        """Start the tournament by updating the state."""
        if self.etat_tournoi == TO_LAUNCH:
            updated_values = {"etat_tournoi": IN_PROGRESS}
            Tournament.update_tournament(tournament_id, updated_values)
            self.etat_tournoi = IN_PROGRESS

    def end_tournament(self, tournament_id):
        """Finish the tournament by updating the state."""
        if self.etat_tournoi == IN_PROGRESS:
            updated_values = {"etat_tournoi": FINISH}
            Tournament.update_tournament(tournament_id, updated_values)

    @staticmethod
    def save_tournaments(tournaments):
        """ "Save the list of tournaments to a JSON file"""
        file_path = Tournament.FILE_PATH
        # Convertir la liste des tournois en une liste de dictionnaires

        tournaments_data = [tournament.to_dict() for tournament in tournaments]
        # Créez le dossier data s'il n'existe pas

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Sauvegardez la liste des tournois dans un fichier JSON

        with open(file_path, "w") as json_file:
            json.dump(tournaments_data, json_file, indent=2)

    def add_tour_to_list(self, round):
        """Add a round to the list of rounds in the tournament."""
        self.list_of_tours.append(round)

    @classmethod
    def load_tournament_by_id(cls, tournament_id):
        """ "Load a specific tournament based on its identifier."""
        tournaments = cls.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        # Si aucun tournoi n'est trouvé avec l'identifiant spécifié

        return None

    @staticmethod
    def update_tournament(tournament_id, updated_values):
        """Update the values of a specific tournament."""
        tournaments = Tournament.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                # Mets à jour les valeurs du tournoi

                for key, value in updated_values.items():
                    setattr(tournament, key, value)
        # Sauvegarde la liste mise à jour dans le fichier JSON

        Tournament.save_tournaments(tournaments)

    def get_round_by_number(self, round_number):
        """Retrieve a specific round by its number."""
        for i, round_data in enumerate(self.list_of_tours):
            if round_data.get("round_name") == f"Round {round_number}" and i > 0:
                return self.list_of_tours[
                    i - 1
                ]  # Utilisez get() pour éviter le KeyError
        print(
            f"Debug: Round {round_number} not found in the list of tournament rounds."
        )
        return None

    @staticmethod
    def load_tournaments_with_rounds():
        """Charge les tournois avec les informations sur les rounds depuis le fichier JSON."""
        file_path = Tournament.FILE_PATH
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return [
                    Tournament.from_dict_with_rounds(tournament_data)
                    for tournament_data in data
                ]
        return []
