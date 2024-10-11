import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

# Event Hub connection string and name
CONNECTION_STR = 'Endpoint=sb://eleventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ejoN5BANMtdKOUfHKV/yWEI0OYuc48pOk+AEhJE8U38='
EVENT_HUB_NAME = 'sensordatahub'

def generate_sample_data():
    sensor_id = random.randint(1, 100)
    temperature = round(random.uniform(20.0, 30.0), 2)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "timestamp": timestamp
    }

    json_data = json.dumps(data)
    return json_data

def send_data_to_event_hub(data):
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    event_data_batch = producer.create_batch()

    event_data_batch.add(EventData(data))
    producer.send_batch(event_data_batch)
    producer.close()

def main():
    for _ in range(10):
        data = generate_sample_data()
        send_data_to_event_hub(data)
        print(f"Sent data to Event Hub: {data}")

if __name__ == "__main__":
    main()
