import uuid
import constantes
import re
from datetime import datetime


class PlayerView:
    @staticmethod
    def display_player_menu():
        """
        Affiche le menu de gestion des joueurs.
        Returns:
            str: Le choix de l'utilisateur.
        """
        print("\nMenu de Gestion des Joueurs :")
        print(constantes.PLAYER_MENU_NOUVEAU, "Ajouter un nouveau joueur")
        print(constantes.PLAYER_MENU_AFFICHER, "Afficher tous les joueurs")
        print(constantes.PLAYER_MENU_QUIT, "Revenir au menu principal")
        return input("Choisissez une option : ")

    @staticmethod
    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée
        pour la gestion des joueurs.
        """
        print(
            "Option invalide. Veuillez choisir une option valide pour la"
            + "gestion des joueurs."
        )

    @staticmethod
    def get_player_data():
        """
        Récupère les données d'un nouveau joueur.
        Returns:
            dict: Les données du nouveau joueur.
        """
        while True:
            last_name = input("Entrez le nom de famille du joueur : ")
            if last_name:
                break
            else:
                print("Le nom de famille ne peut pas être vide. Réessayez.")
        while True:
            first_name = input("Entrez le prénom du joueur : ")
            if first_name:
                break
            else:
                print("Le prénom ne peut pas être vide. Réessayez.")
        while True:
            birth_date = input(
                "Entrez la date de naissance du joueur" + "(au format JJ/MM/AAAA) : "
            )
            try:
                # Essayer de convertir la chaîne en objet datetime

                datetime.strptime(birth_date, "%d/%m/%Y")
                # La conversion a réussi, la date est valide

                print("La date de naissance est conforme.")
                break  # Sortir de la boucle si la date est conforme
            except ValueError:
                # La conversion a échoué, la date n'est pas valide

                print(
                    "Format de date invalide. Assurez-vous d'utiliser "
                    + "le format JJ/MM/AAAA. Réessayez."
                )
        # Définition du motif de la regex
        # Début de la chaîne (^) suivi de deux lettres (maj ou min).
        # Cinq chiffres (\d) suivis de la fin de la chaîne ($).

        motif_regex = r"^[A-Za-z]{2}\d{5}$"
        while True:
            # Demande à l'utilisateur d'entrer l'identifiant du joueur

            player_id_national = input(
                "Entrez l'identifiant nationnal d echecs du joueur (ab12345): "
            )
            # Vérification de la correspondance avec la regex

            if re.match(motif_regex, player_id_national):
                print("L'identifiant est conforme.")
                break  # Sortir de la boucle si l'identifiant est conforme
            else:
                print(
                    "L'identifiant n'est pas conforme.Assurez-vous d'avoir"
                    + " 2 lettres suivies de 5 chiffres. Réessayez."
                )
        score_tournament = 0
        gen_id = str(uuid.uuid4())
        player_id = gen_id[:6]
        # player_id = str(uuid.uuid4())

        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "player_id": player_id,
            "player_id_national": player_id_national,
            "score_tournament": score_tournament,
        }

    def afficher_list(self, players):
        if len(players) <= 0:
            print("Aucun joueur n'a été ajouté.")
        else:
            # Triez les joueurs par nom de famille, puis par prénom

            sorted_players = sorted(players, key=lambda x: (x.last_name, x.first_name))
            output_string = "Liste de tous les joueurs par ordre alphabétique :\n"
            for player in sorted_players:
                output_string += (
                    f"Nom : {player.last_name}, Prénom : {player.first_name}, "
                    f"Date de naissance : {player.birth_date}, "
                    f"ID : {player.player_id}, "
                    f"Score du tournoi : {player.score_tournament}\n"
                )
            print(output_string)
