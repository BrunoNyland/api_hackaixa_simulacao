## Hackathon CAIXA 2023 - Primeira Etapa - Deafio perfil BackEnd: API Simulador

Sobre esta API
Tem por objetivo receber um json via requisição http POST no seguinte formato:

{
    "valorDesejado": 900.00,
    "prazo": 5
}

Então a API deverá responder um arquivo json com o seguinte formato:

{
    "codigoProduto": 1,
    "descricaoProduto": "Produto 1",
    "taxaJuros": 0.0179,
    "resultadoSimulacao":
    [
        {
            "tipo": "SAC",
            "parcelas": 
            [
                {
                    "numero": 1,
                    "valorAmortizacao": 180.00,
                    "valorJuros": 16.11,
                    "valorPrestacao": 196.11
                },
                [...]
            ]
        },
        {
            "tipo": "PRICE",
            "parcelas":
            [
                {
                    "numero": 1,
                    "valorAmortizacao": 173.67,
                    "valorJuros": 16.11,
                    "valorPrestacao": 189.78
                },
                [...]
            ]
        }
    ]
}

Requisitos para executar esta api:
- Python3.7 ou mais recente (preferencialmente 3.11)
- Modulos do python, instalados via pip através do comando: pip install -r requirements.txt

Como utilizar a api:
Instale o python disponivel no site: https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
Instale o modulo para criação de ambientes virtuais python (virtualenv) com o comando no powershell: pip install virtualenv
Crie o ambiente virtual com o comando no shell dentro da pasta do projeto: python -m venv venv
Inicie o ambiente virtual com o comando & ./venv/Scripts/Activate.ps1
Instale as dependecias: pip install - r requirements.txt
Inicie o servidor com o comando: python main.py


Agora podemos acessar a documentação da API pelo link http://localhost:8000/docs/ que é uma grande vantagem de utilizar fastAPI, por gerar a documentação automaticamente usando Swagger(/docs) e Redoc(/redoc)
Outro motivo de termos escolhido trabalhar com fastAPI é que podemos utilizar programação assincrona, o que torna nossa API muito mais performática, ao utilizar melhor os recursos disponiveis

Podemos testar a api agora utilizando o arquivo teste.py

