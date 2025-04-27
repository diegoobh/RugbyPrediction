import os
import sys
import pandas as pd
import numpy as np

# Agregar el directorio src al path para importar módulos desde allí
root_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_path, '..', 'src')
sys.path.append(src_path)

from utils.winner_loser import get_winner_loser
from utils.performance import get_performance

def process_data(results_df):
        # Aplicamos la función get_winner_loser a cada fila del DataFrame
    results_df[['winner', 'loser']] = results_df.apply(get_winner_loser, axis=1).apply(pd.Series)

    # Inicializamos las columnas para los puntos tanto de local como de visitante
    results_df['ranking_home_points'] = 0
    results_df['ranking_away_points'] = 0

    # Añadimos una columna para el margen de victoria del equipo local
    results_df['margin'] = results_df['home_score'] - results_df['away_score']

    # Añadimos una columna para el resultado del partido definiendo si gana el equipo local o visitante
    results_df['result'] = results_df['margin'].apply(lambda x: 'home_win' if x > 0 else ('away_win' if x < 0 else 'draw'))

    # Inicializamos el ranking de los equipos empezando en 80 todos 
    ranking_points = { 'Scotland': 80, 'England': 80, 'Ireland': 80, 'Wales': 80, 'France': 80, 'Italy': 80, 'South Africa': 80, 'New Zealand': 80, 'Australia': 80, 'Argentina': 80}

    for i, row in results_df.iterrows():
        # Obtenemos el nombre del equipo local y visitante
        home_team = row['home_team']
        away_team = row['away_team']

        # Actualizamos los puntos de ranking de los equipos local y visitante
        results_df.at[i, 'ranking_home_points'] = ranking_points[home_team]
        results_df.at[i, 'ranking_away_points'] = ranking_points[away_team]
        if row['neutral'] == True: 
            home_points = ranking_points[home_team]
        else: 
            home_points = ranking_points[home_team] + 3
        away_points = ranking_points[away_team]

        gap = home_points - away_points
        if gap < -10: 
            gap = -10
        elif gap > 10:
            gap = 10
        
        if row['winner'] == home_team: 
            core = 1 - (gap*0.1)
        elif row['winner'] == 'draw': 
            core = gap*0.1
        else: 
            core = 1 + (gap*0.1)

        if np.abs(row['home_score'] - row['away_score']) > 15:
            core = core*1.5

        if row['world_cup'] == True:
            core = core*2
        
        if row['winner'] != 'draw': 
            ranking_points[row['winner']] += core
            ranking_points[row['loser']] -= core
        else:
            ranking_points[home_team] -= core
            ranking_points[away_team] += core

    results_df.reset_index(drop=True, inplace=True)

    for index, row in results_df.iterrows():
        results_df.at[index, 'home_performance'] = get_performance(results_df, row['home_team'], index, 5)
        results_df.at[index, 'away_performance'] = get_performance(results_df, row['away_team'], index, 5)
    
    return results_df