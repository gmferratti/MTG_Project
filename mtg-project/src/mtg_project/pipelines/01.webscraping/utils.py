"""General utils file for pp."""

import logging

def setup_logger(logger_name:str, 
                 log_folder: str = None) -> logging.Logger:
    """
    Configura o logger para salvar os logs em um arquivo ou exibi-los no terminal.
    
    Args:
        log_folder (str, optional): Caminho do arquivo onde os logs serão salvos. 
        Se for None, o logger exibirá as informações no terminal.
    
    Returns:
        logging.Logger: Logger configurado para salvar logs em arquivo ou exibi-los no terminal.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Desativa a propagação do logger para o logger raiz
    logger.propagate = False

    # Verifica se já existem handlers para evitar duplicação de logs
    if not logger.hasHandlers():
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