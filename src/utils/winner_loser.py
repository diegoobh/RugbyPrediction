# Función para indicar si el partido fue ganado por el equipo local o visitante o si fue un empate
def get_winner_loser(row): 
    if row['home_score'] > row['away_score']:
        winner = row['home_team']
        loser = row['away_team']
    elif row['home_score'] < row['away_score']:
        winner = row['away_team']
        loser = row['home_team']
    else:
        winner = 'draw'
        loser = 'draw'
    return winner, loser