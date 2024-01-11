import os
import re
# from constantes import IN_PROGRESS, TO_LAUNCH
from models.player_model import Player
from models.round_model import Round
from views.main_view import MainView
from views.report_view import ReportView
from models.tournament_model import Tournament
from views.tournament_view import TournamentView
import constantes


class ReportController:
    """Contrôleur pour gérer les rapports et leurs opérations associées."""

    def __init__(self, player_controller, tournament_controller=None):
        """Initialise le contrôleur des rapports avec les contrôleurs
        des joueurs et de tournois en option."""
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.report_view = ReportView()
        self.main_view = MainView()

    def run_report_menu(self):
        """Exécute le menu de rapport en fonction du choix de l'utilisateur."""
        self.main_view.clear_screen()
        while True:
            choice = self.report_view.display_report_menu()

            if choice == constantes.REPORT_MENU_LISTE_JOUEUR_ALPHA:
                self.display_players_alphabetically()
            elif choice == constantes.REPORT_MENU_LISTE_TOURNOI:
                self.display_all_tournaments()
            elif choice == constantes.REPORT_MENU_LISTE_DATE_TOURNOI:
                self.display_tournament_details()
            elif choice == constantes.REPORT_MENU_LISTE_JOUEUR_TOURNOI:
                self.display_tournament_players_alphabetically()
            elif choice == constantes.REPORT_MENU_LISTE_ROUND_MATCH_TOURNOI:
                self.display_all_tournament_rounds_and_matches()
            elif choice == constantes.REPORT_MENU_QUIT:
                break
            else:
                self.report_view.display_invalid_option_message()

    def display_players_alphabetically(self):
        """Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport."""
        self.main_view.clear_screen()
        players_report = self.player_controller.display_players()
        players = Player.load_players()
        if not players:
            print("Aucun joueur enregistré")
        else:
            # Triez les joueurs par nom de famille, puis par prénom
            sorted_players = sorted(players, key=lambda x: (x.last_name, x.first_name))
            players_report = "Liste de tous les joueurs par ordre alphabétique :\n"
            for player in sorted_players:
                players_report += (
                    f"Nom : {player.last_name}, Prénom : {player.first_name}, "
                    f"Date de naissance : {player.birth_date}, "
                    f"ID : {player.player_id}, "
                    f"Score du tournoi : {player.score_tournament}\n"
                )
        user_choice = self.report_view.prompt_save_report()
        if user_choice.lower() == "o":
            file_name = self.report_view.get_file_name_to_save()
            self.save_report_to_file(players_report, file_name)
            self.save_report_with_html_template(players_report, file_name)
        else:
            print("Le rapport n'a pas été sauvegardé.")

    def display_all_tournaments(self):
        """Affiche tous les tournois."""
        self.main_view.clear_screen()
        tournaments = Tournament.load_tournaments()

        if not tournaments:
            TournamentView.display_no_available_tournaments()
            return
        tournament_report2 = "Liste des tournois :\n"
        for i, tournament in enumerate(tournaments):

            if tournament.etat_tournoi == constantes.TO_LAUNCH:
                etat = "TO_LAUNCH"
            elif tournament.etat_tournoi == constantes.IN_PROGRESS:
                etat = "IN_PROGRESS"
            else:
                etat = "FINISH"
            tournament_report2 += (
                f"Nom : {tournament.tournament_name}, Etat du tournoi : ({etat}), "
                f" Lieu : {tournament.location}, Date : {tournament.tournament_date}\n"
            )
        ReportView.display_tournaments_list(tournament_report2)
        user_choice = self.report_view.prompt_save_report()
        if user_choice.lower() == "o":
            file_name = self.report_view.get_file_name_to_save()
            self.save_report_to_file(tournament_report2, file_name)
            self.save_report_list_tournament_with_html_template(
                tournament_report2, file_name
            )
        else:
            print("Le rapport n'a pas été sauvegardé.")

    def display_tournament_details(self):
        """Affiche les détails d'un tournoi."""
        self.main_view.clear_screen()
        tournaments = Tournament.load_tournaments()
        ongoing_tournaments = [t for t in tournaments]

        if not ongoing_tournaments:
            TournamentView.display_ongoing_tournaments(tournaments)
            return
        print("Quel tournois vous voulez les details :")
        for i, tournament in enumerate(ongoing_tournaments, start=1):
            print(f"{i}. {tournament.tournament_name}")
        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi : "))
            if 1 <= choice <= len(ongoing_tournaments):
                selected_tournament_index = choice - 1
                selected_tournament = ongoing_tournaments[selected_tournament_index]
                self.date_tournament(selected_tournament)
            else:
                TournamentView.display_invalid_choice()
        except ValueError:
            TournamentView.display_invalid_choice()

    def date_tournament(self, selected_tournament):
        tournament_date = (
            f"Details pour le tournoi : {selected_tournament.tournament_name}\n"
        )
        tournament_date += (
            f"Lieu du tournoi : {selected_tournament.location}\n"
            f"Date du tournoi : {selected_tournament.tournament_date}\n"
            f"Nombre de rounds : {selected_tournament.number_of_tours}\n"
            f"Description du tournoi : {selected_tournament.description}\n"
            f"Etat du tournoi : {selected_tournament.etat_tournoi}\n"
        )
        # Obtenir la liste des joueurs inscrits au tournoi
        players_ids = selected_tournament.players_ids
        players = Player.load_players_by_ids(players_ids)
        tournament_date += "Liste des joueurs du tournoi :\n"
        for player in players:
            tournament_date += (
                f"Nom : {player.first_name}\n"
                f"Prenom : {player.last_name}\n"
                f"Date de naissance : {player.birth_date}\n"
                f"ID national des echecs : {player.player_id_national}\n"
            )
        print(tournament_date)
        user_choice = self.report_view.prompt_save_report()
        if user_choice.lower() == "o":
            file_name = self.report_view.get_file_name_to_save()
            self.save_report_to_file(tournament_date, file_name)
            self.save_report_tournament_date_with_html_template(
                tournament_date, file_name
            )
        else:
            print("Le rapport n'a pas été sauvegardé.")

    def details_tournament(self, selected_tournament):
        tournament_details = (
            f"Details pour le tournoi : {selected_tournament.tournament_name}\n"
        )
        tournament_details += (
            f"Lieu du tournoi : {selected_tournament.location}\n"
            f"Date du tournoi : {selected_tournament.tournament_date}\n"
            f"Nombre de rounds : {selected_tournament.number_of_tours}\n"
            f"Description du tournoi : {selected_tournament.description}\n"
            f"Etat du tournoi : {selected_tournament.etat_tournoi}\n"
        )
        round_number = [
            int(re.search(r"Round (\d+)", tour["round_name"]).group(1))
            for tour in selected_tournament.list_of_tours
        ]
        if round_number:
            dernier_numero_round = max(round_number)
            print("le dernier round est le : ", dernier_numero_round)
        # Obtenir la liste des joueurs inscrits au tournoi
        players_ids = selected_tournament.players_ids
        players = Player.load_players_by_ids(players_ids)
        tournament_details += "Liste des joueurs du tournoi :\n"
        for player in players:
            tournament_details += (
                f"Nom : {player.first_name}\n"
                f"Prenom : {player.last_name}\n"
                f"Date de naissance : {player.birth_date}\n"
                f"ID national des echecs : {player.player_id_national}\n"
            )
        tournament_details += "Liste des rounds du tournoi :\n"
        for tour_data in selected_tournament.list_of_tours:
            tour = Round.from_dict(tour_data, players)
            if tour.round_name:
                tournament_details += (
                    f"Round : {tour.round_name}\n"
                    f"Heure de debut : {tour.start_time.strftime('%d-%m-%Y %H:%M:%S')}\n"
                    f"Heure de fin : {tour.end_time.strftime('%d-%m-%Y %H:%M:%S')}\n"
                )
                tournament_details += "Liste des matchs du tournoi :\n"
                for match in tour.matches:
                    tournament_details += (
                        f"Match : {match.player1.first_name} {match.player1.last_name} vs {match.player2.first_name} "
                        f"{match.player2.last_name}\n"
                        f"Score : {match.score1} - {match.score2}\n"
                    )
                tournament_details += "Fin du round\n"
            else:
                print("Erreur : round_name n'est pas présent dans l'objet Round.")
        print(tournament_details)
        user_choice = self.report_view.prompt_save_report()
        if user_choice.lower() == "o":
            file_name = self.report_view.get_file_name_to_save()
            self.save_report_to_file(tournament_details, file_name)
            self.save_report_tournament_details_with_html_template(
                tournament_details, file_name
            )
        else:
            print("Le rapport n'a pas été sauvegardé.")

    def save_report_tournament_details_with_html_template(self, report_text, file_name):
        template_path = constantes.TEMPLATES_DETAILS

        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()

            # Générer le contenu HTML en utilisant les données du rapport
            data_rows = ""
            for line in report_text.split("\n"):
                if line.strip():
                    # test que chaque ligne commence par le bon commentaire
                    if "Details pour le tournoi : " in line:
                        data_row = line.replace(
                            "Details pour le tournoi : ",
                            "<tr><td>Nom du tournoi</td><td>",
                        )
                    elif "Lieu du tournoi :" in line:
                        data_row = line.replace(
                            "Lieu du tournoi : ", "<tr><td>Lieu du tournoi</td><td>"
                        )
                    elif "Date du tournoi :" in line:
                        data_row = line.replace(
                            "Date du tournoi : ", "<tr><td>Date du tournoi</td><td>"
                        )
                    elif "Nombre de rounds :" in line:
                        data_row = line.replace(
                            "Nombre de rounds : ", "<tr><td>Nombre de tours</td><td>"
                        )
                    elif "Description du tournoi :" in line:
                        data_row = line.replace(
                            "Description du tournoi : ", "<tr><td>Description</td><td>"
                        )
                    elif "Etat du tournoi :" in line:
                        data_row = line.replace(
                            "Etat du tournoi : ", "<tr><td>Etat du tournoi</td><td>"
                        )
                    else:
                        data_row = ""
                    data_row = data_row.replace(",", "") + "</td></tr>"
                    data_rows += f"{data_row}"
            players_rows = ""
            report_lines = report_text.split("\n")
            collecting_players = False
            # Lire le texte ligne par ligne
            for index, line in enumerate(report_lines):
                if line.startswith("Liste des joueurs du tournoi :"):
                    # Commencer à collecter les informations du joueur
                    collecting_players = True
                elif collecting_players and line.startswith("Nom : "):
                    # Extraire les informations du joueur
                    last_name = line.replace("Nom : ", "").strip()
                    first_name = (
                        report_lines[index + 1].replace("Prenom : ", "").strip()
                    )
                    birth_date = (
                        report_lines[index + 2]
                        .replace("Date de naissance : ", "")
                        .strip()
                    )
                    player_id_national = (
                        report_lines[index + 3]
                        .replace("ID national des echecs : ", "")
                        .strip()
                    )
                    # Ajouter les informations directement à la balise <!-- INSERT_PLAYERS --> du modèle HTML
                    player_row = (
                        f"<tr>"
                        f"<td>{last_name}</td>"
                        f"<td>{first_name}</td>"
                        f"<td>{birth_date}</td>"
                        f"<td>{player_id_national}</td>"
                        f"</tr>"
                    )
                    players_rows += player_row
            rounds_rows = ""
            collecting_rounds = False
            # Lire le texte ligne par ligne
            for index, line in enumerate(report_lines):
                if line.startswith("Liste des rounds du tournoi :"):
                    # Commencer à collecter les informations des rounds
                    collecting_rounds = True
                elif collecting_rounds and line.startswith("Round : "):
                    # Extraire les informations du round
                    round_name = line.replace("Round : ", "").strip()
                    start_time = (
                        report_lines[index + 1].replace("Heure de debut : ", "").strip()
                    )
                    end_time = (
                        report_lines[index + 2].replace("Heure de fin : ", "").strip()
                    )
                    # Ajouter les informations directement à la balise <!-- INSERT_ROUNDS --> du modèle HTML
                    round_row = (
                        f" <table>"
                        f"<tr>"
                        f"<th>Round</th>"
                        f"<th>Heure de debut</th>"
                        f"<th>Heure de fin</th>"
                        f"</tr>"
                        f"<tr>"
                        f"<td>{round_name}</td>"
                        f"<td>{start_time}</td>"
                        f"<td>{end_time}</td>"
                    )
                    # Collecter les informations des matchs à l'intérieur du bloc des rounds
                    matchs_rows = ""
                    collecting_matchs = False
                    # Lire le texte ligne par ligne
                    for match_index, match_line in enumerate(report_lines[index:]):
                        if match_line.startswith("Liste des matchs du tournoi :"):
                            # collecter les informations des matchs
                            collecting_matchs = True
                        elif collecting_matchs and match_line.startswith("Match : "):
                            # Extraire les informations du match
                            match = match_line.replace("Match : ", "").strip()
                            score = (
                                report_lines[index + match_index + 1]
                                .replace("Score : ", "")
                                .strip()
                            )
                            # Ajouter les informations directement à la balise <!-- INSERT_MATCHES --> du modèle HTML
                            match_row = (
                                f"<tr>" f"<td>{match}</td>" f"<td>{score}</td>" f"</tr>"
                            )
                            matchs_rows += match_row
                        elif match_line.startswith("Fin du round"):
                            break
                    round_row += matchs_rows + "</td></tr></table>"
                    rounds_rows += round_row
            # Remplacez la balise <!-- INSERT_PLAYERS --> dans le modèle HTML
            modif_template = (
                template_content.replace("<!-- INSERT_DATA -->", data_rows)
                .replace("<!-- INSERT_PLAYERS -->", players_rows)
                .replace("<!-- INSERT_ROUNDS -->", rounds_rows)
            )
            # Enregistrer le contenu modifié dans un nouveau fichier HTML
            self.save_report_as_html(modif_template, file_name)

    def display_tournament_players_alphabetically(self):
        """Affiche les joueurs d'un tournoi par ordre alphabétique."""
        self.main_view.clear_screen()
        tournaments = Tournament.load_tournaments()
        ongoing_tournaments = [t for t in tournaments]

        if not ongoing_tournaments:
            TournamentView.display_ongoing_tournaments(tournaments)
            return
        print("Quel tournois vous voulez les details :")
        for i, tournament in enumerate(ongoing_tournaments, start=1):
            print(f"{i}. {tournament.tournament_name}")
        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi : "))
            if 1 <= choice <= len(ongoing_tournaments):
                selected_tournament_index = choice - 1
                selected_tournament = ongoing_tournaments[selected_tournament_index]
                self.tournament_players_alphabetically(selected_tournament)
            else:
                TournamentView.display_invalid_choice()
        except ValueError:
            TournamentView.display_invalid_choice()

    def tournament_players_alphabetically(self, selected_tournament):
        """affiche tous les joueurs d un tournoi dans l ordre alhabetique"""
        self.main_view.clear_screen()
        # Obtenir la liste des joueurs inscrits au tournoi
        players_ids = selected_tournament.players_ids
        players = Player.load_players_by_ids(players_ids)
        # Triez les joueurs par nom de famille, puis par prénom
        sorted_players = sorted(players, key=lambda x: (x.last_name, x.first_name))
        tournament_list_players = ""
        tournament_list_players += (
            "Liste des joueurs par ordre alphabetique du tournoi :\n"
        )
        for player in sorted_players:
            tournament_list_players += (
                f"Nom : {player.last_name}, Prénom : {player.first_name}, "
                f"Date de naissance : {player.birth_date}, "
                f"ID : {player.player_id}, "
                f"Score du tournoi : {player.score_tournament}\n"
            )
        print(tournament_list_players)
        user_choice = self.report_view.prompt_save_report()
        if user_choice.lower() == "o":
            file_name = self.report_view.get_file_name_to_save()
            self.save_report_to_file(tournament_list_players, file_name)
            self.save_report_with_html_template(tournament_list_players, file_name)
        else:
            print("Le rapport n'a pas été sauvegardé.")

    def display_all_tournament_rounds_and_matches(self):
        """Affiche tous les tours d'un tournoi et tous les matchs du tournoi"""
        """Affiche les détails d'un tournoi."""
        self.main_view.clear_screen()
        tournaments = Tournament.load_tournaments()
        ongoing_tournaments = [t for t in tournaments]

        if not ongoing_tournaments:
            TournamentView.display_ongoing_tournaments(tournaments)
            return
        print("Quel tournois vous voulez les details :")
        for i, tournament in enumerate(ongoing_tournaments, start=1):
            print(f"{i}. {tournament.tournament_name}")
        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi : "))
            if 1 <= choice <= len(ongoing_tournaments):
                selected_tournament_index = choice - 1
                selected_tournament = ongoing_tournaments[selected_tournament_index]
                self.details_tournament(selected_tournament)
            else:
                TournamentView.display_invalid_choice()
        except ValueError:
            TournamentView.display_invalid_choice()

    def save_report_to_file(self, report_text, file_name):
        """
        Sauvegarde le rapport dans un fichier texte.
        Args:
        report_text (str): Le texte du rapport à sauvegarder.
        file_name (str): Le nom du fichier de sauvegarde.
        """
        data_folder = constantes.REPORTS_FOLDER
        self.create_report_folder_if_not_exists(data_folder)
        file_path = os.path.join(data_folder, file_name + ".txt")
        with open(file_path, "w") as file:
            file.write(report_text)
        print(f"Rapport sauvegardé avec succès dans {file_path}")

    def save_report_as_html(self, report_text, file_name):
        """
        Sauvegarde le rapport dans un fichier au format HTML.
        Args:
        report_text (str): Le texte du rapport à sauvegarder au format HTML.
        file_name (str): Le nom du fichier de sauvegarde.
        """
        data_folder = constantes.REPORTS_FOLDER
        self.create_report_folder_if_not_exists(data_folder)
        file_path = os.path.join(data_folder, file_name + ".html")
        report_text = report_text.replace(
            "Liste de tous les joueurs" + "par ordre alphabétique :", ""
        )
        with open(file_path, "w") as file:
            file.write(report_text)
        print(f"Rapport sauvegardé au format HTML dans {file_path}")

    def save_report_with_html_template(self, report_text, file_name):
        """
        Sauvegarde le rapport avec un modèle HTML spécifique.
        Args:
        report_text (str): Le texte du rapport à sauve avec le modèle HTML.
        file_name (str): Le nom du fichier de sauvegarde.
        """
        template_path = constantes.TEMPLATES
        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
            # Générer le contenu HTML en utilisant les données du rapport
            data_rows = ""
            for line in report_text.split("\n"):
                if line.strip():
                    data_row = (
                        line.replace("Nom : ", "<td>")
                        .replace("Prénom : ", "</td><td>")
                        .replace("Date de naissance : ", "</td><td>")
                        .replace("ID : ", "</td><td>")
                        .replace("Classement : ", "</td><td>")
                        .replace("Score du tournoi : ", "</td><td>")
                        .replace(",", "")
                        + "</td></tr>"
                    )
                    data_rows += f"<tr>{data_row}"
            modif_template = template_content.replace("<!-- INSERT_DATA -->", data_rows)
            # Enregistrer le contenu modifié dans un nouveau fichier HTML
            self.save_report_as_html(modif_template, file_name)

    def save_report_list_tournament_with_html_template(self, report_text, file_name):
        """
        Sauvegarde le rapport avec un modèle HTML spécifique.
        Args:
        report_text (str): Le texte du rapport à sauve avec le modèle HTML.
        file_name (str): Le nom du fichier de sauvegarde.
        """
        template_path = constantes.TEMPLATES_LIST_TOURNAMENT
        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
            # Générer le contenu HTML en utilisant les données du rapport
            data_rows = ""
            for line in report_text.split("\n"):
                if line.strip():
                    data_row = (
                        line.replace("Nom : ", "<td>")
                        .replace("Etat du tournoi : ", "</td><td>")
                        .replace("Lieu : ", "</td><td>")
                        .replace("Date : ", "</td><td>")
                        .replace(",", "")
                        + "</td></tr>"
                    )
                    data_rows += f"<tr>{data_row}"
            modif_template = template_content.replace("<!-- INSERT_DATA -->", data_rows)
            # Enregistrer le contenu modifié dans un nouveau fichier HTML
            self.save_report_as_html(modif_template, file_name)

    def save_report_tournament_date_with_html_template(self, report_text, file_name):
        template_path = constantes.TEMPLATES_DATE

        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
            # Générer le contenu HTML en utilisant les données du rapport
            data_rows = ""
            for line in report_text.split("\n"):
                if line.strip():
                    # test chaque ligne commence par le bon commentaire
                    if "Details pour le tournoi : " in line:
                        data_row = line.replace(
                            "Details pour le tournoi : ",
                            "<tr><td>Nom du tournoi</td><td>",
                        )
                    elif "Lieu du tournoi :" in line:
                        data_row = line.replace(
                            "Lieu du tournoi : ", "<tr><td>Lieu du tournoi</td><td>"
                        )
                    elif "Date du tournoi :" in line:
                        data_row = line.replace(
                            "Date du tournoi : ", "<tr><td>Date du tournoi</td><td>"
                        )
                    elif "Nombre de rounds :" in line:
                        data_row = line.replace(
                            "Nombre de rounds : ", "<tr><td>Nombre de tours</td><td>"
                        )
                    elif "Description du tournoi :" in line:
                        data_row = line.replace(
                            "Description du tournoi : ", "<tr><td>Description</td><td>"
                        )
                    elif "Etat du tournoi :" in line:
                        data_row = line.replace(
                            "Etat du tournoi : ", "<tr><td>Etat du tournoi</td><td>"
                        )
                    else:
                        data_row = ""
                    data_row = data_row.replace(",", "") + "</td></tr>"
                    data_rows += f"{data_row}"
            players_rows = ""
            report_lines = report_text.split("\n")
            collecting_players = False
            # Lire le texte ligne par ligne
            for index, line in enumerate(report_lines):
                if line.startswith("Liste des joueurs du tournoi :"):
                    # Commencer à collecter les informations du joueur
                    collecting_players = True
                elif collecting_players and line.startswith("Nom : "):
                    # Extraire les informations du joueur
                    last_name = line.replace("Nom : ", "").strip()
                    first_name = (
                        report_lines[index + 1].replace("Prenom : ", "").strip()
                    )
                    birth_date = (
                        report_lines[index + 2]
                        .replace("Date de naissance : ", "")
                        .strip()
                    )
                    player_id_national = (
                        report_lines[index + 3]
                        .replace("ID national des echecs : ", "")
                        .strip()
                    )
                    # Ajouter les informations directement à la balise <!-- INSERT_PLAYERS --> du modèle HTML
                    player_row = (
                        f"<tr>"
                        f"<td>{last_name}</td>"
                        f"<td>{first_name}</td>"
                        f"<td>{birth_date}</td>"
                        f"<td>{player_id_national}</td>"
                        f"</tr>"
                    )
                    players_rows += player_row
            # Remplacez la balise <!-- INSERT_PLAYERS --> dans le modèle HTML
            modif_template = template_content.replace(
                "<!-- INSERT_DATA -->", data_rows
            ).replace("<!-- INSERT_PLAYERS -->", players_rows)
            # Enregistrer le contenu modifié dans un nouveau fichier HTML
            self.save_report_as_html(modif_template, file_name)

    @staticmethod
    def create_report_folder_if_not_exists(data_folder):
        """
        Crée le dossier de rapport s'il n'existe pas déjà.
        Args:
        data_folder (str): Le nom du dossier de rapport.
        """
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
