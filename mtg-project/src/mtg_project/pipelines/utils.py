"""General utils file for pp."""

import logging


def setup_logger(logger_name: str, log_folder: str = None) -> logging.Logger:
    """
    Configura o logger para salvar os logs em um arquivo ou exibi-los no terminal.

    Args:
        logger_name (str): Nome do logger a ser configurado.
        log_folder (str, optional): Caminho do arquivo onde os logs serão salvos.
        Se for None, o logger exibirá as informações no terminal.

    Returns:
        logging.Logger: Logger configurado para salvar logs em arquivo ou exibi-los no terminal.
    """
    logger = logging.getLogger(logger_name)

    # Evita adicionar múltiplos handlers para o mesmo logger
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Desativa a propagação para o logger raiz para evitar duplicação de logs
        logger.propagate = False

        if log_folder:
            # Criar um handler para salvar o log em arquivo
            file_handler = logging.FileHandler(log_folder, mode='w', encoding='utf-8')
            file_handler.setLevel(logging.INFO)

            # Criar um formato para o log
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Adicionar o handler ao logger
            logger.addHandler(file_handler)
        else:
            # Criar um StreamHandler para exibir os logs no terminal
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Criar um formato para o log no console
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)

            # Adicionar o handler ao logger
            logger.addHandler(console_handler)

    return logger


def get_last_file(partitioned_data):
    """
    Obtém o last file da partição mais recente de um PartitionedDataset.

    Args:
        partitioned_data (dict): Dicionário com as partições de dados.

    Returns:
        Any: O ultimo arquivo da partição mais recente.
    """
    # Obter a chave da partição mais recente
    latest_partition = max(partitioned_data.keys())

    # Obter os dados da partição mais recente
    data = partitioned_data[latest_partition]

    return data
