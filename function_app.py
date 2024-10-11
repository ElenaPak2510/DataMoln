#import azure.functions as func
#import logging

#app = func.FunctionApp()

#@app.queue_trigger(arg_name="azqueue", queue_name="queueelena",
                               #connection="AzureWebJobsStorage") 
#def queue_trigger1(azqueue: func.QueueMessage):
    #logging.info('Python Queue trigger processed a message: %s',
                #azqueue.get_body().decode('utf-8'))



import logging
import pyodbc

# SQL Server credentials
server = 'elpak2510.database.windows.net'
database = 'ElenaPakDB'
username = 'ElenaPak2510'
password = 'your_passwordAlanIsmatPark2023'
driver = '{ODBC Driver 17 for SQL Server}'

def main(msg: str):
    logging.info(f"Queue trigger function processed a message: {msg}")
    
    # Connect to Azure SQL Database
    conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()

        # Assume the queue message is in JSON format
        # Insert data into SQL Database (modify based on your table schema)
        insert_query = "INSERT INTO SensorData (sensor_id, temperature, timestamp) VALUES (?, ?, ?)"
        
        # Example: Parsing the message (assuming JSON structure)
        message_data = json.loads(msg)
        cursor.execute(insert_query, message_data['sensor_id'], message_data['temperature'], message_data['timestamp'])
        conn.commit()
