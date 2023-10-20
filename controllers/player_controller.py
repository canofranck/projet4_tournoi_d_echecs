import os
import json
from models.player_model import Player
from views.player_view import PlayerView

DATA_FOLDER = 'data'


class PlayerController:
    """Contrôleur pour la gestion des joueurs."""
    def __init__(self):
        """Initialise le contrôleur des joueurs."""
        self.players = []
        self.player_view = PlayerView()
        # Chargez les joueurs à partir du fichier JSON lors de l'initialisation
        self.load_players('players.json')

    def run_player_menu(self, main_view):
        """Exécute le menu des joueurs.
        Cette méthode permet de gérer les actions du menu des joueurs,
        notamment l'ajout de nouveaux joueurs, l'affichage de la liste des
        joueurs et la sortie du menu.
        Args:
            main_view (obj): La vue principale de l'application.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        while True:
            choice = self.player_view.display_player_menu()

            if choice == "1":
                self.add_player()
            elif choice == "2":
                self.display_players()
            elif choice == "3":
                break
            else:
                self.player_view.display_invalid_option_message()

    def add_player(self):
        """Ajoute un nouveau joueur.
        Cette méthode permet d'ajouter un nouveau joueur à la liste des
        joueurs. Elle vérifie également l'existence du joueur avant l'ajout.
        Args:
            Aucun argument requis.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        print("Ajout d'un nouveau joueur...") 
        player_data = self.player_view.get_player_data()
        print("Données du joueur :", player_data) 
        last_name = player_data['last_name']
        first_name = player_data['first_name']
        birth_date = player_data['birth_date']
        player_id = player_data['player_id']
        ranking = player_data['ranking']
        score_tournament = player_data['score_tournament']
        # vérifications supplémentaires ici,valider la date au format requis

        player = Player(last_name,
                        first_name,
                        birth_date,
                        player_id,
                        ranking,
                        score_tournament)
        # Vérifiez s'il y a des doublons en fonction de l'identifiant du joueur
        if not any(p.player_id == player_id for p in self.players):
            self.players.append(player)
            print("Joueur ajouté avec succès !")
            # Save les joueurs dans JSON sans écraser les données existantes
            self.save_players('players.json')
            print("Joueur ajouté avec succès dans la sauvegarde!")
        else:
            print("Le joueur existe déjà dans la base de données.")

    def display_players(self):
        """Affiche la liste des joueurs.
        Cette méthode affiche la liste de tous les joueurs par ordre
        alphabétique en fonction de leur nom de famille et de leur prénom.
        Args:
            Aucun argument requis.
        Returns:
            output_string (str): Une chaîne de caractères contenant la liste
                                 de tous les joueurs.
        Raises:
            Aucune exception n'est levée.
        """   
        if not self.players:
            print("Aucun joueur n'a été ajouté.")
        else:
            # Triez les joueurs par nom de famille, puis par prénom
            sorted_players = sorted(self.players,
                                    key=lambda x: (x.last_name, x.first_name)) 
            output_string = "Liste de tous les joueurs par ordre alphabétique :\n"
            for player in sorted_players:
                output_string +=f"Nom : {player.last_name}, Prénom : {player.first_name}, Date de naissance : {player.birth_date}, ID : {player.player_id}, Classement : {player.ranking}, Score du tournoi : {player.score_tournament}\n"
                print(output_string)
        return output_string

    def save_players(self, file_name):
        """Sauvegarde les joueurs dans un fichier JSON.
        Cette méthode sauvegarde la liste des joueurs dans un fichier JSON.
        Args:
            file_name (str): Le nom du fichier dans lequel les joueurs seront
                             sauvegardés.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        self.create_data_folder_if_not_exists()
        file_path = os.path.join(DATA_FOLDER, file_name)
        with open(file_path, 'w') as file:
            players_data = []
            for player in self.players:
                players_data.append({
                    "last_name": player.last_name,
                    "first_name": player.first_name,
                    "birth_date": player.birth_date,
                    "player_id": player.player_id,
                    "ranking": player.ranking,
                    "score_tournament": player.score_tournament
                })
            json.dump(players_data, file, indent=4)

    def load_players(self, file_name):
        """Charge les joueurs à partir d'un fichier JSON.
        Cette méthode charge les joueurs à partir d'un fichier JSON spécifié.
        Les données sont lues à partir du fichier et chaque joueur est ajouté
        à la liste des joueurs.
        Args:
            file_name (str): Le nom du fichier à partir duquel charger les
                             données des joueurs.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        self.create_data_folder_if_not_exists()
        file_path = os.path.join(DATA_FOLDER, file_name)
        with open(file_path, 'r') as file:
            players_data = json.load(file)
            for data in players_data:
                player = Player(
                    data['last_name'],
                    data['first_name'],
                    data['birth_date'],
                    data['player_id'],
                    data['ranking'],
                    data['score_tournament']
                )
                self.players.append(player)

    @staticmethod
    def create_data_folder_if_not_exists():
        """Crée le dossier de données s'il n'existe pas.
        Cette méthode vérifie l'existence du dossier de données et le crée
        si il n'existe pas.
        Args:
            Aucun argument requis.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
