from models.player_model import Player


class Match:
    """Initialise une instance de Match avec deux joueurs et leurs scores optionnels."""
    def __init__(self, player1, player2, score1=None, score2=None):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    # def to_dict(self):
    #     """Convertit l'objet en un dictionnaire.
    #     Returns:
    #         dict: Dictionnaire représentant l'objet Match.
    #     """
    #     return {
    #         "matches": [
    #             ([self.player1.player_id, self.score1], [self.player2.player_id, self.score2])
    #         ]
    #     }

    # @classmethod
    # def from_dict(cls, match_data):
    #     """Crée une instance de Match à partir d'un dictionnaire.
    #     Args:
    #         match_data (dict): Dictionnaire contenant les données du match.
    #     Returns:
    #         Match: Instance de Match créée à partir des données.
    #     """
    #     player1_id, score1 = match_data[0]  # [0]
    #     player2_id, score2 = match_data[1]  # [1]

    #     player1 = Player.load_players_by_ids(player1_id)
    #     player2 = Player.load_players_by_ids(player2_id)

    #     return cls(player1, player2, score1, score2)
