import re
from models.player_model import Player
from models.round_model import Round
from controllers.match_controller import MatchController
from models.tournament_model import Tournament


class roundController:
    """Contrôleur pour la gestion des rounds dans un tournoi."""

    def start_rounds(self, tournament, tournament_id, players_ids):
        """Démarre les rounds d'un tournoi."""
        # Charge l'instance spécifique du tournoi à partir du fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        # Charge uniquement les joueurs inscrits

        players = Player.load_players_by_ids(players_ids)
        number_of_rounds = selected_tournament.number_of_tours
        print("\nce tournoi a ", number_of_rounds, " rounds")
        # Démarre le tournoi spécifique

        selected_tournament.start_tournament(tournament)

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"debut du round : {round_number}")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_id)
                previous_results = self.get_previous_results(
                    tournament_id, round_number
                )
                pairs, _ = new_round.generate_pairs_for_next_round(
                    players, previous_results, sorted_players
                )
                print("\nprochain Match pour le round en cours :\n")
                for pair in pairs:
                    player1 = f"{pair['player1']['last_name']} {pair['player1']['first_name']}"
                    player2 = f"{pair['player2']['last_name']} {pair['player2']['first_name']}"
                    print(f"Match : {player1} vs {player2}")
            selected_tournament.add_tour_to_list(new_round)
            MatchController.play_match(new_round)
            new_round.end_round()
            Tournament.update_tournament(
                tournament_id, {"list_of_tours": selected_tournament.list_of_tours}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament_final(tournament_id)
            selected_tournament.end_tournament(tournament_id)

    def get_previous_results(self, tournament_id, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = []
        # Charge les données du tournoi depuis le fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        # Renverse la liste des tours pour parcourir du dernier au premier

        reversed_rounds = reversed(selected_tournament.list_of_tours)
        # Parcourt les rounds précédents et récupère les résultats des matchs

        for round_data in reversed_rounds:
            current_round_number = round_data.get("round_number", 0)
            if current_round_number < round_number and round_data.get("matches"):
                previous_results.extend(round_data["matches"])
                break
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

            Tournament.update_tournament(
                tournament_id, {"list_of_tours": selected_tournament.list_of_tours}
            )

    def calculate_points_for_tournament(self, tournament_id):
        # Charger le tournoi spécifique

        tournament = Tournament.load_tournament_by_id(tournament_id)
        if not tournament:
            print(f"Tournament with ID {tournament_id} not found.")
            return
        player_points = {}
        for round_data in tournament.list_of_tours:
            for match_data in round_data.get("matches", []):
                for player_id, score in match_data:
                    self.update_player_points(player_points, player_id, score)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_players

    def update_player_points(self, player_points, player_id, score):
        player_points.setdefault(player_id, 0)
        player_points[player_id] += score

    def resume_rounds(self, tournament_id, players_ids):
        """Reprendre l'entrée des résultats pour les rounds d'un tournoi."""
        # Charge l'instance spécifique du tournoi à partir du fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        players = Player.load_players_by_ids(
            players_ids
        )  # Charge uniquement les joueurs inscrits
        number_of_rounds = selected_tournament.number_of_tours
        # Reprendre l'entrée des résultats pour chaque round

        round_number = [
            int(re.search(r"Round (\d+)", tour["round_name"]).group(1))
            for tour in selected_tournament.list_of_tours
        ]
        if round_number:
            dernier_numero_round = max(round_number)
            print("le dernier round est le : ", dernier_numero_round, "\n")
        for round_number in range(dernier_numero_round + 1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"debut du round : {round_number}\n")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_id)
                previous_results = self.get_previous_results(
                    tournament_id, round_number
                )
                pairs, _ = new_round.generate_pairs_for_next_round(
                    players, previous_results, sorted_players
                )
                print("\nprochain Match pour le round en cours :\n")
                for pair in pairs:
                    player1 = f"{pair['player1']['last_name']} {pair['player1']['first_name']}"
                    player2 = f"{pair['player2']['last_name']} {pair['player2']['first_name']}"
                    print(f"Match : {player1} vs {player2}")
            selected_tournament.add_tour_to_list(new_round)
            MatchController.play_match(new_round)
            # Mets à jour le tournoi avec les nouvelles valeurs

            new_round.end_round()
            Tournament.update_tournament(
                tournament_id, {"list_of_tours": selected_tournament.list_of_tours}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament_final(tournament_id)
            selected_tournament.end_tournament(tournament_id)

    def calculate_points_for_tournament_final(self, tournament_id):
        # Charger le tournoi spécifique

        tournament = Tournament.load_tournament_by_id(tournament_id)
        if not tournament:
            print(f"Tournament with ID {tournament_id} not found.")
            return
        player_points = {}
        new_tournament_score = 0
        score = 0
        for round_data in tournament.list_of_tours:
            for match_data in round_data.get("matches", []):
                for player_id, score in match_data:
                    player_points.setdefault(player_id, 0)
                    player_points[player_id] += score
                    # Mets à jour le score du tournoi dans le modèle Player

                    player = Player.get_player_by_id(player_id)
                    if player:
                        new_tournament_score = score
                        player.update_score_tournament(player_id, new_tournament_score)
                    else:
                        print(f"Joueur avec l'ID {player_id} non trouvé.")
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        print("Classement Final du Tournoi :\n")
        for player_id, points in sorted_players:
            player = Player.get_player_by_id(player_id)
            if player:
                print(f"{player.first_name} {player.last_name}: {points} points")
            else:
                print(f"Player with ID {player_id} not found.")
        print()
        return sorted_players
