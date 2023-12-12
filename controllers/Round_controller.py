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
                pairs = self.generate_pairs_for_next_round(players, previous_results)
                for pair in pairs:
                    print(f"Pair: {pair['player1']['last_name']} vs {pair['player2']['last_name']}")
                # new_round.create_pairs_based_on_results(players, previous_results)
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
            print(f"Avant la saisie du score pour "
                  f"{match.player1.first_name} {match.player1.last_name} vs "
                  f"{match.player2.first_name} {match.player2.last_name}")

            # Saisie des scores par les utilisateurs
            score1 = int(input(f"Score de {match.player1.first_name} {match.player1.last_name}: "))
            score2 = int(input(f"Score de {match.player2.first_name} {match.player2.last_name}: "))

            # Mettez à jour les scores des joueurs
            match.score1 = score1
            match.score2 = score2

            if score1 > score2:
                match_result = ((match.player1.player_id, 1), (match.player2.player_id, 0))
            elif score1 < score2:
                match_result = ((match.player1.player_id, 0), (match.player2.player_id, 1))
            else:
                match_result = ((match.player1.player_id, 0.5), (match.player2.player_id, 0.5))

            # Imprimez le résultat du match (vous pouvez le commenter si vous ne le voulez pas)
            print("Résultat du match:", match_result)

            # Mettez à jour les scores des joueurs dans le tournoi
            for player_id, score in match_result:
                player = next(player for player in [match.player1, match.player2] if player.player_id == player_id)
                player.update_scores(score)

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

    def generate_pairs_for_next_round(self, players, previous_results):
        """
        Trie les joueurs en fonction de leur nombre total de points dans le tournoi.

        Args:
            players (list): Liste des joueurs à trier.
            previous_results (list): Résultats des rounds précédents pour éviter les matchs identiques.

        Returns:
            list: Liste de paires de joueurs pour le prochain round.
        """
        # Triez les joueurs par nombre total de points
        sorted_players = sorted(players, key=lambda x: x.score_tournament, reverse=True)

        # Initialisez la liste de paires
        pairs = []

        # Créez des paires en associant les joueurs dans l'ordre
        for i in range(0, len(sorted_players), 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1] if i + 1 < len(sorted_players) else None

            # Évitez les matchs identiques en vérifiant les résultats précédents
            while player2 and (player1.player_id, player2.player_id) in previous_results:
                i += 1
                player2 = sorted_players[i + 1] if i + 1 < len(sorted_players) else None

            if player2:
                pairs.append({"player1": player1.to_dict(), "player2": player2.to_dict()})

        return pairs

