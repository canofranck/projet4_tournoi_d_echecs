import os
import json
from constantes import DATA_FOLDER
from constantes import FILE_NAME


class Player:

    def __init__(self,
                 last_name,
                 first_name,
                 birth_date,
                 player_id,
                 score_tournament
                 ):
        """
        Initialise un objet Player avec les attributs spécifiés.

        Args:
            last_name (str): Le nom de famille du joueur.
            first_name (str): Le prénom du joueur.
            birth_date (str): La date de naissance du joueur.
            player_id (str): L'ID du joueur.
            ranking (int): Le classement du joueur.
            score_tournament (int): Le score du tournoi du joueur.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.player_id = player_id
        self.score_tournament = score_tournament

    @staticmethod
    def load_players():
        """Charge les joueurs à partir d'un fichier JSON.
        Cette méthode charge les joueurs à partir d'un fichier JSON spécifié.
        Les données sont lues à partir du fichier et chaque joueur est ajouté
        à la liste des joueurs.
        Args:
            FILE_NAME (str): Le nom du fichier à partir duquel charger les
                             données des joueurs.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        players = []
        Player.create_data_folder_if_not_exists()
        file_path = os.path.join(DATA_FOLDER, FILE_NAME)
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return players  # Si le fichier n'existe pas ou est vide, retourne une liste vide

        with open(file_path, 'r') as file:
            players_data = json.load(file)
            for data in players_data:
                player = Player(
                    data['last_name'],
                    data['first_name'],
                    data['birth_date'],
                    data['player_id'],
                    data['score_tournament']
                )
                players.append(player)
        return players

    def save(self):
        """Sauvegarde les joueurs dans un fichier JSON.
        Cette méthode sauvegarde la liste des joueurs dans un fichier JSON.
        Args:
            FILE_NAME (str): Le nom du fichier dans lequel les joueurs seront
                             sauvegardés.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        self.create_data_folder_if_not_exists()
        file_path = os.path.join(DATA_FOLDER, FILE_NAME)
        players = Player.load_players()
        players.append(self)
        players_data = []
        for p in players:
            players_data.append({
                    "last_name": p.last_name,
                    "first_name": p.first_name,
                    "birth_date": p.birth_date,
                    "player_id": p.player_id,
                    "score_tournament": p.score_tournament
                })
        with open(file_path, 'w') as file:  
            json.dump(players_data, file, indent=4)

    @staticmethod
    def create_data_folder_if_not_exists():
        """Crée le dossier de données s'il n'existe pas.
        Cette méthode vérifie l'existence du dossier de données et le crée
        si il n'existe pas.
        Args:
            Aucun argument requis.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

    @classmethod
    def is_player_id_taken(cls, player_id):
        """Vérifie si l'ID du joueur est déjà pris."""
        players = Player.load_players()
        for player in players:
            if player.player_id == player_id:
                return True
        return False

    @classmethod
    def load_players_by_ids(cls, players_ids):
        """Charge les joueurs avec les IDs spécifiés."""
        all_players = cls.load_players()  # Chargez tous les joueurs
        selected_players = [player for player in all_players if player.player_id in players_ids]
        return selected_players

    def to_dict(self):
        """Convertit l'objet Player en un dictionnaire."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "player_id": self.player_id,
            "score_tournament": self.score_tournament
        }

    def update_scores(self, match_result):
        """Met à jour le score du joueur en fonction du résultat du match."""
        if match_result == "win":
            self.score_tournament += 1
        elif match_result == "draw":
            self.score_tournament += 0.5
