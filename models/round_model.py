import datetime
import random
from models.match_model import Match
from models.player_model import Player


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
        # Ajoute les matches créés au tour actuel

    def generate_pairs_for_next_round(self, players, previous_results, sorted_players):
        print("Classement des joueurs dans generate pair for next round:")
        pairs = []
        # Fonction de comparaison personnalisée pour le tri des joueurs

        def custom_sort(player_info):
            _, score, player = player_info
            return (-score, player.last_name, player.first_name)

        # Chargez les informations complètes des joueurs pour trier par nom et prénom
        sorted_players_info = [(player_id, score, Player.get_player_by_id(player_id))
                               for player_id, score in sorted_players]
        sorted_players_info = sorted(sorted_players_info, key=custom_sort)

        for player_id, points, player in sorted_players_info:
            print(f"{player.first_name} {player.last_name}: {points} points")
        print("\ndans generate pairs for next round : previous result :", previous_results)
        # Utilisé pour suivre les joueurs déjà appariés dans ce round
        paired_players = set()
        players_set = set()

        # Iteration sur chaque paire dans previous_results
        for pair in previous_results:
            # Extraction des identifiants des joueurs de la paire actuelle
            current_pair_ids = frozenset([player[0] for player in pair])

            # Ajout des identifiants à l'ensemble
            players_set.add(current_pair_ids)

        # Utilisé pour suivre les paires déjà utilisées
        used_pairs = set()

        # Les deux premiers joueurs du classement
        i = 0
        while i < len(sorted_players_info) - 1:
            player_id, points, player = sorted_players_info[i]

            # Vérifiez si le joueur a déjà été apparié
            if player_id not in paired_players:
                # Cherchez le joueur suivant disponible
                j = i + 1
                while j < len(sorted_players_info):
                    next_player_id, next_points, next_player = sorted_players_info[j]
                    next_pair = frozenset([player_id, next_player_id])

                    # Vérifie si la paire a déjà été utilisée ou si elle a été jouée au tour précédent
                    if not any(
                        next_pair == prev_pair or next_pair in used_pairs or prev_pair in used_pairs
                        for prev_pair in players_set
                    ):
                        # Ajoute les joueurs à la paire et les suivre dans l'ensemble
                        pairs.append({"player1": player.to_dict(), "player2": next_player.to_dict()})
                        paired_players.add(player_id)
                        paired_players.add(next_player_id)

                        # Ajoute la paire à l'ensemble des paires utilisées
                        used_pairs.add(next_pair)

                        # Ajoute la paire à la liste des matchs
                        match = Match(player, next_player)
                        self.matches.append(match)

                        # Supprime les joueurs appariés de la liste sorted_players_info
                        sorted_players_info = [p for p in sorted_players_info if p[0]
                                               not in (player_id, next_player_id)]

                        i = -1  # reprends a zero dans la list sorted_players_info vue que les index on changer
                        # Sort de la boucle interne une fois la paire validée
                        break

                    # Incrémente l'indice pour passer au joueur suivant
                    j += 1

                # Assure que la boucle ne continue pas indéfiniment
                i += 1

        # Ajoute la dernière paire manquante avec les joueurs restants
        if len(sorted_players_info) == 2:
            player1_id, points1, player1 = sorted_players_info[0]
            player2_id, points2, player2 = sorted_players_info[1]
            remaining_pair = frozenset([player1_id, player2_id])

            # Ajoute les joueurs à la paire et les suit dans l'ensemble
            pairs.append({"player1": player1.to_dict(), "player2": player2.to_dict()})

            # Ajoute la paire à l'ensemble des paires utilisées
            used_pairs.add(remaining_pair)

            # Ajoute la paire à la liste des matchs
            match = Match(player1, player2)
            self.matches.append(match)

        return pairs, self.matches

    def to_dict(self):
        """Convertit l'objet en un dictionnaire."""
        result = {
            "round_name": self.round_name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "matches": [
                (
                    [match.player1.player_id, match.score1],
                    [match.player2.player_id, match.score2]
                )
                for match in self.matches
            ]
        }

        return result

    @classmethod
    def from_dict(cls, round_data):
        """Crée une instance de Round à partir d'un dictionnaire."""
        round_name = round_data["round_name"]
        start_time = datetime.datetime.fromisoformat(round_data["start_time"]) if round_data["start_time"] else None
        end_time = datetime.datetime.fromisoformat(round_data["end_time"]) if round_data["end_time"] else None
        new_round = cls(round_name, start_time, end_time)

        # Modifier cette partie pour créer des instances de Match avec le format attendu
        if "matches" in round_data and isinstance(round_data["matches"], list):
            for match_data in round_data["matches"]:
                new_round.matches.append(
                    Match(
                        Player(player_id=match_data[0][0]),
                        Player(player_id=match_data[1][0]),
                        match_data[0][1],
                        match_data[1][1]
                    )
                )
        else:
            print("Invalid or missing 'matches' data in round_data")

        return new_round

    def update_matches(self, updated_matches):
        """Met à jour les matchs du round avec de nouvelles valeurs."""
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)