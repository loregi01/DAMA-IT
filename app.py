from flask import Flask, render_template, request
import mysql.connector
import pika
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

app = Flask(__name__)

#connection = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"), password=os.getenv("MYSQL_PASSWORD"), host='mysql', port="3306", database=os.getenv("MYSQL_DB"))
#print("DB connected")

#cursor = connection.cursor()
#cursor.execute('Select * FROM students')
#students = cursor.fetchall()
#connection.close()

#cursor.execute('INSERT INTO students (FirstName, Surname) VALUES ("Lorenzo", "Russo3")')
#connection.commit()
#cursor.execute('Select * FROM students')
#students = cursor.fetchall()
#print(students)

#connection.close()


#credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USERNAME"), os.getenv("RABBITMQ_PASSWORD"))
#connection = pika.BlockingConnection (pika.ConnectionParameters(os.getenv("RABBITMQ_IP"), 5672, '/', credentials))
#channel = connection.channel()
#print(channel)

'''
@app.route('/api', methods=['POST'])
def handle_api_request():
    # Gestisci la richiesta API qui
    return "Risposta da marte4"

@app.route("/", methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        data = await request.json  # Legge i dati JSON inviati dal client
        # Puoi aggiungere qui la logica per gestire i dati ricevuti dal client
        print("Dati ricevuti:", data)
        return "Dati ricevuti"
    else:
        return "Server Flask in esecuzione"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run_async(host="0.0.0.0", port=5000))
'''

executor = ThreadPoolExecutor(max_workers=10)  # Puoi regolare il numero massimo di thread qui

def process_request(data):
    # Simula un'operazione di elaborazione dei dati
    # In questo caso, stiamo solo stampando i dati ricevuti
    print("Dati ricevuti:", data)
    #time.sleep(5)  # Simula un'elaborazione di 5 secondi
    return "Dati ricevuti: " + str(data) + " Il numero di thread attivi è " + str(len(executor._threads))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json  # Legge i dati JSON inviati dal client
        # Invoca l'operazione di elaborazione dei dati all'interno di un thread del pool
        future = executor.submit(process_request, data)
        # Attendi il completamento dell'operazione e ottieni il risultato
        result = future.result()
        # Stampa il numero di thread attivi nel pool dei thread
        print("Thread attivi nel pool:", len(executor._threads))
        return result
    else:
        return "Server Flask in esecuzione"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)