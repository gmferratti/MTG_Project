"""ML Modeling Pipeline."""

import pandas as pd
import numpy as np
import random

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

from typing import List
from .constants import (
    derived_feats, 
    key_cols)
from ..utils import setup_logger, get_last_file
from ...config import run_key

def feature_engineering(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza engenharia de features nos dados das partidas de Magic: The Gathering.

    Esta função cria variáveis cumulativas, baseadas em razões, lag features e rolling features
    a partir dos dados das partidas, e prepara o dataset para modelagem. Além disso, realiza a codificação
    de variáveis categóricas e trata valores ausentes ou infinitos, garantindo que os dados estejam adequados
    para uso em modelos preditivos.

    Args:
        matches_df (pd.DataFrame): DataFrame contendo os dados das partidas, com colunas como 'mana_pool', 
        'spent_mana', 'spells_played', 'lands_played', 'turn', e 'deck_colors', entre outras.

    Retorna:
        pd.DataFrame: DataFrame com novas features calculadas, incluindo:
        
        - 'cum_mana_pool': Soma cumulativa do mana disponível ao longo dos turnos para cada jogador e partida.
        - 'cum_spent_mana': Soma cumulativa do mana gasto ao longo dos turnos para cada jogador e partida.
        - 'cum_spells_played': Soma cumulativa dos feitiços jogados ao longo dos turnos para cada jogador e partida.
        - 'spell_ratio': Razão entre os feitiços jogados e o número de turnos (feitiços por turno).
        - 'land_ratio': Razão entre os terrenos jogados e o número de turnos (terrenos por turno).
        - 'mana_curve_efficiency': Eficiência da curva de mana, definida como a razão entre o mana gasto 
          cumulativo e o mana acumulado ao longo dos turnos.
        - 'mana_curve_efficiency_lag_1': Valor de 'mana_curve_efficiency' no turno anterior.
        - 'mana_curve_efficiency_lag_2': Valor de 'mana_curve_efficiency' dois turnos anteriores.
        - 'spell_ratio_lag_1': Valor de 'spell_ratio' no turno anterior.
        - 'land_ratio_lag_1': Valor de 'land_ratio' no turno anterior.
        - 'rolling_mean_mana_curve_efficiency_3': Média móvel de 'mana_curve_efficiency' em uma janela de 3 turnos.
        - 'rolling_mean_spell_ratio_3': Média móvel de 'spell_ratio' em uma janela de 3 turnos.
        - 'rolling_mean_land_ratio_3': Média móvel de 'land_ratio' em uma janela de 3 turnos.
        - Colunas binárias codificadas em One-Hot para representar as cores de mana ('W', 'U', 'B', 'R', 'G').

    A função também lida com erros de divisão, substituindo valores infinitos por 0, e preenche valores 
    ausentes na variável 'mana_curve_efficiency'.
    """
    # Configura o logger geral
    logger = setup_logger("feature_engineering")

    # Pegando o ultimo arquivo do PartitionedDataset
    matches_df = get_last_file(matches_df)()

    logger.info("Criando variáveis cumulativas por jogador e partida...")

    # Garantir que 'spent_mana' esteja no formato correto
    matches_df["spent_mana"] = matches_df["spent_mana"].astype(int)

    # Criação de variáveis cumulativas por 'name' e 'match'
    matches_df['cum_mana_pool'] = matches_df.groupby(['name', 'match'])['mana_pool'].cumsum()
    matches_df["cum_spent_mana"] = matches_df.groupby(['name', 'match'])["spent_mana"].cumsum()

    logger.info("Criando variáveis de razão...")

    # Criação de variáveis baseadas em razões: feitiços por turno e terrenos por turno
    matches_df['spell_ratio'] = (matches_df['spells_played'] / (matches_df['turn'] + 1)).round(2)
    matches_df['land_ratio'] = (matches_df['lands_played'] / (matches_df['turn'] + 1)).round(2)

    logger.info("Criando variável de eficiência da curva de mana...")

    # Criação da variável de eficiência da curva de mana (razão entre mana gasto e mana acumulado)
    matches_df['mana_curve_efficiency'] = matches_df['cum_spent_mana'] / matches_df['cum_mana_pool']

    # Tratamento de valores infinitos e valores ausentes
    matches_df['mana_curve_efficiency'].replace([float('inf'), -float('inf')], 0, inplace=True)
    matches_df['mana_curve_efficiency'].fillna(0, inplace=True)
    matches_df['mana_curve_efficiency'] = matches_df['mana_curve_efficiency'].round(2)

    # Codificação One-Hot para as cores de mana
    all_colors = ['W', 'U', 'B', 'R', 'G']

    logger.info("Codificando cores de mana (One-Hot Encoding)...")

    # Criar uma coluna binária para cada cor de mana
    for color in all_colors:
        matches_df[f'{color}'] = (matches_df['deck_colors'].apply(lambda x: 1 if color in x else 0))

    # Remover a coluna original de cores do deck
    matches_df.drop(columns=['deck_colors'], inplace=True)

    # Cria uma coluna com a quantidade de cores total do deck
    matches_df['n_colors'] = matches_df[all_colors].sum(axis=1)

    logger.info("Criando lag features...")

    # Lag Features: Captura os valores dos turnos anteriores
    matches_df['mana_curve_efficiency_lag_1'] = matches_df['mana_curve_efficiency'].shift(1)
    matches_df['mana_curve_efficiency_lag_2'] = matches_df['mana_curve_efficiency'].shift(2)
    matches_df['spell_ratio_lag_1'] = matches_df['spell_ratio'].shift(1)
    matches_df['land_ratio_lag_1'] = matches_df['land_ratio'].shift(1)

    logger.info("Criando rolling features...")

    # Rolling Features: Médias móveis para capturar tendências temporais
    matches_df['rolling_mean_mana_curve_efficiency_3'] = matches_df['mana_curve_efficiency'].rolling(window=3).mean()
    matches_df['rolling_mean_spell_ratio_3'] = matches_df['spell_ratio'].rolling(window=3).mean()
    matches_df['rolling_mean_land_ratio_3'] = matches_df['land_ratio'].rolling(window=3).mean()

    # Tratamento de valores nulos gerados pelos shifts e rolling
    matches_df.fillna(0, inplace=True)

    logger.info("Engenharia de features concluída.")

    return {run_key:matches_df}

def feature_selection(
        features_df: pd.DataFrame,
        threshold_features: float,
        target: str = "mana_curve_efficiency",
        derived_features: list = derived_feats,
        key_columns: list = key_cols) -> pd.DataFrame:
    """
    Auxilia na seleção de features, removendo aquelas derivadas do target, 
    colunas-chave, e features altamente correlacionadas entre si.

    Args:
        features_df (pd.DataFrame): DataFrame contendo as features.
        target (str): Nome da variável alvo.
        threshold_features (float): Limiar para remover features com alta correlação.
        derived_features (list, optional): Lista de features derivadas do target para serem removidas.
        key_columns (list, optional): Lista de colunas-chave para serem removidas (ex: 'match', 'turn').

    Returns:
        pd.DataFrame: DataFrame com as features selecionadas.
    """
    # Configura o logger geral
    logger = setup_logger("feature_selection")
    logger.info("Iniciando o processo de seleção de features...")

    # Pegando o ultimo arquivo do PartitionedDataset
    features_df = get_last_file(features_df)()

    # Separar apenas colunas numéricas para o cálculo da correlação
    numeric_features_df = features_df.select_dtypes(include=[np.number])

    logger.info(f"Número inicial de features numéricas: {numeric_features_df.shape[1]}")

    # Remover features derivadas do target, se fornecidas
    if derived_features:
        numeric_features_df = numeric_features_df.drop(columns=derived_features, errors='ignore')
        logger.info(f"Features derivadas do target removidas: {derived_features}")

    # Remover colunas-chave nao categoricas ou string
    if key_columns:
        numeric_features_df = numeric_features_df.drop(columns=key_columns, errors='ignore')
        logger.info(f"Colunas-chave removidas: {key_columns}")

    # Remover a variável alvo do conjunto de features
    features_without_target = numeric_features_df.drop(columns=[target], errors='ignore')

    # Calcular a matriz de correlação entre as features (excluindo o target)
    corr_matrix = features_without_target.corr().abs()

    # Criar uma máscara para identificar as correlações acima do limiar entre as features, excluindo a diagonal
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Identificar colunas com alta correlação entre si, usando o limiar definido
    to_drop_features = [column for column in upper.columns if any(upper[column] > threshold_features)]

    # Remover as colunas altamente correlacionadas entre si
    features_cleaned = features_without_target.drop(columns=to_drop_features)

    logger.info(f"Número de features após a remoção de correlação maior que {threshold_features}: {features_cleaned.shape[1]}")

    # Selecionar as colunas finais de features
    selected_features_cols = features_cleaned.columns.tolist()
    
    # Reconstruir o DataFrame final, reinserindo key_columns e target
    features_cleaned = pd.concat([features_cleaned, features_df[key_columns], features_df[[target]]], axis=1)

    logger.info("Processo de seleção de features concluído.")

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

    return {run_key: features_cleaned}, {run_key:selected_features_cols}


def train_test_split(
        selected_features_df: pd.DataFrame,
        target_column: str,
        final_features_list: List[str], 
        hide_players: bool = False, 
        n_test_players: int = None, 
        hide_advanced_turns: bool = False,
        turn_threshold: int = None,) -> None:
    """
    Segrega as partidas em treino e teste, permitindo que o modelo nunca veja um determinado grupo de jogadores ou
    escondendo os turnos mais avançados de cada jogador durante o treino.

    Filtra o DataFrame pelas features selecionadas e produz os DataFrames de treino e teste para features e targets.

    Args:
        features_df (pd.DataFrame): O DataFrame contendo as features selecionadas do DF das partidas.
        final_features_list (List[str]): Lista das features selecionadas para o modelo.
        target_column (str): Nome da coluna target.
        n_test_players (int, opcional): Número de jogadores a serem amostrados aleatoriamente para o conjunto de teste.
        hide_advanced_turns (bool, opcional): Se True, usa a estratégia de esconder os turnos mais avançados no conjunto de teste.
        turn_threshold (int, opcional): Limite de turnos para segregar treino e teste. Os turnos maiores que esse valor serão usados como teste.
        hide_players (bool, opcional): Se True, usa a estratégia de esconder jogadores do conjunto de teste.

    Retorna:
        Tuple: DataFrames de treino e teste para features e targets.
    """
    # Configura o logger geral
    logger = setup_logger("train_test_split")

    # Pegando o ultimo arquivo do PartitionedDataset
    selected_features_df = get_last_file(selected_features_df)()
    final_features_list = get_last_file(final_features_list)()
    
    if hide_advanced_turns and turn_threshold is None:
        raise ValueError("Se `hide_advanced_turns` for True, `turn_threshold` deve ser fornecido.")
    
    if hide_players and n_test_players is None:
        raise ValueError("Se `hide_players` for True, `n_test_players` deve ser fornecido.")
    
    if hide_advanced_turns and hide_players:
        raise ValueError("Apenas uma estratégia pode ser usada de cada vez: `hide_advanced_turns` ou `hide_players`.")
    
    if hide_advanced_turns:
        # Estratégia de esconder turnos mais avançados
        logger.info(f"Usando a estratégia de esconder turnos mais avançados (turnos > {turn_threshold}).")
        
        # Dividir os dados entre treino e teste com base no turn_threshold
        train_df = selected_features_df[selected_features_df['turn'] <= turn_threshold]
        test_df = selected_features_df[selected_features_df['turn'] > turn_threshold]
    
    elif hide_players:
        # Estratégia de esconder jogadores
        logger.info(f"Usando a estratégia de esconder {n_test_players} jogadores.")
        
        # Verifica se a quantidade de jogadores para o teste é válida
        unique_players = selected_features_df['name'].unique()
        if n_test_players > len(unique_players):
            raise ValueError(f"O número de jogadores de teste ({n_test_players}) excede o número de jogadores únicos ({len(unique_players)}).")
        
        # Amostrando jogadores aleatoriamente
        test_players = random.sample(list(unique_players), n_test_players)
        logger.info(f"Jogadores selecionados para o conjunto de teste: {test_players}")
        
        # Segregar os dados entre treino e teste com base nos jogadores amostrados
        test_df = selected_features_df[selected_features_df['name'].isin(test_players)]
        train_df = selected_features_df[~selected_features_df['name'].isin(test_players)]
    
    else:
        raise ValueError("Nenhuma estratégia foi selecionada. Use `hide_advanced_turns` ou `hide_players`.")
    
    # Filtrando apenas as features selecionadas
    train_features = train_df[final_features_list]
    test_features = test_df[final_features_list]

    # Extraindo os targets
    train_target = train_df[[target_column]]
    test_target = test_df[[target_column]]

    return {run_key:train_features}, {run_key:test_features}, {run_key:train_target}, {run_key:test_target}