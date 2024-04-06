from flask import Flask, render_template
import mysql.connector
import pika
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)

#connection = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"), password=os.getenv("MYSQL_PASSWORD"), host='mysql', port="3306", database=os.getenv("MYSQL_DB"))
#print("DB connected")

#cursor = connection.cursor()
#cursor.execute('Select * FROM students')
#students = cursor.fetchall()
#connection.close()

#credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USERNAME"), os.getenv("RABBITMQ_PASSWORD"))
#connection = pika.BlockingConnection (pika.ConnectionParameters(os.getenv("RABBITMQ_IP"), 5672, '/', credentials))
#channel = connection.channel()
#print(channel)

#print(students) 

@app.route('/api', methods=['POST'])
def handle_api_request():
    # Gestisci la richiesta API qui
    return "Risposta dal server Flask"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
