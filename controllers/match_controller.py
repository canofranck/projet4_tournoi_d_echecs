class MatchController:
    def play_match(round):
        """Simule le déroulement des matches pour un round."""

        for match in round.matches:
            # Logique pour simuler le déroulement du match
            # demande les scores aux utilisateurs

            print(
                f"Entrez le score pour "
                f"{match.player1.first_name} {match.player1.last_name} vs "
                f"{match.player2.first_name} {match.player2.last_name}\n"
            )

            # Saisie des scores par les utilisateurs

            while True:
                try:
                    score1 = int(
                        input(
                            f"Score de {match.player1.first_name} {match.player1.last_name}: "
                        )
                    )
                    score2 = int(
                        input(
                            f"Score de {match.player2.first_name} {match.player2.last_name}: "
                        )
                    )
                    print()
                    # Mettre à jour les scores des joueurs

                    match.score1 = score1
                    match.score2 = score2
                    if score1 > score2:
                        match.score1 = 1
                        match.score2 = 0
                    elif score1 < score2:
                        match.score1 = 0
                        match.score2 = 1
                    else:
                        match.score1 = 0.5
                        match.score2 = 0.5
                    break
                except ValueError:
                    print("Veuillez entrer des chiffres valides pour les scores.")
