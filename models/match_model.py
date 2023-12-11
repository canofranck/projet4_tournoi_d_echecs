# import json

from models.player_model import Player


class Match:
    def __init__(self, player1, player2, score1=None, score2=None):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        """Convertit l'objet en un dictionnaire."""
        return {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "score1": self.score1,
            "score2": self.score2
        }

    @classmethod
    def from_dict(cls, match_data):
        """Crée une instance de Match à partir d'un dictionnaire."""
        player1 = Player.from_dict(match_data["player1"])
        player2 = Player.from_dict(match_data["player2"])
        score1 = match_data["score1"]
        score2 = match_data["score2"]
        return cls(player1, player2, score1, score2)
