import pandas as pd


def feature_engineering(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza engenharia de features nos dados das partidas.

    Esta função calcula variáveis cumulativas e baseadas em razão a partir dos dados de partidas em turnos, 
    além de preparar o dataset para modelagem, codificando variáveis categóricas e lidando com valores ausentes.

    Args:
        matches_df (pd.DataFrame): DataFrame contendo dados das partidas, incluindo colunas como 'mana_pool', 
        'spent_mana', 'spells_played', 'lands_played', 'turn', e 'deck_colors'.

    Retorna:
        pd.DataFrame: DataFrame com novas features, incluindo somas cumulativas, razões, e colunas codificadas 
        em one-hot para as cores dos decks. As seguintes features são adicionadas:

        - 'cum_mana_pool': Soma cumulativa da coluna 'mana_pool'.
        - 'cum_spent_mana': Soma cumulativa da coluna 'spent_mana'.
        - 'cum_spells_played': Soma cumulativa da coluna 'spells_played'.
        - 'spell_ratio': Razão de feitiços jogados por turno.
        - 'land_ratio': Razão de terrenos jogados por turno.
        - 'mana_curve_efficiency': Razão entre mana gasta cumulativa e mana acumulada, representando a eficiência
          do uso de mana.
        - Colunas codificadas em one-hot para cada cor de mana (W, U, B, R, G), derivadas de 'deck_colors'.
        
    A função também lida com erros de divisão na coluna 'mana_curve_efficiency', substituindo valores infinitos
    por 0 e preenchendo valores ausentes.
    """
    # Creating cumulative variables
    matches_df['cum_mana_pool'] = matches_df['mana_pool'].cumsum()
    matches_df["cum_spent_mana"] = matches_df["spent_mana"].cumsum()
    matches_df["cum_spells_played"] = matches_df["spells_played"].cumsum()

    # Creating ratio variables
    matches_df['spell_ratio'] = (matches_df['spells_played'] / (matches_df['turn'] + 1)).round(2)
    matches_df['land_ratio'] = (matches_df['lands_played'] / (matches_df['turn'] + 1)).round(2)

    # Creating target variable
    matches_df['mana_curve_efficiency'] = matches_df['cum_spent_mana'] / matches_df['cum_mana_pool']
    matches_df['mana_curve_efficiency'].replace([float('inf'), -float('inf')], 0, inplace=True)
    matches_df['mana_curve_efficiency'].fillna(0, inplace=True)
    matches_df['mana_curve_efficiency'] = matches_df['mana_curve_efficiency'].round(2)

    # Expand deck_colors into multiple columns (One-Hot Encoding for individual colors)
    all_colors = ['W', 'U', 'B', 'R', 'G']

    # Criar uma coluna para cada cor
    for color in all_colors:
        matches_df[f'{color}'] = (matches_df['deck_colors'].apply(lambda x: 1 if color in x else 0)).astype("category")

    # Drop the original deck_colors column
    matches_df.drop(columns=['deck_colors'], inplace=True)

    # Visualizando as primeiras linhas para confirmar as alterações
    return matches_df
