import datetime
import random
from models.match_model import Match


class Round:
    def __init__(self, round_name, start_time=None, end_time=None):
        self.round_name = round_name
        self.start_time = start_time or datetime.datetime.now()
        self.end_time = end_time
        self.matches = []

    def start_round(self):
        """Démarre le round."""
        self.start_time = datetime.datetime.now()

    def end_round(self):
        """Termine le round."""
        self.end_time = datetime.datetime.now()

    def create_random_pairs(self, players):
        """Crée des paires aléatoires pour le round."""
        random.shuffle(players)
        pairs = [(players[i], players[i + 1]) for i in range(0, len(players), 2)]
        
        # Initialise la liste des matches dans le tour
        self.matches = []
        
        for pair in pairs:
            player1 = pair[0]
            player2 = pair[1]
            
            # Crée un objet Match et ajoute-le à la liste des matches du tour
            match = Match(player1, player2)
            self.matches.append(match)

            print(f"{player1.first_name} {player1.last_name} vs {player2.first_name} {player2.last_name}")

    def create_pairs_based_on_results(self, players, previous_results):
        """Crée des paires en fonction des résultats précédents."""
        # Logique pour créer des paires basées sur les résultats précédents
        # ...

    def to_dict(self):
        """Convertit l'objet en un dictionnaire."""
        return {
            "round_name": self.round_name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "matches": [
                {"player1": match.player1.to_dict(), "player2": match.player2.to_dict()}
                for match in self.matches
            ]
        }

    @classmethod
    def from_dict(cls, round_data):
        """Crée une instance de Round à partir d'un dictionnaire."""
        round_name = round_data["round_name"]
        start_time = datetime.datetime.fromisoformat(round_data["start_time"]) if round_data["start_time"] else None
        end_time = datetime.datetime.fromisoformat(round_data["end_time"]) if round_data["end_time"] else None
        new_round = cls(round_name, start_time, end_time)
        return new_round

    def update_matches(self, updated_matches):
        """Met à jour les matchs du round avec de nouvelles valeurs."""
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)