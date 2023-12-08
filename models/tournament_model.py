import os
import json
# from constantes import DATA_FOLDER
# from constantes import FILE_NAME
from constantes import TO_LAUNCH, IN_PROGRESS, FINISH


class Tournament:
    """Use to create an instance of a tournament"""
    FILE_PATH = "data/tournament.json"
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
        etat_tournoi=None
    ):
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

        # Incrémente le compteur d'ID et l'assigne à l'instance actuelle
        # self.load()
        # Si l'ID n'est pas spécifié, utilise le prochain ID disponible
        if tournament_id is None:
            self.tournament_id = Tournament.get_next_tournament_id()
        else:
            self.tournament_id = tournament_id

    @staticmethod
    def load():
        # Charge les données depuis le fichier JSON
        if os.path.exists(Tournament.FILE_PATH):
            with open(Tournament.FILE_PATH, 'r') as file:
                return json.load(file)
        return []

    def to_dict(self):
        """Convertit l'objet Tournament en un dictionnaire."""
        # Crée une liste vide pour stocker les données des tours du tournoi
        list_of_tours_data = []

        # Parcours la liste des tours du tournoi
        for tour in self.list_of_tours:
            try:
                # Tente de convertir chaque tour en un dictionnaire en appelant sa méthode to_dict()
                list_of_tours_data.append(tour.to_dict())
            except AttributeError:
                # Si le tour n'a pas de méthode to_dict(), ajoute simplement le tour à la liste
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
            "tournament_id": self.tournament_id
        }

    def save(self):
        """Sauvegarde l'objet Tournament dans un fichier JSON."""
        file_path = Tournament.FILE_PATH
        tournament_dict = self.to_dict()

        # Chargez les données existantes à partir du fichier JSON
        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)

        # Ajoutez le dictionnaire actuel à la liste existante
        existing_data.append(tournament_dict)

        # Créez le dossier data s'il n'existe pas
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Sauvegardez la liste mise à jour dans un fichier JSON
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=2)

    @staticmethod
    def get_next_tournament_id():
        """Récupère le prochain ID de tournoi à partir du fichier JSON."""
        data = Tournament.load()
        # Vérifie si la liste data est vide
        if not data:
            return 1  # Si le fichier n'existe pas, c'est le premier tournoi

        # Les données sont maintenant stockées dans une liste, récupérons le dernier élément
        last_tournament = data[-1]

        # Si 'tournament_id' est présent dans le dernier tournoi, incrémentez-le, sinon, commencez à 1
        return last_tournament.get('tournament_id', 0) + 1

    @staticmethod
    def load_tournaments():
        """Charge la liste des tournois depuis le fichier JSON."""
        file_path = Tournament.FILE_PATH

        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return [Tournament.from_dict(tournament_data) for tournament_data in data]

        return []

    @classmethod
    def from_dict(cls, tournament_data):
        """Crée une instance de Tournament à partir d'un dictionnaire."""
        return cls(**tournament_data)

    def start_tournament(self, tournament_id):
        """Démarre le tournoi en mettant à jour l'état."""
        if self.etat_tournoi == TO_LAUNCH:
            updated_values = {"etat_tournoi": IN_PROGRESS}
            Tournament.update_tournament(tournament_id, updated_values)
        else:
            print("Le tournoi ne peut pas être lancé dans son état actuel.")

    def end_tournament(self):
        """Termine le tournoi en mettant à jour l'état."""
        self.etat_tournoi = FINISH

    @staticmethod
    def save_tournaments(tournaments):
        """Sauvegarde la liste des tournois dans un fichier JSON."""
        file_path = Tournament.FILE_PATH

        # Convertir la liste des tournois en une liste de dictionnaires
        tournaments_data = [tournament.to_dict() for tournament in tournaments]

        # Créez le dossier data s'il n'existe pas
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Sauvegardez la liste des tournois dans un fichier JSON
        with open(file_path, "w") as json_file:
            json.dump(tournaments_data, json_file, indent=2)

    def add_tour_to_list(self, round):
        """Ajoute un tour à la liste des tours du tournoi."""
        self.list_of_tours.append(round)

    @classmethod
    def load_tournament_by_id(cls, tournament_id):
        """Charge un tournoi spécifique en fonction de son identifiant."""
        tournaments = cls.load_tournaments()

        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament

        # Si aucun tournoi n'est trouvé avec l'identifiant spécifié
        return None

    @staticmethod
    def update_tournament(tournament_id, updated_values):
        """Met à jour les valeurs d'un tournoi spécifique."""
        tournaments = Tournament.load_tournaments()

        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                # Mettez à jour les valeurs du tournoi
                for key, value in updated_values.items():
                    setattr(tournament, key, value)

        # Sauvegardez la liste mise à jour dans le fichier JSON
        Tournament.save_tournaments(tournaments)


