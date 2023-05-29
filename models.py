from pydantic import BaseModel
from typing import List

class EntradaSimulacao(BaseModel):
    valorDesejado: float
    prazo: int

class Parcela(BaseModel):
    numero: int
    valorAmortizacao: float
    valorJuros: float
    valorPrestacao: float

class ResultadoSimulacao(BaseModel):
    tipo: str
    parcelas: List[Parcela]

class RetornoSimulacao(BaseModel):
    codigoProduto: int
    descricaoProduto: str
    taxaJuros: float
    resultadoSimulacao: List[ResultadoSimulacao]

class Erro(BaseModel):
    Codigo: int
    Mensagem: str