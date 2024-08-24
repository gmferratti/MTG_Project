# API + Modelo ML MTGA

API para extração dos dados do card game Magic: The Gathering Arena.
Tais dados alimentarão uma base de dados que, por sua vez, alimentarão
um modelo de Machine Learning de cálculo de probabilidade de vitórias.

## Integrantes

* Antonio Eduardo de Oliveira Lima
* Gustavo Mendonça Ferratti
* Luiz Claudio Santana Barbosa
* Mauricio de Araujo Pintor

## Visão Geral do Projeto

Inserir fluxograma aqui

## Configuração Inicial

### Criação do Ambiente Virtual

Para criar o ambiente virtual utilizando Conda, execute o comando abaixo:

```bash
make create_env
```

Após a criação do ambiente, ative-o com:
```bash
conda activate mtg_env
```

Obs: É bom garantir que o ambiente correto esteja ativado para todos os comandos e rodagens.


### Instalação de Dependências
Para instalar todas as dependências necessárias para produção, execute:
```bash
make install
```

Para instalar as dependências de desenvolvimento, incluindo ferramentas necessárias para linting e testes, execute:
```bash
make install-dev
```

## Aplicação

Para rodar a aplicação, execute:
```bash
make run
```

A aplicação por padrão será disponibilizada na porta 5000. A partir dela será possível:
* Ponto 1
* Ponto 2
* Ponto 3

Imagem da aplicação

### Endpoints

Para visualizar os endpoints e suas documentações, basta acessar http://localhost:5000/apidocs. 
Tal documentação foi feita com flasgger (Swagger para o Flask).

## Desenvolvimento

### Rodando Linters
Linters são ferramentas que ajudam a manter a qualidade do código, verificando erros e garantindo conformidade com as boas práticas de codificação.

Para rodar os linters (flake8, black e isort) e verificar se o código está de acordo com os padrões estabelecidos, execute:
```bash
make lint
```
Você também pode aplicar automaticamente correções de formatação com o comando:
```bash
make lint-all
```

### Rodando Testes
Para executar os testes automatizados do projeto, utilize o comando:
```bash
make test
```

Obs: O make test utiliza o pytest no background (observar arquivo Makefile), logo, fique a vontade para utilizar esse comando com qualquer argumento de preferência (por exemplo: pytest tests/pastaA/arquivob.py)

### Trabalhando com Notebooks
Para trabalhar com Jupyter Notebooks na pasta /notebooks, é recomendável que você mantenha seu ambiente virtual ativo para garantir que todas as dependências necessárias estão disponíveis.

Para melhor organização, está convencionado que cada desenvolvedor terá sua pasta dentro de notebooks/, tal prática irá fácilitar o desenvolvimento sem qualquer sobrescrita e conflito de git.

Os notebooks permitem uma interação direta com o código, facilitando a visualização de dados e resultados de forma interativa, sendo ideal para experimentos e análises exploratórias. Logo, não é um requisito se ater às melhores práticas de coding (apenas de ser recomenddado). Já nos scripts produtivos (.py) o rigor será maior.

## Contribuindo

Para contribuir com o projeto, siga os passos abaixo:

1. **Fork** o repositório para sua conta no GitHub.
2. **Clone** o fork para sua máquina local.
3. **Crie uma branch** para suas modificações, nomeando-a de forma que reflita a natureza das mudanças (e atendo a elas).
4. **Faça suas alterações** e **commit**.
5. **Push** suas mudanças para seu fork no GitHub.
6. Abra um **Pull Request** do seu fork para o repositório principal. Certifique-se de descrever as mudanças realizadas e qualquer outra informação que facilite a avaliação do PR.

Sua contribuição será revisada e, se apropriada, mesclada no projeto principal.