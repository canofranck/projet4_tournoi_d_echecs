from models.player_model import Player
from models.round_model import Round
from models.tournament_model import Tournament
# from datetime import datetime
# import os
# import json
# from constantes import DATA_FOLDER
# from constantes import FILE_NAME


class roundController:
    """Contrôleur pour la gestion des rounds dans un tournoi."""

    def start_rounds(self, tournament, tournament_id, players_ids):
        # Charge l'instance spécifique du tournoi à partir du fichier JSON
        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        players = Player.load_players_by_ids(players_ids)  # Chargez uniquement les joueurs inscrits
        """Démarre les rounds d'un tournoi."""
        number_of_rounds = selected_tournament.number_of_tours
        # Démarre le tournoi spécifique
        selected_tournament.start_tournament(tournament)

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"Before if: round_number={round_number}")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                previous_results = self.get_previous_results(tournament, round_number - 1)
                print("")
                new_round.create_pairs_based_on_results(players, previous_results)
            print(f"After if: round_number={round_number}")
            # Ajoute le tour à la liste des tours du tournoi
            selected_tournament.add_tour_to_list(new_round)
            # Ajoute une impression pour vérifier la liste des tours après l'ajout
            print(f"Tours après l'ajout du tour {round_number}: {selected_tournament.list_of_tours}")
            print("avant play round")
            self.play_round(new_round)
            print("apres play round")
            print(f"Round {round_number} créé.")
            # Mets à jour le tournoi avec les nouvelles valeurs
            new_round.end_round()
            Tournament.update_tournament(tournament_id, {"list_of_tours": selected_tournament.list_of_tours})
            # Ajoute une impression pour vérifier la liste des tours après la mise à jour
            print(f"Tours après la mise à jour du tournoi : {selected_tournament.list_of_tours}")
            print("tournoi save")
            # break

    def play_round(self, round):
        """Simule le déroulement des matches pour un round."""
        for match in round.matches:
            # Logique pour simuler le déroulement du match
            # demande les scores aux utilisateurs
            print("Avant la saisie du score1")
            match.score1 = int(input(f"Score de {match.player1.first_name} {match.player1.last_name}: "))
            print("Après la saisie du score1")

            print("Avant la saisie du score2")
            match.score2 = int(input(f"Score de {match.player2.first_name} {match.player2.last_name}: "))
            print("Après la saisie du score2")
            # Mets à jour les scores des joueurs
            if match.score1 > match.score2:
                match.player1.update_scores("win")
                match.player2.update_scores("lose")
            elif match.score1 < match.score2:
                match.player1.update_scores("lose")
                match.player2.update_scores("win")
            else:
                match.player1.update_scores("draw")
                match.player2.update_scores("draw")

    def get_previous_results(self, tournament, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = []

        return previous_results

    def update_matches_in_round(self, round_number, tournament_id, updated_matches):
        # Charge l'instance spécifique du tournoi à partir du fichier JSON
        selected_tournament = Tournament.load_tournament_by_id(tournament_id)

        # Récupére le round spécifique
        round_to_update = selected_tournament.get_round_by_number(round_number)

        if round_to_update:
            # Mets à jour les matchs dans le round
            round_to_update.update_matches(updated_matches)

            # Mets à jour le tournoi avec les nouvelles valeurs
            Tournament.update_tournament(tournament_id, {"list_of_tours": selected_tournament.list_of_tours})