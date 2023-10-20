class Player:

    def __init__(self,
                 last_name,
                 first_name,
                 birth_date,
                 player_id,
                 ranking,
                 score_tournament
                 ):
        """
        Initialise un objet Player avec les attributs spécifiés.

        Args:
            last_name (str): Le nom de famille du joueur.
            first_name (str): Le prénom du joueur.
            birth_date (str): La date de naissance du joueur.
            player_id (str): L'ID du joueur.
            ranking (int): Le classement du joueur.
            score_tournament (int): Le score du tournoi du joueur.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.player_id = player_id
        self.ranking = ranking
        self.score_tournament = score_tournament
