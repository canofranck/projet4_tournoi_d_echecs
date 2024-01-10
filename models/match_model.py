class Match:
    """Initialise une instance de Match avec deux joueurs et leurs scores optionnels."""

    def __init__(self, player1, player2, score1=None, score2=None):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
