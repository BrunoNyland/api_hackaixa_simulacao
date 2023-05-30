from azure.eventhub import EventHubProducerClient, EventData
from collections import deque
from models import RetornoSimulacao
from threading import Timer

class EventHub:
    conn_str = "Endpoint=sb://eventhack.servicebus.windows.net/;SharedAccessKeyName=hack;SharedAccessKey=HeHeVaVqyVkntO2FnjQcs2Ilh/4MUDo4y+AEhKp8z+g=;EntityPath=simulacoes"

    def __init__(self) -> None:
        self.deque:deque[RetornoSimulacao] = deque(maxlen=2000)

    def add(self, item:RetornoSimulacao):
        self.deque.append(item)

    def parar(self):
        self.enviar_para_o_eventhub()
        if hasattr(self, 'timer'):
            print('Parando gravações na database...')
            self.timer.cancel()

    def enviar_periodicamente(self, intervalo_minutos:int):
        self.enviar_para_o_eventhub()
        self.timer = Timer(intervalo_minutos * 60, self.enviar_periodicamente, args=[intervalo_minutos])
        self.timer.start()

    def enviar_para_o_eventhub(self):
        if not len(self.deque):
            return

        try:
            with EventHubProducerClient.from_connection_string(self.conn_str) as producer:
                for i in range(len(self.deque)):
                    event_data_batch = producer.create_batch()
                    event_data_batch.add(EventData(self.deque[0].json()))
                    producer.send_batch(event_data_batch)
                    print(f'Simulação do produto: {self.deque[0].descricaoProduto} enviada para o envethub')
                    self.deque.popleft()

        except BaseException as e:
            print(e)

