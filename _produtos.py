from database import DataBase
from typing import List
from models import EntradaSimulacao
from pyodbc import OperationalError
import threading

class Produto():
    def __init__(self, id:int, nome:str, taxa_de_juros:float, prazo_minimo:int, prazo_maximo:int, valor_minimo:float, valor_maximo:float) -> None:
        self.id = id
        self.nome = nome
        self.taxa_de_juros = taxa_de_juros
        self.prazo_minimo = prazo_minimo
        self.prazo_maximo = prazo_maximo
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo

    def validar_simulacao(self, valor_desejado:float, prazo:int) -> bool:
        if self.valor_maximo is not None and valor_desejado > self.valor_maximo:
            return False
        if self.valor_minimo is not None and valor_desejado < self.valor_minimo:
            return False
        if self.prazo_maximo is not None and prazo > self.prazo_maximo:
            return False
        if self.prazo_minimo is not None and prazo < self.prazo_minimo:
            return False
        return True

    def __str__(self) -> str:
        return f'{self.nome} | Taxa: {self.taxa_de_juros} | Prazo(min-max): {self.prazo_minimo}-{self.prazo_maximo} | Valor(min-max): {self.valor_minimo}-{self.valor_maximo}'

class Lista_Produtos(List[Produto]):
    copia = []

    def __init__(self) -> None:
        super().__init__()
        self.leitura_disponivel = True

    def __str__(self) -> str:
        return ''.join([f'{i} - {produto}\n' for i, produto in enumerate(self)])

    def carregar_produtos_da_db(self):
        self.copia = self.copy()
        self.leitura_disponivel = False

        try:
            with DataBase() as db:
                rows = db.select_all()
        except OperationalError as e:
            self.leitura_disponivel = True
            return

        self.clear()
        for row in rows:
            self.append(Produto(*row))

        self.leitura_disponivel = True

    def retorna_produto_enquadrado(self, simulacao:EntradaSimulacao) -> Produto:
        if self.leitura_disponivel:
            for produto in self:
                if produto.validar_simulacao(simulacao.valorDesejado, simulacao.prazo):
                    return produto
            return None

        for produto in self.copy:
            if produto.validar_simulacao(simulacao.valorDesejado, simulacao.prazo):
                return produto
        return None

    def atualizar_periodicamente(self, intervalo_minutos:int):
        self.leitura_disponivel = False
        self.carregar_produtos_da_db()
        # print(self)
        self.timer = threading.Timer(intervalo_minutos * 60, self.atualizar_periodicamente, args=[intervalo_minutos])
        self.timer.start()

    def parar_atualizacao(self):
        if hasattr(self, 'timer'):
            print('Parando consultas na database...')
            self.timer.cancel()

if __name__ == '__main__':
    lista = Lista_Produtos()
    lista.atualizar_periodicamente(1)
