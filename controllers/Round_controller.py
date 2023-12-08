from models.player_model import Player
from models.round_model import Round
from models.tournament_model import Tournament
# from datetime import datetime
import os
import json
# from constantes import DATA_FOLDER
# from constantes import FILE_NAME


class roundController:
    """Contrôleur pour la gestion des rounds dans un tournoi."""

    def start_rounds(self, tournament, tournament_id, players_ids):
        # Chargez l'instance spécifique du tournoi à partir du fichier JSON
        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        players = Player.load_players_by_ids(players_ids)  # Chargez uniquement les joueurs inscrits
        """Démarre les rounds d'un tournoi."""
        number_of_rounds = selected_tournament.number_of_tours
        # Démarrez le tournoi spécifique
        selected_tournament.start_tournament(tournament)

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"Before if: round_number={round_number}")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                # previous_results = self.get_previous_results(tournament, round_number - 1)
                print("")
                # new_round.create_pairs_based_on_results(players, previous_results)
            print(f"After if: round_number={round_number}")
            # Ajoutez le tour à la liste des tours du tournoi
            selected_tournament.add_tour_to_list(new_round)
            # tournament.add_round(new_round)
            # self.play_round(new_round)
            # Ajoutez le tour à la liste des tours du tournoi
            
            # new_round.end_round()
            print(f"Round {round_number} créé.")
            # Sauvegardez le tournoi mis à jour
            # Mettez à jour le tournoi avec les nouvelles valeurs
            Tournament.update_tournament(tournament_id, {"list_of_tours": selected_tournament.list_of_tours})
            print("tournoi save")

    def play_round(self, round):
        """Simule le déroulement des matches pour un round."""
        for match in round.matches:
            # Logique pour simuler le déroulement du match
            # ...
            print()

    def get_previous_results(self, tournament, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = {}
        for previous_round in tournament.rounds[:round_number - 1]:
            # Logique pour récupérer les résultats des matches des rounds précédents
            # ...
            print()
        return previous_results

    def to_dict(self):
        """Convertit l'objet Round en un dictionnaire."""
        return {
            "round_name": self.round_name,
            "matches": [(match.player1.to_dict(), match.player2.to_dict()) for match in self.matches],
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }

    def save(self):
        """Sauvegarde l'objet Round dans un fichier JSON."""
        file_path = "data/rounds.json"  # Vous pouvez ajuster le chemin du fichier au besoin
        round_dict = self.to_dict()

        # Chargez les données existantes à partir du fichier JSON
        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)

        # Ajoutez le dictionnaire actuel à la liste existante
        existing_data.append(round_dict)

        # Créez le dossier data s'il n'existe pas
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Sauvegardez la liste mise à jour dans un fichier JSON
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=2)
