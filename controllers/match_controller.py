# from models.player_model import Player
# from models.round_model import Round
# from models.tournament_model import Tournament


class MatchController:

    def play_match(round):
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
