
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
        print("\nDebug: Loaded players:", players)
        print("\nDebug: Loaded tournament data:", selected_tournament.to_dict())
        """Démarre les rounds d'un tournoi."""
        number_of_rounds = selected_tournament.number_of_tours
        print("\nce tournoi a ", number_of_rounds, " tours")
        # Démarre le tournoi spécifique
        selected_tournament.start_tournament(tournament)

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"debut du round_number={round_number}")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_id)
               
                previous_results = self.get_previous_results(tournament_id, round_number)
                # print("\nDebug: after fonction previous result\n")
                # print("\napres get previous result :", previous_results)
                
                # new_round.create_random_pairs(players)
                
                pairs, _ = new_round.generate_pairs_for_next_round(players, previous_results, sorted_players)
                
                print("\nprochaine pair pour le round en cours :")
                for pair in pairs:
                    player1 = f"{pair['player1']['last_name']} {pair['player1']['first_name']}"
                    player2 = f"{pair['player2']['last_name']} {pair['player2']['first_name']}"
                    print(f"Pair: {player1} vs {player2}")

            # print(f"After if: round_number={round_number}")
            # Ajoute le tour à la liste des tours du tournoi
            selected_tournament.add_tour_to_list(new_round)
            # Ajoute une impression pour vérifier la liste des tours après l'ajout
            # print(f"Tours après l'ajout du tour {round_number}: {selected_tournament.list_of_tours}")
            # print("avant play round")
            self.play_round(new_round)
            # print("apres play round")
            # print(f"Round {round_number} créé.")
            # Mets à jour le tournoi avec les nouvelles valeurs
            new_round.end_round()
            Tournament.update_tournament(tournament_id, {"list_of_tours": selected_tournament.list_of_tours})
            # Ajoute une impression pour vérifier la liste des tours après la mise à jour
            # print(f"Tours après la mise à jour du tournoi : {selected_tournament.list_of_tours}")
            print("\ntournoi save & FIN DU ROUND")
        self.calculate_points_for_tournament(tournament_id)        
        # break

    def play_round(self, round):
        """Simule le déroulement des matches pour un round."""
        for match in round.matches:
            # Logique pour simuler le déroulement du match
            # demande les scores aux utilisateurs
            
            print(f"Entrez le score pour "
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

            # Mettez à jour les scores des joueurs dans le tournoi
            for player_id, score in match_result:
                player = next(player for player in [match.player1, match.player2] if player.player_id == player_id)
                player.update_scores(score)

    def get_previous_results(self, tournament_id, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = []
       
        # Charge les données du tournoi depuis le fichier JSON
        selected_tournament = Tournament.load_tournament_by_id(tournament_id)

        # Renverse la liste des tours pour parcourir du dernier au premier
        reversed_rounds = reversed(selected_tournament.list_of_tours)

        # Parcourt les rounds précédents et récupère les résultats des matchs
        print(f"Debug: Getting previous results for round {round_number-1}")

        for round_data in reversed_rounds:
            current_round_number = round_data.get("round_number", 0)

            if current_round_number < round_number and round_data.get("matches"):
                print(f"Debug: Matches in round {round_data['round_name']}: {round_data['matches']}")
                previous_results.extend(round_data['matches'])

                # Afficher les paires de joueurs récupérées
                print(f"Debug: Pairs of players for round {round_data['round_name']}:")
                for pair in round_data['matches']:
                    player1_id, _ = pair[0]
                    player2_id, _ = pair[1]
                    print(f"Pair: {player1_id} vs {player2_id}")
                break
        print(f"Debug: Length of previous_results after loop: {len(previous_results)}")
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

    # def generate_pairs_for_next_round(self, players, previous_results):
    #     """
    #     Trie les joueurs par le nombre total de points dans le tournoi.

    #     Args:
    #         players (list): Liste des joueurs à trier.
    #         previous_results (list): Résultats des rounds précédents pour éviter les matchs identiques.

    #     Returns:
    #         list: Liste de paires de joueurs pour le prochain round.
    #     """
    #     # Triez les joueurs par nombre total de points
    #     sorted_players = sorted(players, key=lambda x: x.score_tournament, reverse=True)

    #     # Initialisez la liste de paires
    #     pairs = []

    #     # Divisez les joueurs en groupes en fonction du nombre de points
    #     groups = {}
    #     for player in sorted_players:
    #         groups.setdefault(player.score_tournament, []).append(player)

    #     # Associez aléatoirement les joueurs dans chaque groupe
    #     for group_players in groups.values():
    #         random.shuffle(group_players)

    #     # Créez les paires en associant les joueurs de chaque groupe
    #     while any(len(group_players) > 1 for group_players in groups.values()):
    #         for group_players in groups.values():
    #             if len(group_players) > 1:
    #                 player1 = group_players.pop(0)
    #                 player2 = group_players.pop(0)

    #                 # Vérifiez si les joueurs dans la paire ont déjà joué ensemble
    #                 pair_exists = any(
    #                     (player1.player_id, player2.player_id) in result or
    #                     (player2.player_id, player1.player_id) in result
    #                     for result in previous_results
    #                 )

    #                 # Si la paire existe, prenez le joueur suivant dans le classement
    #                 while pair_exists:
    #                     if group_players:
    #                         player2 = group_players.pop(0)
    #                         pair_exists = any(
    #                             (player1.player_id, player2.player_id) in result or
    #                             (player2.player_id, player1.player_id) in result
    #                             for result in previous_results
    #                         )
    #                     else:
    #                         break

    #                 if not pair_exists:
    #                     pairs.append({"player1": player1.to_dict(), "player2": player2.to_dict()})
    #                     match = Match(player1, player2)
    #                     matches.append(match)

    #     return pairs, self.matches
        
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

        print("Points par joueur :")
        for player_id, points in sorted_players:
            player = Player.get_player_by_id(player_id)
            if player:
                print(f"{player.first_name} {player.last_name}: {points} points")
            else:
                print(f"Player with ID {player_id} not found.")
        return sorted_players
    
    def update_player_points(self, player_points, player_id, score):
        player_points.setdefault(player_id, 0)
        player_points[player_id] += score
