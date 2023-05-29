from models import Parcela, ResultadoSimulacao

def simular_sistema_sac(valor_desejado:float, num_parcelas:int, taxa_juros:float) -> ResultadoSimulacao:
    valor_desejado = float(valor_desejado)
    taxa_juros = float(taxa_juros)

    amortizacao_constante = valor_desejado / float(num_parcelas)
    
    parcelas = []
    saldo_devedor = valor_desejado
    for i in range(1, num_parcelas + 1):
        juros = taxa_juros * saldo_devedor
        amortizacao = amortizacao_constante
        saldo_devedor = saldo_devedor - amortizacao
     
        valor_prestacao = juros + amortizacao

        parcela = Parcela(numero=i, valorAmortizacao=round(amortizacao, 2), valorJuros=round(juros, 2), valorPrestacao=round(valor_prestacao, 2))
        parcelas.append(parcela)

    resultado = ResultadoSimulacao(tipo='SAC', parcelas=parcelas)
    return resultado
