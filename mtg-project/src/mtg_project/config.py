"""Configurações do projeto."""
from datetime import datetime

# Obter a data e hora atuais
now = datetime.now()

# Definir as constantes para data e hora de execução
RUN_DATE = now.strftime('%Y-%m-%d')  # Formato: 'YYYY-MM-DD'

# Caso deseje adicionar a hora, descomente a linha abaixo
# RUN_TIME = now.strftime('%H-%M-%S')  # Formato: 'HH-MM-SS'

# RUN KEY
run_key = f"{RUN_DATE}"
# run_key = f"{RUN_DATE}_{RUN_TIME}"  # Adiciona a hora à chave de execução