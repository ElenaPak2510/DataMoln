import json
import random
from datetime import datetime
from azure.storage.queue import QueueClient

# Azure Storage Account connection string and queue name
CONNECTION_STR = 'DefaultEndpointsProtocol=https;AccountName=alanleo;AccountKey=hkfWIp0sxPL0zyeK7fyVXmPJi9ne0hKqOzsfvM7TgcaOXT5v4D/A4TjLg8dB4+ExxMaLBXnmVnUo+AStdL7slQ==;EndpointSuffix=core.windows.net'
QUEUE_NAME = 'queueelena'

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

def send_data_to_queue(data):
    # Create a QueueClient
    queue_client = QueueClient.from_connection_string(CONNECTION_STR, QUEUE_NAME)
    
    # Send the message to the queue
    queue_client.send_message(data)

def main():
    for _ in range(10):
        data = generate_sample_data()
        send_data_to_queue(data)
        print(f"Sent data to Storage Queue: {data}")

if __name__ == "__main__":
    main()
