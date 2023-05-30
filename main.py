from fastapi import FastAPI, responses

from models import EntradaSimulacao, RetornoSimulacao, Parcela, ResultadoSimulacao, Erro
from _produtos import Lista_Produtos

from _calculo_price import simular_sistema_price as price
from _calculo_sac import simular_sistema_sac as sac
from eventhub import EventHub

app = FastAPI()

lista_produtos = Lista_Produtos()
lista_produtos.atualizar_periodicamente(5)

eventhub = EventHub()
eventhub.enviar_periodicamente(1)

@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")

@app.post("/")
async def simular_emprestimo(input:EntradaSimulacao):
    produto = lista_produtos.retorna_produto_enquadrado(input)
    if produto is None or input.prazo == 0:
        return Erro(Codigo=400, Mensagem='Não há produtos disponiveis para os parâmetros informados')

    resultado_simulacao = []
    resultado_simulacao.append(price(input.valorDesejado, input.prazo, produto.taxa_de_juros))
    resultado_simulacao.append(sac(input.valorDesejado, input.prazo, produto.taxa_de_juros))

    output = RetornoSimulacao(codigoProduto=produto.id, descricaoProduto=produto.nome, taxaJuros=produto.taxa_de_juros, resultadoSimulacao=resultado_simulacao)
    eventhub.add(output)

    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    lista_produtos.parar()
    eventhub.parar()
    
    