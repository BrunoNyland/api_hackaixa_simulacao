from typing import List

from requests import Session
from random import uniform, randint
from codetiming import Timer

from _produtos import Lista_Produtos
from models import EntradaSimulacao

lista_produto = Lista_Produtos()
lista_produto.carregar_produtos_da_db()

print(lista_produto)

import json

testes = {
    'Parametros Vazios':{},
    'Parametros Incompletos':{'prazo':20},
    'Parametros Incompletos 2':{'valorDesejado':200.0},
    'Prazo Negativo':{'valorDesejado':200.0, 'prazo':-1},
    'Prazo Zero':{'valorDesejado':200.0, 'prazo':0},
    'Prazo Float':{'valorDesejado':200.0, 'prazo':0.5},
    'Prazo Vazio':{'valorDesejado':200.0, 'prazo':None},
    'Prazo String':{'valorDesejado':200.0, 'prazo':'aushduahudas'},
    'Prazo String Vazia':{'valorDesejado':200.0, 'prazo':''},
    'Prazo Lista':{'valorDesejado':200.0, 'prazo':[10, 20, 30]},
    'Prazo Dicionario':{'valorDesejado':200.0, 'prazo':{}},
    'Parametros extras':{'valorDesejado':200.0, 'prazo':5, 'Parametro Teste':20},
    'Prazo Muito Grande':{'valorDesejado':20000000000000.0, 'prazo':9999},
}
lista_de_simulacoes:List[EntradaSimulacao] = []

# for i in range(200):
#     produto = lista_produto[randint(0, len(lista_produto) -1)]
#     valor_maximo = float(produto.valor_maximo) if produto.valor_maximo is not None else float(produto.valor_minimo) * 2.0
#     prazo_maximo = produto.prazo_maximo if produto.prazo_maximo is not None else produto.prazo_minimo*2
#     valor_desejado = round(uniform(float(produto.valor_minimo), float(valor_maximo)), 2)
#     prazo = randint(produto.prazo_minimo, prazo_maximo)
#     lista_de_simulacoes.append(EntradaSimulacao(valorDesejado=valor_desejado, prazo=prazo))

# for i, simulacao in enumerate(lista_de_simulacoes):
#     print(f'Simulação {i} - Valor desejado: {simulacao.valorDesejado} - Prazo: {simulacao.prazo}')


@Timer()
def simula(link):
    with Session() as s:
        for teste, payload in testes.items():
            response = s.post(link, data=json.dumps(payload))
            print(teste)
            print(response.content.decode('utf-8'))
            print()

simula('http://localhost:8000/')
