## Hackathon CAIXA 2023 - Primeira Etapa - Deafio perfil BackEnd: API Simulador

Requisitos para executar esta api:
- Python3.7 ou mais recente (preferencialmente 3.11)
- Modulos do python, instalados via pip através do comando: pip install -r requirements.txt

Como utilizar a api (Windows):
Instale o python disponivel no site: https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
Instale o modulo para criação de ambientes virtuais python (virtualenv) com o comando no powershell: pip install virtualenv
Crie o ambiente virtual com o comando no shell dentro da pasta do projeto: python -m venv venv
Inicie o ambiente virtual com o comando & ./venv/Scripts/Activate.ps1
Instale as dependecias: pip install - r requirements.txt
Inicie o servidor com o comando: python main.py

Como utilizar no Linux (Ubuntu):
deverá instalar o driver da microsoft odbc: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline
apt-get update
apt-get install unixodbc-dev
apt-get install g++
apt-get install python
apt-get install python-pip
apt-get install python-dev
pip install -r requirements.txt
python3 main.py (dentro da pasta do app)


Após iniciar o servidor, a API pode ser testada de duas formas:
1 - No navegador acessoando o endereço: http://localhost:8000 na documentação poderá usar a opção tryout e enviar requisicoões diretamente pelo site
2 - Rodando o arquivos teste.py através do comando 'python teste.py', irá gerar uma lista randomica de 200 solicitações e irá devolver o tempo para finalizar as requisições
    

Sobre esta API

Tem por objetivo receber um json via requisição http POST no seguinte formato:
{
    "valorDesejado": float,
    "prazo": int
}

Consultar os parametros dos produtos em uma database, calcular e devolver a simulação no formato json:
{
  "codigoProduto": 0,
  "descricaoProduto": "string",
  "taxaJuros": 0,
  "resultadoSimulacao": [
    {
      "tipo": "PRICE",
      "parcelas": [
        {
          "numero": 0,
          "valorAmortizacao": 0,
          "valorJuros": 0,
          "valorPrestacao": 0
        }
        ...
      ]
    },
    {
      "tipo": "SAC",
      "parcelas": [
        {
          "numero": 0,
          "valorAmortizacao": 0,
          "valorJuros": 0,
          "valorPrestacao": 0
        }
        ...
      ]
    }
  ]
}
Após isso irá gravar a resposta json em um eventhub


Considerações:

Tendo em vista a possibilidade da eventual indisponibilidade da database ou eventhub
para que os usuários não percam acesso ao serviço optamos por colocar as consultas na
database em loop, num período de 5 em 5 minutos, quando não for possivel atualizar as
informações dos produtos, a simulação será feita com os dados mais recentes disponiveis
em cache. 

Já as gravações no eventhub serão efetuadas de 1 em 1 minuto, desde que tenhamos itens 
na fila, com um máximo de 2mil itens na fila para não sobrecarregar a memória do servidor
no caso de falha de conexão ou indisponibilidade do eventhub 

Ainda evitamos necessidade de uma nova conexão ao eventhub e a db a cada nova consulta

Também facilita para o administrador do produto que poderá fazer a alteração dos parametros
e logo eles serão automaticamente atualizados na API

Os tempos de gravação no eventhub e de consulta dos parametros dos produtos podem ser 
facilmente alterados no arquivo main.py alterando as seguintes linhas onde N seria o 
tempo em minutos

lista_produtos.atualizar_periodicamente(N)
eventhub.enviar_periodicamente(N)

Nos testes executando o arquivo teste.py a nossa API se saiu levemente melhor no tempo de resposta
provavelmente por esta estar no localhost (200 simulações)

http://localhost:8000/
Elapsed time: 4.2089 seconds

https://apphackaixades.azurewebsites.net/api/Simulacao
Elapsed time: 11.3227 seconds

