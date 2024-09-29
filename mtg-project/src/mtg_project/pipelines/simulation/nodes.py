"""Simulation nodes."""

import os
import random
import warnings
import logging
import pandas as pd

from faker import Faker
from typing import Callable, Dict, List

from classes.deck import Deck
from classes.player import Player
from classes.player_tracker import PlayerTracker

warnings.filterwarnings("ignore")

def create_players(n_players: int):
    """
    Cria uma lista de objetos Player com nomes aleatórios.

    Args:
        n_players (int): Número de jogadores a serem criados.

    Returns:
        List[Player]: Lista de objetos Player com nomes gerados aleatoriamente.
    """
    # Inicializando o gerador de dados falsos Faker
    fake = Faker()

    # Gerando uma lista de nomes aleatórios usando o Faker
    player_names = [
        fake.first_name() + " " + fake.last_name() for _ in range(n_players)
    ]

    # Criando uma lista de objetos Player a partir dos nomes gerados
    players = [Player(name) for name in player_names]

    # Retornando a lista de objetos Player
    return players


def assign_decks_to_players(
    players: List[Player], sampled_decks: Dict[str, str], log_folder: str
) -> List[Player]:
    """
    Função para atribuir decks aleatórios a cada player na lista de players.

    A função tentará atribuir um deck a cada player chamando o método assign_deck().
    Caso ocorra algum erro na atribuição, tentará com outro deck disponível.

    Args:
        players (list): Lista de objetos Player.
        sampled_decks (dict): Dicionário com os nomes e caminhos dos decks.
        log_folder (str): Caminho da pasta para salvar o log.

    Returns:
        List[Player]: Lista de objetos Player com decks atribuídos.
    """
    # Configurar o logger para a função
    logger = logging.getLogger(__name__)

    # Log de início da validação
    logger.info("Validating decks...")

    # Convertemos as chaves do dicionário para uma lista de nomes de decks disponíveis
    available_decks = list(sampled_decks.keys())

    for player in players:
        assigned = False
        while not assigned and available_decks:
            try:
                # Seleciona um deck aleatório da lista de decks disponíveis
                deck_name = random.choice(available_decks)

                # Obter o caminho completo do deck a partir do dicionário sampled_decks
                deck_path = sampled_decks[deck_name]

                # Cria um novo objeto Deck
                deck = Deck()

                # Carrega o deck a partir do arquivo .txt no caminho obtido
                deck.load_deck_from_txt(deck_path)

                # Atribui o deck ao player
                player.assign_deck(deck)
                logger.info(f"Deck '{deck_name}' assigned to player '{player.name}'")

                # Remove o deck da lista de decks disponíveis para evitar reutilização
                available_decks.remove(deck_name)

                assigned = True  # Deck atribuído com sucesso
            except Exception as e:
                # Em caso de erro, tenta outro deck
                logger.error(
                    f"Failed to assign deck '{deck_name}' to player '{player.name}': {e}"
                )
                continue

        # Se não houver mais decks disponíveis e não conseguir atribuir, lança um erro
        if not assigned:
            raise ValueError(
                f"No available decks left to assign to player '{player.name}'."
            )

    players_with_decks = players

    logger.info("Deck assignment process completed.")

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

    # Preparar o dicionário para o PartitionedDataset
    players_with_decks = {}
    for player in players:
        # Nome da partição inclui o nome do jogador
        partition_name = f"{player.name.replace(' ', '_')}"
        players_with_decks[partition_name] = player

    return players_with_decks

def simulate_player_matches(
    params: dict, players_with_decks: Dict[str, Callable]
) -> Dict[str, pd.DataFrame]:
    """
    Simula partidas de Magic: The Gathering para uma lista de jogadores com base nos parâmetros fornecidos.

    Parâmetros:
    -----------
    params : dict
        Dicionário contendo os parâmetros de simulação.

    players_with_decks : Dict[str, Callable]
        Dicionário onde as chaves são os nomes dos arquivos (e.g., 'Jeremy_Wiggins.pkl')
        e os valores são métodos que carregam objetos Player.

    Retorna:
    --------
    Dict[str, pd.DataFrame]
        Dicionário onde as chaves são combinações nome do jogador e número da partida,
        e os valores são DataFrames contendo os dados das partidas.
    """
    # Carregar os jogadores chamando os métodos de carregamento
    loaded_players = {}
    for partition_name, load_method in players_with_decks.items():
        player = load_method()  # Chama o método _load para obter o objeto Player
        loaded_players[partition_name] = player

    # Verificar se há jogadores carregados
    if not loaded_players:
        raise ValueError("Nenhum jogador foi carregado.")

    # Atribuir os parâmetros
    max_mulligans = params["max_mulligans"]
    mulligan_prob = params["mulligan_prob"]
    hand_size_stop = params["hand_size_stop"]
    max_turns = params["max_turns"]
    extra_land_prob = params["extra_land_prob"]
    matches_per_player = params["matches_per_player"]
    log_folder = params["log_folder"]

    # Configurar o logger para a função
    logger = logging.getLogger(__name__)

    # Log de início da simulação
    logger.info("Iniciando simulações...")

    # Dicionário para armazenar os resultados de cada partida
    matches_data = {}

    # Loop através dos jogadores e realizar as simulações de partidas
    for partition_name, player in loaded_players.items():
        for match_num in range(1, matches_per_player + 1):
            logger.info(
                f"Simulando partida {match_num} para o jogador '{player.name}'..."
            )

            # Inicializa o tracker para armazenar os dados da partida atual
            tracker = PlayerTracker()

            # Simula uma partida
            player.play_a_match(
                tracker,
                max_mulligans,
                mulligan_prob,
                max_turns,
                hand_size_stop,
                extra_land_prob,
            )

            # Obter os dados da partida atual
            match_dataframe = tracker.get_data()

            # Construir o nome da partição usando nome do jogador e número da partida
            player_name_sanitized = player.name.replace(' ', '_')
            match_num_filled = str(match_num).zfill(3)
            partition_key = f"{player_name_sanitized}/match_{match_num_filled}"

            # Armazena o DataFrame da partida atual no dicionário de resultados
            matches_data[partition_key] = match_dataframe

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

    return matches_data
