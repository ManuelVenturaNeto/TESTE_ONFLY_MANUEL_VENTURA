
# Teste Técnico OnFly

## Autor

Manuel Ventura De Oliveira Neto
- [@github](https://github.com/ManuelVenturaNeto)
- [@linkedin](https://www.linkedin.com/inmanuel-ventura-neto/)

### Descrição

Uma pipeline que consome dados de 100 pokemons da PokeAPI em formato json, trata esses dados com pandas, gera um grafico com o matplotlib. 

Por fim ele salva em uma pasta "outputs" dois arquivos: 

1. O primeiro é uma **imagem jpg** que apresenta a **distribuição de quantos pokemons tem em cada tipo de pokemon.** 
2. O segundo arquivo salvo é um **arquivo csv** contendo 3 informações: um dataframe com os 5 pokemons de maior experiência base, um dataframe com a media do HP, Ataque e Defesa dos pokemons para cada tipo, e a referencia do link para a imagem do gráfico gerado.

## Instalação

1. Clone o repositorio do github:

```terminal
  git clone https://github.com/ManuelVenturaNeto/TESTE_ONFLY_MANUEL_VENTURA.git
```

2. Entre na parta: 
```terminal
  CD TESTE_ONFLY_MANUEL_VENTURA
```  
3. Crie o docker:

```terminal
  docker build -t flask-app .
```    

4. Crie um ambiente virtual:

```terminal
  docker run -p 5000:5000 -v ${PWD}/outputs:/app/outputs flask-app
```

## Rodando os testes

Para rodar todos os testes, rode o seguinte comando:

```bash
  docker run --rm flask-app pytest
```

Para rodar um teste isoladamente rode o pytest com o caminho da pasta até o aquivo do seu teste, como no exemplo abaixo:

```bash
  docker run --rm flask-app pytest -s -v src/stages/load/load_pokemon_files_test.py
```

### Resumo da aplicação
A pipeline é composta pelos três estágios típicos do processo ETL (Extract, Transform, Load), organizados da seguinte forma:

1. **Extração (Extract):** A extração dos dados é iniciada a partir de uma pasta denominada Drivers, onde um método chamado HttpRequest é responsável por realizar as requisições à API para coletar as informações necessárias.

A classe ExtractPokemonData, localizada na pasta extract, orquestra o processo de chamada à API e armazena os dados obtidos em uma tupla nomeada. Esta tupla funciona como um contrato, garantindo um formato padronizado para os dados antes de serem passados para o estágio de transformação. A tupla contém dois campos:

- raw_information_content, que armazena as informações extraídas;
- extraction_date, que registra o momento exato em que os dados foram extraídos.

2. **Transformação (Transform):** No estágio de transformação, a classe TransformPokemonData recebe o contrato gerado na etapa anterior e processa os dados. O objetivo dessa transformação é:

- Obter a imagem em formato PNG de cada Pokémon;
- Criar um dataframe contendo os 5 Pokémons com a maior experiência base;
- Gerar outro dataframe que calcula as médias de HP, ataque e defesa dos Pokémons agrupadas por tipo.

Após a transformação dos dados, essas informações são armazenadas em uma nova tupla nomeada TransformContract.

- transformation_content, que armazena os dados tratados;
- transformation_date, que registra o momento exato em que os dados foram tratados.

3. **Carga (Load):** Finalmente, o contrato transformado é enviado para a classe responsável por gerar os arquivos finais, contendo os dados já processados e prontos para uso.


## Estrutura de pastas

```
📁outputs
📁src
└── 📁drivers
    └── __init__.py
    └── http_requester_test.py
    └── http_requester.py
    └── 📁interfaces
        └── __init__.py
        └── http_request.py
└── 📁errors
    └── __init__.py
    └── driver_error.py
    └── extract_error.py
    └── load_error.py
    └── transform_error.py
└── 📁main
    └── __init__.py
    └── main_pipeline.py
└── 📁stages
    └── __init__.py
    └── 📁contracts
        └── __init__.py
        └── extract_contract.py
        └── transform_contract.py
    └── 📁extract
        └── __init__.py
        └── extract_pokemon_data_test.py
        └── extract_pokemon_data.py
    └── 📁load
        └── __init__.py
        └── load_pokemon_files_test.py
        └── load_pokemon_files.py
    └── 📁transform
        └── __init__.py
        └── transform_pokemon_data_test.py
        └── transform_pokemon_data.py
└── __init__.py
 📁venv
.dockerignore
.flake8
.gitignore
.pre-commit-config.yaml
.pylintrc
dockerfile
pipeline_logs.log
requirements.txt
run.py
```
## Documentação da Classes

1. **HttpRequester (arquivo: http_requester.py)**

**Responsabilidade:** Esta classe é responsável por fazer requisições HTTP à API de Pokémons para coletar informações. 

Ela possui dois métodos principais:

- **get_100_pokemons_from_api:** Obtém informações de 100 Pokémons a partir da URL configurada.

- **get_unique_pokemon_data:** Coleta informações detalhadas de um único Pokémon usando sua URL específica.

**Tratamento de Erros:** Utiliza um logger para registrar o sucesso ou falha nas requisições e trata exceções com o lançamento de um erro personalizado DriverError.

2. **ExtractPokemonData (arquivo: extract_pokemon_data.py)**

**Responsabilidade:** Esta classe orquestra a coleta dos dados essenciais dos Pokémons através da classe HttpRequester.

Método principal: 
- **collect_essential_informations**: coleta dados de 100 Pokémons e os organiza em um dicionário contendo o ID, nome, experiência base, tipos e estatísticas básicas (HP, ataque, defesa).

**Saída:** Retorna um contrato de extração (ExtractContract) que contém os dados brutos coletados e a data da extração.

3. **TransformPokemonData (arquivo: transform_pokemon_data.py)**

**Responsabilidade:** Esta classe transforma os dados brutos extraídos em informações estruturadas, como gráficos e dataframes.

Método principal: 

- **tranform_pokemon_data:** recebe um contrato de extração e realiza várias transformações:
Converte dados brutos em um DataFrame estruturado.
- Gera gráficos de distribuição de Pokémons por tipo.
- Calcula os 5 Pokémons com maior experiência base.
- Calcula as médias de HP, ataque e defesa para cada tipo de Pokémon.
**Saída:** Retorna um contrato de transformação (TransformContract) contendo os dados refinados e a data de transformação.

4. **LoadPokemonFiles (arquivo: load_pokemon_files.py)**

**Responsabilidade:** A classe é responsável por carregar os dados transformados e gerar arquivos de saída.
Método principal: 

**load_requered_files:** recebe o contrato de transformação e executa o carregamento de:
- Gráfico gerado, salvando como imagens PNG.
- Relatórios em formato CSV contendo os 5 Pokémons com maior experiência base, a média das estatísticas por tipo e uma referência ao gráfico gerado .

**Saída:** Gera e salva arquivos na pasta "outputs", incluindo gráficos e relatórios CSV.