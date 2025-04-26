# Función para medir el rendimiento de un equipo en función de los partidos ganados, perdidos y empatados
def get_performance(results_df, team_name, current_row_index, n_games):
    team_performance = []
    games = results_df.copy()
    games_sliced = games.iloc[:current_row_index]

    for index in range(len(games_sliced)-1, -1, -1):
        current_row = games_sliced.iloc[index]

        if current_row['home_team'] == team_name or current_row['away_team'] == team_name:
            if current_row['winner'] == team_name:
                team_performance.append(1)
            elif current_row['winner'] == 'draw':
                team_performance.append(0.5)
            else:
                team_performance.append(0)
    return sum(team_performance[:n_games])   