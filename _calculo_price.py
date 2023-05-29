from models import Parcela, ResultadoSimulacao

def simular_sistema_price(valor_desejado:float, num_parcelas:int, taxa_juros:float) -> ResultadoSimulacao:
    valor_desejado = float(valor_desejado)
    taxa_juros = float(taxa_juros)

    valor_parcela = (valor_desejado * ((1.0 + taxa_juros)**num_parcelas) * taxa_juros) / (((1 + taxa_juros)**num_parcelas) - 1)
    
    parcelas = []
    saldo_devedor = valor_desejado
    for i in range(1, num_parcelas + 1):
        juros = taxa_juros * saldo_devedor
        amortizacao = valor_parcela - juros
        saldo_devedor = saldo_devedor - amortizacao
        parcela = Parcela(numero=i, valorAmortizacao=round(amortizacao, 2), valorJuros=round(juros, 2), valorPrestacao=round(valor_parcela, 2))
        parcelas.append(parcela)

    resultado = ResultadoSimulacao(tipo='PRICE', parcelas=parcelas)
    return resultado
