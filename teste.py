from typing import List

from requests import Session
from random import uniform, randint
from codetiming import Timer

from _produtos import Lista_Produtos
from models import EntradaSimulacao

lista_produto = Lista_Produtos()
lista_produto.carregar_produtos_da_db()

print(lista_produto)



lista_de_simulacoes:List[EntradaSimulacao] = []

for i in range(200):
    produto = lista_produto[randint(0, len(lista_produto) -1)]
    valor_maximo = float(produto.valor_maximo) if produto.valor_maximo is not None else float(produto.valor_minimo) * 2.0
    prazo_maximo = produto.prazo_maximo if produto.prazo_maximo is not None else produto.prazo_minimo*2
    valor_desejado = round(uniform(float(produto.valor_minimo), float(valor_maximo)), 2)
    prazo = randint(produto.prazo_minimo, prazo_maximo)
    lista_de_simulacoes.append(EntradaSimulacao(valorDesejado=valor_desejado, prazo=prazo))

for i, simulacao in enumerate(lista_de_simulacoes):
    print(f'Simulação {i} - Valor desejado: {simulacao.valorDesejado} - Prazo: {simulacao.prazo}')


@Timer()
def simula(link):
    print(link)
    with Session() as s:
        for simulacao in lista_de_simulacoes:
            response = s.post(link, data=simulacao.json())

simula('http://localhost:8000/')
simula('https://apphackaixades.azurewebsites.net/api/Simulacao')