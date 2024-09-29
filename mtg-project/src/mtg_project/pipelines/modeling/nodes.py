"""ML Modeling Pipeline."""

import pandas as pd
import numpy as np
import random
import shap
import pickle

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from typing import List, Dict, Any
from .constants import (
    derived_feats, 
    key_cols)
from ..utils import setup_logger, get_last_file
from ...config import run_key

def feature_engineering(matches_partitions: Dict[str, Any]) -> pd.DataFrame:
    import pandas as pd
    import numpy as np
    from typing import Any, Dict

    # Configura o logger geral
    logger = setup_logger("feature_engineering")

    # Lista para armazenar os DataFrames carregados
    dataframes = []

    # Iterar sobre as partições e carregar cada DataFrame
    for partition_name, dataset in matches_partitions.items():
        logger.info(f"Carregando partição: {partition_name}")
        # Carrega o DataFrame chamando o método diretamente
        df = dataset()
        # Adicionar informações sobre o jogador e a partida
        player_name, match_id = partition_name.split('/')
        df['player_name'] = player_name
        df['match_id'] = match_id
        # Adicionar o DataFrame à lista
        dataframes.append(df)

    # Concatenar todos os DataFrames em um único DataFrame
    matches_df = pd.concat(dataframes, ignore_index=True)

    logger.info("Criando variáveis cumulativas por jogador e partida...")

    # Garantir que 'spent_mana' esteja no formato correto
    matches_df["spent_mana"] = matches_df["spent_mana"].astype(int)

    # Criação de variáveis cumulativas por 'player_name' e 'match_id'
    matches_df['cum_mana_pool'] = matches_df.groupby(['player_name', 'match_id'])['mana_pool'].cumsum()
    matches_df["cum_spent_mana"] = matches_df.groupby(['player_name', 'match_id'])["spent_mana"].cumsum()

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

    # Certificar-se de que a coluna 'deck_colors' é do tipo string
    matches_df['deck_colors'] = matches_df['deck_colors'].astype(str)
    # Substituir 'nan' por string vazia
    matches_df['deck_colors'].replace('nan', '', inplace=True)

    # Criar uma coluna binária para cada cor de mana
    for color in all_colors:
        matches_df[f'{color}'] = matches_df['deck_colors'].apply(lambda x: 1 if color in x else 0)

    # Remover a coluna original de cores do deck
    matches_df.drop(columns=['deck_colors'], inplace=True)

    # Criar uma coluna com a quantidade de cores total do deck
    matches_df['n_colors'] = matches_df[all_colors].sum(axis=1)

    logger.info("Criando lag features...")

    # Ordenar o DataFrame para garantir que os shifts e rollings funcionem corretamente
    matches_df.sort_values(by=['player_name', 'match_id', 'turn'], inplace=True)

    # Lag Features: Captura os valores dos turnos anteriores
    matches_df['mana_curve_efficiency_lag_1'] = matches_df.groupby(['player_name', 'match_id'])['mana_curve_efficiency'].shift(1)
    matches_df['mana_curve_efficiency_lag_2'] = matches_df.groupby(['player_name', 'match_id'])['mana_curve_efficiency'].shift(2)
    matches_df['spell_ratio_lag_1'] = matches_df.groupby(['player_name', 'match_id'])['spell_ratio'].shift(1)
    matches_df['land_ratio_lag_1'] = matches_df.groupby(['player_name', 'match_id'])['land_ratio'].shift(1)

    # Preencher valores ausentes nas lag features
    lag_features = ['mana_curve_efficiency_lag_1', 'mana_curve_efficiency_lag_2', 'spell_ratio_lag_1', 'land_ratio_lag_1']
    matches_df[lag_features] = matches_df[lag_features].fillna(0)

    logger.info("Criando rolling features...")

    # Rolling Features: Médias móveis para capturar tendências temporais
    matches_df['rolling_mean_mana_curve_efficiency_3'] = matches_df.groupby(['player_name', 'match_id'])['mana_curve_efficiency']\
        .rolling(window=3, min_periods=1).mean().reset_index(level=['player_name', 'match_id'], drop=True)
    matches_df['rolling_mean_spell_ratio_3'] = matches_df.groupby(['player_name', 'match_id'])['spell_ratio']\
        .rolling(window=3, min_periods=1).mean().reset_index(level=['player_name', 'match_id'], drop=True)
    matches_df['rolling_mean_land_ratio_3'] = matches_df.groupby(['player_name', 'match_id'])['land_ratio']\
        .rolling(window=3, min_periods=1).mean().reset_index(level=['player_name', 'match_id'], drop=True)

    # Tratamento de valores nulos gerados pelos shifts e rolling
    matches_df.fillna(0, inplace=True)

    logger.info("Engenharia de features concluída.")

    # Retornar o DataFrame final
    return matches_df

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

    return features_cleaned, selected_features_cols


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

    return train_features, test_features, train_target, test_target

