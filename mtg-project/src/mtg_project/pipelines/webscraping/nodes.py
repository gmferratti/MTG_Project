"""Preprocessing nodes."""

import os
import requests
import zipfile
import random

from ..utils import setup_logger

def get_deck_zip_from_web(        
        project_path: str,
        zip_url: str,  
        zip_folder: str) -> None:
    """
    Baixa um arquivo ZIP de um URL, o descompacta em uma pasta temporária e salva os arquivos JSON
    no subdiretório 'decks_json' dentro da pasta especificada.

    Args:
        project_path (str): Caminho base do projeto onde o zip_folder será concatenado.
        zip_url (str): URL do arquivo ZIP a ser baixado.
        zip_folder (str): Caminho relativo dentro do project_path onde o arquivo ZIP será salvo.

    Returns:
        None: A função salva os arquivos JSON na pasta especificada e não retorna nada.
    """
    # Configura o logger geral com o nome "get_deck_zip_logger"
    logger = setup_logger("get_deck_zip_logger")

    # Concatenar o caminho completo de zip_folder com project_path (que é a raiz)
    full_output_path = os.path.join(project_path, zip_folder)
    
    # Criar a pasta raiz se ela não existir
    os.makedirs(full_output_path, exist_ok=True)

    # Criar o subdiretório 'decks_json' dentro da pasta especificada
    decks_json_path = os.path.join(full_output_path, 'decks_json')
    os.makedirs(decks_json_path, exist_ok=True)

    # Função para baixar o arquivo zip
    def download_file(url, folder):
        local_filename = os.path.join(folder, url.split("/")[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logger.info(f"Zip dos decklists baixado com sucesso em: {local_filename}")
        return local_filename

    # Baixar o arquivo zip
    zip_file_path = download_file(zip_url, full_output_path)

    # Descompactar o arquivo zip e salvar os arquivos JSON no subdiretório 'decks_json'
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('.json'):
                # Definir o caminho de destino do arquivo extraído no subdiretório 'decks_json'
                output_file_path = os.path.join(decks_json_path, file_name)
                
                # Ler e salvar o arquivo JSON diretamente no caminho especificado
                with zip_ref.open(file_name) as json_file, open(output_file_path, "wb") as out_file:
                    out_file.write(json_file.read())
    
    logger.info(f"Arquivos JSON extraídos com sucesso em: {decks_json_path}")

    # Remover o arquivo zip após extração
    os.remove(zip_file_path)
    logger.info(f"Arquivo ZIP removido após extração!")

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

def pp_decks_from_json_files(
        decks_json_partitioned: dict, 
        deck_cards: int, 
        log_folder: str) -> dict:
    """
    Processa todos os decks JSON fornecidos pelo PartitionedDataSet e salva no formato .txt.

    Faz isso desde que contenham pelo menos o número mínimo de cartas definido em deck_cards (params).
    O log dos decks processados é salvo em um arquivo no log_folder (params).

    Args:
        decks_json_partitioned (dict): Dicionário de decks carregados de arquivos JSON através de PartitionedDataSet.
        deck_cards (int): Número mínimo de cartas no mainBoard para que o deck seja processado.
        log_folder (str): Caminho do arquivo onde os logs serão salvos.

    Returns:
        dict: Dicionário de decks processados, onde as chaves são os nomes dos arquivos e os valores são as decklists.
    """
    # Caminho do arquivo de log
    log_filepath = os.path.join(log_folder, 'decks_selection_log.txt')

    # Cria a pasta de log se ela não existir
    os.makedirs(log_folder, exist_ok=True)

    # Chama a função para configurar o logger
    logger = setup_logger("pp_decks_from_json_files", log_filepath)

    # Função para extrair o nome do deck diretamente do JSON
    def get_deck_name(data):
        return data['data'].get('name', 'Unknown Deck')

    # Função para contar o número de cartas no mainBoard
    def count_mainboard_cards(data):
        return sum(card['count'] for card in data['data']['mainBoard'])

    # Função para gerar a decklist formatada
    def generate_decklist(data):
        decklist = []
        deck_name = get_deck_name(data)
        decklist.append("About")
        decklist.append(f"Name {deck_name}")
        decklist.append("\nDeck")

        for card in data['data']['mainBoard']:
            name = card['name']
            count = card['count']
            decklist.append(f"{count} {name}")

        return decklist

    # Dicionário de saída para armazenar as decklists processadas
    processed_decks = {}

    # Percorrer os arquivos JSON no dicionário fornecido pelo PartitionedDataSet
    for file_name, dataset in decks_json_partitioned.items():
        # Carregar os dados chamando o método `load()` do dataset
        data = dataset()

        # Verificar se o deck tem pelo menos deck_cards no mainboard
        if count_mainboard_cards(data) >= deck_cards:
            
            # Gerar a decklist
            decklist = generate_decklist(data)

            # Definir o nome do arquivo de saída .txt com base no nome do deck
            deck_name = get_deck_name(data)
            output_file_name = f"{deck_name.replace(' ', '_')}.txt"

            # Salvar no dicionário de decks processados
            processed_decks[output_file_name] = "\n".join(decklist)

            logger.info(f"Decklist {output_file_name} gerada com sucesso!")
        else:
            logger.info(f"Deck {file_name} ignorado (menos de {deck_cards} cartas no mainBoard).")

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

    return processed_decks


def sample_decks(
        decks_txt_partitioned: dict, 
        sample_size: float, 
        log_folder: str) -> dict:
    """
    Amostra os decks no formato .txt com base no sample_size e retorna um dicionário de paths (pkl).

    Args:
        decks_txt_partitioned (dict): Dicionário de decks onde as chaves são nomes de arquivos e os valores 
        são funções que retornam o conteúdo do deck.
        sample_size (float): A fração da população original que será usada para amostragem (valor entre 0 e 1).
        log_folder (str): Caminho da pasta para salvar os logs.

    Returns:
        dict: Dicionário com os caminhos dos decks amostrados.
    """

    # Caminho do arquivo de log
    log_filepath = os.path.join(log_folder, 'decks_sampling_log.txt')

    # Cria a pasta de log se ela não existir
    os.makedirs(log_folder, exist_ok=True)

    # Configurar o logger para salvar no arquivo .txt
    logger = setup_logger('decks_sampling_logger', log_filepath)

    # Número total de decks disponíveis
    total_decks = len(decks_txt_partitioned)
    
    # Calcular o tamanho da amostra
    target_sample_size = int(total_decks * sample_size)

    # Amostra aleatória da população
    logger.info(f"Amostrando {target_sample_size} decks de um total de {total_decks}.")
    sampled_keys = random.sample(list(decks_txt_partitioned.keys()), target_sample_size)
    
    # Criar dicionário contendo os paths dos decks amostrados
    sampled_decks = {key: os.path.join('data/01_raw/decks_txt', key) for key in sampled_keys}

    # Logar os decks escolhidos
    logger.info(f"Decks amostrados: {', '.join(sampled_keys)}")
    logger.info(f"Amostragem completa. {len(sampled_decks)} decks selecionados.")

    return sampled_decks

