from fastapi import FastAPI, responses
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Input(BaseModel):
    valorDesejado: float
    prazo: int

class Parcelas(BaseModel):
    numero: int
    valorAmortizacao: float
    valorJuros: float
    valorPrestacao: float

class Simulacao(BaseModel):
    tipo: str
    parcelas: List[Parcelas]

class Output(BaseModel):
    codigoProduto: int
    descricaoProduto: str
    taxaJuros: float
    resultadoSimulacao: List[Simulacao]

@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")

@app.post("/")
async def simular_emprestimo(input_data: Input) -> Output:
    valor_desejado = input_data.valorDesejado
    prazo = input_data.prazo
    
    # sua lógica para calcular a simulação aqui
    
    output = Output(
        codigoProduto=1,
        descricaoProduto="Produto 1",
        taxaJuros=0.0179,
        resultadoSimulacao=[
            Simulacao(
                tipo="SAC",
                parcelas=[
                    Parcelas(
                        numero=1,
                        valorAmortizacao=180.00,
                        valorJuros=16.11,
                        valorPrestacao=196.11
                    ),
                    # ...
                ]
            ),
            Simulacao(
                tipo="PRICE",
                parcelas=[
                    Parcelas(
                        numero=1,
                        valorAmortizacao=173.67,
                        valorJuros=16.11,
                        valorPrestacao=189.78
                    ),
                    # ...
                ]
            )
        ]
    )

    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)