def fit_model(
    train_features: pd.DataFrame,
    train_target: pd.DataFrame,
    param_grid: tuple,
) -> str:
    """
    Ajusta um modelo de árvore de decisão com suporte a features temporais e realiza tuning de hiperparâmetros com GridSearchCV.
    O modelo ajustado é salvo em um arquivo .pkl.

    Args:
        train_features (pd.DataFrame): DataFrame com as features de treino.
        train_target (pd.DataFrame): DataFrame com a variável target de treino.
        param_grid (dict): Dicionário com os hiperparâmetros a serem ajustados.
        model_path (str): Caminho para salvar o modelo ajustado (.pkl).

    Returns:
        model_path (str): Caminho do arquivo do modelo ajustado salvo.
    """
    # Configurando o logger geral
    logger = setup_logger("fit_model")
    logger.info("Iniciando o ajuste do modelo e o tuning de hiperparâmetros.")

    # Criando o modelo base
    model = DecisionTreeRegressor(random_state=42)
    
    logger.info("Configurando o GridSearchCV com a seguinte grade de hiperparâmetros:")
    logger.info(param_grid)

    # Configurando o GridSearchCV para tuning de hiperparâmetros
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='neg_mean_squared_error',
        cv=5,
        verbose=1
    )
    
    # Ajustando o modelo com os dados de treino e realizando tuning
    grid_search.fit(train_features, train_target)
    
    # Extraindo o melhor modelo e seus parâmetros
    best_model = grid_search.best_estimator_
    best_hiper_params = grid_search.best_params_

    logger.info("O melhor modelo foi encontrado com os seguintes hiperparâmetros:")
    logger.info(best_hiper_params)

    return best_model, best_hiper_params

def predict_and_evaluate_model(
        model: pickle, 
        test_features: pd.DataFrame, 
        test_target: pd.Series) -> tuple:
    """
    Carrega o modelo salvo, faz previsões nos dados de teste, avalia o modelo e calcula valores SHAP.

    Args:
        model (pickle): Arquivo do modelo ajustado.
        test_features (pd.DataFrame): DataFrame com as features de teste.
        test_labels (pd.Series): Rótulos reais para avaliação do modelo.

    Returns:
        y_pred (pd.Series): Previsões do modelo.
        shap_values (pd.DataFrame): Valores SHAP para interpretação do modelo.
        error_metrics (dict): Métricas de erro do modelo (MSE, MAE, R2).
    """
    # Configura o logger geral
    logger = setup_logger("predict_and_evaluate_model")

    logger.info("Carregando o modelo...")
    logger.info("Fazendo previsões nos dados de teste.")
    
    # Desempacotando as variaveis
    test_features = test_features
    test_target = test_target

    # Fazendo previsões
    predicted_target = model.predict(test_features)
    
    # Calculando as métricas de erro
    logger.info("Calculando as métricas de erro...")
    mse = mean_squared_error(test_target, predicted_target)
    mae = mean_absolute_error(test_target, predicted_target)
    r2 = r2_score(test_target, predicted_target)
    
    error_metrics = {
        "mean_squared_error": mse,
        "mean_absolute_error": mae,
        "r2_score": r2
    }
    
    # Calculando os valores SHAP
    logger.info("Calculando os valores SHAP...")
    explainer = shap.Explainer(model)
    shap_values = explainer(test_features)

    logger.info("Previsões e avaliação completadas.")
    
    # encapsulando as variaveis em dicionarios versionados
    predicted_target = pd.DataFrame(predicted_target)
    predicted_target.rename(columns={0:"predicted_target"}, inplace=True)
    
    shap_values = pd.DataFrame(shap_values.values)
    error_metrics = pd.DataFrame([error_metrics])

    return predicted_target, shap_values, error_metrics