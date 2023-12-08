class Match:
    def __init__(self, player1, player2, result=None):
        self.player1 = player1
        self.player2 = player2
        self.result = result  # Peut être un tuple (score_player1, score_player2)

    def to_dict(self):
        """Convertit l'objet en un dictionnaire."""
        return {
            "player1": self.player1,
            "player2": self.player2,
            "result": self.result
        }

    @classmethod
    def from_dict(cls, match_data):
        """Crée une instance de Match à partir d'un dictionnaire."""
        player1 = match_data["player1"]
        player2 = match_data["player2"]
        result = match_data["result"]
        return cls(player1, player2, result)