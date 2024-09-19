"""Simulation nodes."""

import pandas as pd
import random
import os
import warnings

from typing import List, Dict
from faker import Faker

from classes.deck import Deck
from classes.player import Player
from classes.player_tracker import PlayerTracker
from src.mtg_project.pipelines.utils import setup_logger, get_last_file

from ...config import run_key

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
    player_names = [fake.first_name() + " " + fake.last_name() for _ in range(n_players)]
    
    # Criando uma lista de objetos Player a partir dos nomes gerados
    players = [Player(name) for name in player_names]

    # Retornando a lista de objetos Player
    return players

def assign_decks_to_players(
        players: List[Player], 
        sampled_decks: Dict[str, str],
        log_folder: str) -> List[Player]:
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
    # Caminho do arquivo de log
    log_filepath = os.path.join(log_folder, 'decks_assignment.txt')

    # Cria a pasta de log se ela não existir
    os.makedirs(log_folder, exist_ok=True)

    # Configura o logger geral
    logger = setup_logger("validate_decks", log_filepath)

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
                logger.error(f"Failed to assign deck '{deck_name}' to player '{player.name}': {e}")
                continue
        
        
        # Se não houver mais decks disponíveis e não conseguir atribuir, lança um erro
        if not assigned:
            raise ValueError(f"No available decks left to assign to player '{player.name}'.")

    players_with_decks = players

    logger.info("Deck assignment process completed.")

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

    return {run_key:players_with_decks}

def simulate_player_matches(
        params: dict, 
        players_with_decks: list) -> pd.DataFrame:
    """
    Simulates Magic: The Gathering matches for a list of players based on the provided simulation parameters.

    Parameters:
    -----------
    params : dict
        A dictionary containing the simulation parameters, including:
        - 'max_mulligans': Maximum number of mulligans allowed per player.
        - 'mulligan_prob': Probability of a player choosing to mulligan.
        - 'hand_size_stop': Minimum hand size at which the simulation will stop.
        - 'max_turns': Maximum number of turns per match.
        - 'extra_land_prob': Probability of playing an extra land during a turn.
        - 'matches_per_player': Number of matches to simulate per player.
        - 'log_folder': Folder path for logging the simulation process.
    
    players_with_decks : list
        A list of Player objects, each with an assigned deck to be used in the simulation.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing the match data for all players across all matches and turns, including:
        - Player attributes at each turn.
        - Match number for each simulation.
    """
    # Lendo os ultimos players com decks
    players_with_decks = get_last_file(players_with_decks)()
    
    # Atribuir os parâmetros
    max_mulligans = params["max_mulligans"]
    mulligan_prob = params["mulligan_prob"]
    hand_size_stop = params["hand_size_stop"]
    max_turns = params["max_turns"]
    extra_land_prob = params["extra_land_prob"]
    matches_per_player = params["matches_per_player"]
    log_folder = params["log_folder"]

    # Caminho do arquivo de log
    log_filepath = os.path.join(log_folder, 'player_matches.txt')

    # Cria a pasta de log se ela não existir
    os.makedirs(log_folder, exist_ok=True)

    # Configura o logger geral
    logger = setup_logger("player_matches", log_filepath)

    # Log de início da validação
    logger.info(f"Initiating simulations...")

    # Inicializa o tracker para armazenar os dados
    tracker = PlayerTracker()

    # Loop através dos jogadores e realizar as simulações de partidas
    for player in players_with_decks:
        for match in range(matches_per_player):

            logger.info(f"Simulating match {match + 1} for player '{player.name}'...")
            
            # Simular várias partidas para o jogador
            player.play_a_match(tracker, 
                                max_mulligans, 
                                mulligan_prob, 
                                max_turns, 
                                hand_size_stop, 
                                extra_land_prob)

    # Obter os dados de todas as partidas e turnos
    matches_dataframe = tracker.get_data()
    
    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
    
    return {run_key:matches_dataframe}