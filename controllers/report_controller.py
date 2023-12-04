import os
from models.player_model import Player
from views.report_view import ReportView


class ReportController:
    """Contrôleur pour gérer les rapports et leurs opérations associées."""
    def __init__(self, player_controller, tournament_controller=None):
        """Initialise le contrôleur des rapports avec les contrôleurs
        des joueurs et de tournois en option."""
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.report_view = ReportView()

    def run_report_menu(self):
        """Exécute le menu de rapport en fonction du choix de l'utilisateur."""
        while True:
            choice = self.report_view.display_report_menu()

            if choice == "1":
                self.display_players_alphabetically()
            elif choice == "2":
                self.display_all_tournaments()
            elif choice == "3":
                self.display_tournament_details()
            elif choice == "4":
                self.display_tournament_players_alphabetically()
            elif choice == "5":
                self.display_all_tournament_rounds_and_matches()
            elif choice == "6":
                break
            else:
                self.report_view.display_invalid_option_message()

    def display_players_alphabetically(self):
        """Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport."""
        players_report = self.player_controller.display_players()
        players = Player.load_players()
        if not players:
            print("Aucun joueur enregistré")
        else:
            # Triez les joueurs par nom de famille, puis par prénom
            sorted_players = sorted(players,
                                    key=lambda x: (x.last_name, x.first_name)) 
            players_report = (
                "Liste de tous les joueurs par ordre alphabétique :\n")
            for player in sorted_players:
                players_report += (
                 f"Nom : {player.last_name}, Prénom : {player.first_name}, "
                 f"Date de naissance : {player.birth_date}, "
                 f"ID : {player.player_id}, "
                 f"Classement : {player.ranking}, "
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
        pass

    def display_tournament_details(self):
        """Affiche les détails d'un tournoi."""
        pass

    def display_tournament_players_alphabetically(self):
        """Affiche les joueurs d'un tournoi par ordre alphabétique."""
        pass

    def display_all_tournament_rounds_and_matches(self):
        """Affiche tous les tours d'un tournoi et tous les matchs du tournoi"""
        pass

    def save_report_to_file(self, report_text, file_name):
        """
        Sauvegarde le rapport dans un fichier texte.
        Args:
        report_text (str): Le texte du rapport à sauvegarder.
        file_name (str): Le nom du fichier de sauvegarde.
        """
        data_folder = "reports"
        self.create_report_folder_if_not_exists(data_folder)
        file_path = os.path.join(data_folder, file_name + ".txt")
        with open(file_path, 'w') as file:
            file.write(report_text)
        print(f"Rapport sauvegardé avec succès dans {file_path}")

    def save_report_as_html(self, report_text, file_name):
        """
        Sauvegarde le rapport dans un fichier au format HTML.
        Args:
        report_text (str): Le texte du rapport à sauvegarder au format HTML.
        file_name (str): Le nom du fichier de sauvegarde.
        """
        print("save_report_as_html")
        data_folder = "reports"
        self.create_report_folder_if_not_exists(data_folder)
        # Ajout de ".html" à file_name
        file_path = os.path.join(data_folder, file_name + ".html")
        report_text = report_text.replace("Liste de tous les joueurs" +
                                          "par ordre alphabétique :", "")
        with open(file_path, 'w') as file:
            file.write(report_text)
        print(f"Rapport sauvegardé au format HTML dans {file_path}")

    def save_report_with_html_template(self, report_text, file_name):
        """
        Sauvegarde le rapport avec un modèle HTML spécifique.
        Args:
        report_text (str): Le texte du rapport à sauve avec le modèle HTML.
        file_name (str): Le nom du fichier de sauvegarde.
        """  
        template_path = "templates/template.html"
        with open(template_path, 'r', encoding='utf-8') as template_file:
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
                        .replace(",", "") + "</td></tr>")
                    data_rows += f"<tr>{data_row}"
            modif_template = template_content.replace(
                                             '<!-- INSERT_DATA -->', data_rows)
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
