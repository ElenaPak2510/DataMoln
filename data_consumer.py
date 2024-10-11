
import pyodbc
from azure.eventhub import EventHubConsumerClient
import json

# SQL Server credentials (Using Active Directory Integrated authentication)
server = 'elpak2510.database.windows.net'
database = 'ElenaPakDB'
driver = '{ODBC Driver 17 for SQL Server}'

# Event Hub credentials
event_hub_connection_str = '<your_event_hub_connection_string>'
event_hub_name = '<your_event_hub_name>'
consumer_group = '$Default'  # Default consumer group

# Function to handle incoming events
def on_event(partition_context, event):
    # Parse event body
    event_data = event.body_as_str(encoding='UTF-8')
    print(f"Received event: {event_data}")
    
    # Assume event data is in JSON format
    event_json = json.loads(event_data)
    
    # Connect to SQL Database using Azure AD Integrated authentication
    connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};Authentication=ActiveDirectoryIntegrated'
    
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()

        # Example: Insert into SensorData table
        insert_query = '''
        INSERT INTO SensorData (sensor_id, temperature, timestamp) 
        VALUES (?, ?, ?)
        '''
        cursor.execute(insert_query, event_json['sensor_id'], event_json['temperature'], event_json['timestamp'])
        conn.commit()
        print("Data inserted into Azure SQL Database.")

    # Update the checkpoint in Event Hub
    partition_context.update_checkpoint(event)

# Create EventHubConsumerClient to receive events
client = EventHubConsumerClient.from_connection_string(
    event_hub_connection_str,
    consumer_group,
    eventhub_name=event_hub_name
)

# Run the consumer
try:
    print("Starting the Event Hub consumer...")
    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1",  # Read from the beginning of the partition
        )
except KeyboardInterrupt:
    print("Stopped receiving.")
