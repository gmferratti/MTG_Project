import os
import zipfile

import requests


def get_decks_zip_from_web(zip_url: str, project_path: str, output_folder: str):
    """
    Baixa um arquivo ZIP de um URL e o descompacta em uma pasta de destino.

    Esta função realiza o download de um arquivo ZIP a partir de um URL e salva o arquivo em uma pasta
    especificada. Caso a pasta de destino não exista, ela será criada. Após o download, o arquivo ZIP
    será descompactado no diretório de destino.

    Args:
        zip_url (str): URL do arquivo ZIP a ser baixado.
        project_path (str): Caminho base do projeto onde o output_folder será concatenado.
        output_folder (str): Caminho relativo dentro do project_path onde o arquivo ZIP será salvo e descompactado.

    Raises:
        requests.exceptions.RequestException: Caso ocorra um erro durante o download do arquivo.
        zipfile.BadZipFile: Caso o arquivo baixado não seja um arquivo ZIP válido.

    Example:
        get_decks_zip_from_web(
            zip_url="https://exemplo.com/decks.zip",
            project_path="C:/Users/name/OneDrive/Documentos/FIAP/Fase_03/mtg-project",
            output_folder="data/01_raw/decks_json"
        )
    """
    # Concatenar o caminho completo de output_folder com project_path
    full_output_path = os.path.join(project_path, output_folder)

    # Criar a pasta se ela não existir
    os.makedirs(full_output_path, exist_ok=True)

    # Função para baixar o arquivo zip
    def download_file(url, folder):
        local_filename = os.path.join(folder, url.split("/")[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Arquivo {local_filename} baixado com sucesso!")
        return local_filename

    # Baixar o arquivo zip
    zip_file_path = download_file(zip_url, full_output_path)

    # Descompactar o arquivo zip
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(full_output_path)
    print(f"Arquivo extraído com sucesso em {full_output_path}")
