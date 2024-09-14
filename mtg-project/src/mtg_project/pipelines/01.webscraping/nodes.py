"""Preprocessing nodes."""

import os
import requests
import zipfile

from utils import setup_logger

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

    return None


def pp_decks_from_json_files(
        decks_json_partitioned: dict, 
        txt_folder: str, 
        valid_card_count: int, 
        log_folder: str) -> None:
    """
    Processa todos os decks JSON fornecidos pelo PartitionedDataSet e salva no formato .txt.
     
    Faz isso desde que contenham pelo menos o número mínimo de cartas definido em valid_card_count (params). 
    O log dos decks processados é salvo em um arquivo no log_folder (params).

    Args:
        decks_json_partitioned (dict): Dicionário de decks carregados de arquivos JSON através de PartitionedDataSet.
        txt_folder (str): Pasta onde os arquivos .txt serão salvos.
        valid_card_count (int): Número mínimo de cartas no mainBoard para que o deck seja processado.
        log_folder (str): Caminho do arquivo onde os logs serão salvos.
    """
    # Chama a função para configurar o logger
    logger = setup_logger("process_all_decks_logger",log_folder)

    # Criar a pasta de saída se não existir
    os.makedirs(txt_folder, exist_ok=True)

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

    # Função para salvar a decklist no arquivo .txt
    def save_decklist(decklist, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(decklist))  # Escreve tudo de uma vez para ser mais eficiente

    # Percorrer os arquivos JSON no dicionário fornecido pelo PartitionedDataSet
    for file_name, data in decks_json_partitioned.items():
        # Verificar se o deck tem pelo menos valid_card_count no mainboard
        if count_mainboard_cards(data) >= valid_card_count:
            
            # Gerar a decklist
            decklist = generate_decklist(data)
            
            # Definir o nome do arquivo de saída .txt com base no nome do deck
            deck_name = get_deck_name(data)
            output_file_name = f"{deck_name.replace(' ', '_')}.txt"
            output_file_path = os.path.join(txt_folder, output_file_name)
            
            # Salvar a decklist no formato .txt
            save_decklist(decklist, output_file_path)
            logger.info(f"Decklist {output_file_name} gerada com sucesso!")
        else:
            logger.info(f"Deck {file_name} ignorado (menos de {valid_card_count} cartas no mainBoard).")

    # Remover o handler para evitar problemas futuros
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

