
import re
from models.player_model import Player
from models.round_model import Round
from controllers.match_controller import MatchController
from models.tournament_model import Tournament


class roundController:
    """Contrôleur pour la gestion des rounds dans un tournoi."""

    def start_rounds(self, tournament, tournament_id, players_ids):
        # Charge l'instance spécifique du tournoi à partir du fichier JSON
        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        players = Player.load_players_by_ids(players_ids)  # Chargez uniquement les joueurs inscrits
        # print("\nDebug: Loaded players:", players)
        # print("\nDebug: Loaded tournament data:", selected_tournament.to_dict())
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
            MatchController.play_match(new_round)
            # print("apres play round")
            # print(f"Round {round_number} créé.")
            # Mets à jour le tournoi avec les nouvelles valeurs
            new_round.end_round()
            Tournament.update_tournament(tournament_id, {"list_of_tours": selected_tournament.list_of_tours})
            # Ajoute une impression pour vérifier la liste des tours après la mise à jour
            # print(f"Tours après la mise à jour du tournoi : {selected_tournament.list_of_tours}")
            user_choice = input("Continuez a entrer les resultats O/N : ")
            if user_choice.lower() == "n":
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament(tournament_id)
            selected_tournament.end_tournament(tournament_id)

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
                # print(f"Debug: Matches in round {round_data['round_name']}: {round_data['matches']}")
                previous_results.extend(round_data['matches'])

                # Afficher les paires de joueurs récupérées
                # print(f"Debug: Pairs of players for round {round_data['round_name']}:")
                # for pair in round_data['matches']:
                #     player1_id, _ = pair[0]
                #     player2_id, _ = pair[1]
                #     print(f"Pair: {player1_id} vs {player2_id}")
                break
        # print(f"Debug: Length of previous_results after loop: {len(previous_results)}")
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

        # print("Points par joueur dans camcilate points for tournament:")
        # for player_id, points in sorted_players:
        #     player = Player.get_player_by_id(player_id)
        #     if player:
        #         print(f"{player.first_name} {player.last_name}: {points} points")
        #     else:
        #         print(f"Player with ID {player_id} not found.")
        return sorted_players

    def update_player_points(self, player_points, player_id, score):
        player_points.setdefault(player_id, 0)
        player_points[player_id] += score

    def resume_rounds(self, tournament, tournament_id, players_ids):
        """Reprendre l'entrée des résultats pour les rounds d'un tournoi."""
        # Charge l'instance spécifique du tournoi à partir du fichier JSON
        selected_tournament = Tournament.load_tournament_by_id(tournament_id)
        players = Player.load_players_by_ids(players_ids)  # Chargez uniquement les joueurs inscrits
        # print("\nDebug: Loaded players:", players)
        # print("\nDebug: Loaded tournament data:", selected_tournament.to_dict())
        number_of_rounds = selected_tournament.number_of_tours
        # Reprendre l'entrée des résultats pour chaque round
       
        round_number = [int(re.search(r'Round (\d+)', tour['round_name']).group(1))
                        for tour in selected_tournament.list_of_tours]
        if round_number:
            dernier_numero_round = max(round_number)
            print("le dernier round est le : ", dernier_numero_round)
        for round_number in range(dernier_numero_round+1, number_of_rounds + 1):
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

                # print("\nprochaine pair pour le round en cours :")
                # for pair in pairs:
                #     player1 = f"{pair['player1']['last_name']} {pair['player1']['first_name']}"
                #     player2 = f"{pair['player2']['last_name']} {pair['player2']['first_name']}"
                #     print(f"Pair: {player1} vs {player2}")

            # print(f"After if: round_number={round_number}")
            # Ajoute le tour à la liste des tours du tournoi
            selected_tournament.add_tour_to_list(new_round)
            # Ajoute une impression pour vérifier la liste des tours après l'ajout
            # print(f"Tours après l'ajout du tour {round_number}: {selected_tournament.list_of_tours}")
            # print("avant play round")
            MatchController.play_match(new_round)
            # print("apres play round")
            # print(f"Round {round_number} créé.")
            # Mets à jour le tournoi avec les nouvelles valeurs
            new_round.end_round()
            Tournament.update_tournament(tournament_id, {"list_of_tours": selected_tournament.list_of_tours})
            # Ajoute une impression pour vérifier la liste des tours après la mise à jour
            # print(f"Tours après la mise à jour du tournoi : {selected_tournament.list_of_tours}")
            user_choice = input("Continuez a entrer les resultats O/N : ")
            if user_choice.lower() == "n":
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament(tournament_id)
            selected_tournament.end_tournament(tournament_id)
