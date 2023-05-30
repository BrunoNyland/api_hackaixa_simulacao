from azure.eventhub import EventHubProducerClient, EventData

def enviar_para_o_eventhub(json_simulacao):
    conn_str = "Endpoint=sb://eventhack.servicebus.windows.net/;SharedAccessKeyName=hack;SharedAccessKey=HeHeVaVqyVkntO2FnjQcs2Ilh/4MUDo4y+AEhKp8z+g=;EntityPath=simulacoes"

    with EventHubProducerClient.from_connection_string(conn_str) as producer:
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(json_simulacao))
        producer.send_batch(event_data_batch)
