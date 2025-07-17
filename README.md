# SPV Automático

O script tem como objetivo realizar a consulta de pesquisas nas plataformas de Tribunal Jurídico do Brasil de forma automatizada.

## Resumo
Lê dados do banco de dados
Usa web scraping com Selenium para buscar informações judiciais
Interpreta os resultados
Salva no banco
É capaz de reiniciar a si mesmo automaticamente

## Fluxo
Conecta ao banco de dados e obtém uma lista de pesquisas pendentes.
Usa o Selenium para consultar essas pessoas no site do TJSP.
Analisa o resultado da página e classifica como: "Nada consta", "Consta criminal" ou "Consta cível".
Armazena o resultado da pesquisa no banco de dados.
Repete o processo com diferentes filtros de pesquisa (CPF, RG, nome), reiniciando o programa após cada execução.

## Estrutura
### Classe Principal: SPVAutomatico
__init__(self, filtro='')
Inicializa o objeto com o filtro de busca atual.
Valores típicos de filtro:
0: pesquisa por CPF
1 ou 3: por RG
2: por nome

### conectaBD(filtro)
Conecta ao banco de dados e retorna uma lista de pesquisas ainda não concluídas (resultado NULL).

### pesquisa(self)
Fluxo principal de execução:
1. Chama conectaBD() para obter os registros pendentes.
2. Para cada registro:
    - Extrai dados como CPF, RG, nome, etc.
    - Chama executaPesquisa() com base no filtro.
    - Limita o tempo de execução (600 segundos).
3. Se houver filtros adicionais, reinicia com filtro+1.
4. Se todas as tentativas falharem ou não houver dados, reinicia o programa.

### executaPesquisa(self, filtro, nome, cpf, rg, codPesquisa, spvTipo)
Escolhe qual dado usar na pesquisa:
- Se filtro = 0 → usa CPF.
- Se filtro = 1 ou 3 → usa RG.
- Se filtro = 2 → usa nome.

1. Carrega o site via carregaSite().
2. Analisa o conteúdo da página com checaResultado().
3. Insere o resultado da análise no banco via SQL INSERT.

### checaResultado(site, codPesquisa)
Classifica a página obtida como:

- Nada consta: 1
- Consta criminal: 2
- Consta cível: 5
- Não identificado: 7

### carregaSite(self, filtro, documento)
Usa o Edge WebDriver em modo headless (sem abrir janela) para fazer a consulta no site do TJSP:

1. Acessa: https://esaj.tjsp.jus.br/cpopg/open.do
2. Seleciona tipo de busca:
    - CPF/RG: DOCPARTE
    - Nome: NMPARTE
3. Preenche o campo correto e clica em "Consultar"
4. Retorna o HTML da página para análise posterior

Se der erro, ele aguarda 2 minutos e reinicia o programa.

### restarta_programa(self)
Reinicia o programa com os.execl().

### Linhhas finais
```
p = SPVAutomatico(0)
p.pesquisa()
```
Cria o objeto com o filtro 0 (CPF) e inicia a pesquisa.

# Ambiente
Python 3.10

## Inicialização do ambiente virtual
source desafio_fidelity_venv/bin/activate  # Linux/macOS
desafio_fidelity_venv\Scripts\activate     # Windows

### Caso necessário
pip install -r requirements.txt