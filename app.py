from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room
from flask import request
import pika
import os
import sys
from my_email import email_functions
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"), password=os.getenv("MYSQL_PASSWORD"), host='mysql', port="3306", database=os.getenv("MYSQL_DB"))
print("DB connected")

app = Flask(__name__)
socketio = SocketIO(app)

cursor = connection.cursor()
cursor.execute('SELECT * FROM user')
users = cursor.fetchall()
#connection.close()
print(users)

#cursor.execute('INSERT INTO statistic(TotGames, TotWins, TotDraw, Elo, SLevel) VALUES("6","2","2","6","3")')
#connection.commit()
#cursor.execute('INSERT INTO user(FirstName, Surname, Email, UPassword, Username, Birthdate, Statistic) VALUES ("Maximum","Mecellum","mecellum@taccituam.it", "dockermerdum", "mmlover", "30/02/400", 2);')
#connection.commit()
#cursor.execute('Select * FROM user')
#users = cursor.fetchall()
#print(users)

"""
connected_clients = {}
matched_clients = {}

room_id = []

@socketio.on('connect_client')
def handle_connect(settings):
    client_id = request.sid
    name = settings['name']
    level = settings['level']

    connected_clients[client_id] = {'name': name, 'level': int(level)}
    print(f"{name} connected with level {level}")

    try_match_clients(client_id)

def try_match_clients(sender_id):
    sender_data = connected_clients.get(sender_id)
    sender_name = sender_data['name']
    sender_lv = sender_data['level']

    for client_id, client_data in connected_clients.items():
        if client_data['name'] != sender_name:
            if sender_lv - 50 <= client_data['level'] <= sender_lv + 50:

                matched_clients[sender_id] = client_id
                matched_clients[client_id] = sender_id
                
                join_room(sender_id)
                #join_room(client_id)

                socketio.emit('matched', f"{sender_name} is matched with {client_data['name']} in room {sender_id}", room=sender_id)
                socketio.emit('matched', f"{client_data['name']} is matched with {sender_name} in room {sender_id}", room=client_id)
                
                room_id.append(sender_id)

                #first that can send message
                socketio.emit('starting', room=sender_id)
                break

@socketio.on('message')
def handle_message(data):
    sender_id = request.sid
    receiver_id = matched_clients.get(sender_id)

    if data == 'exit':
        socketio.emit('disconnect', room=sender_id)
        socketio.emit('disconnect', room=receiver_id)
    else:
        if receiver_id:
            if receiver_id != sender_id:
                sender_name = connected_clients[sender_id]['name']
                #receiver_name = connected_clients[receiver_id]['name']
            
                socketio.emit('message', f'{sender_name}: {data}', room=receiver_id)
                #socketio.emit('message', f'{sender_name}: {data}', room=sender_id)

@socketio.on('credentials')
def handle_credentials(credentials):
    print(credentials)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO students (FirstName, Surname) VALUES ("Lorenzo", "Russo3")')
    connection.commit()
    #cursor.execute('Select * FROM students')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)


from flask import Flask, render_template
import mysql.connector
import pika
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)

connection = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"), password=os.getenv("MYSQL_PASSWORD"), host='mysql', port="3306", database=os.getenv("MYSQL_DB"))
print("DB connected")

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

#@app.route('/api', methods=['POST'])
#def handle_api_request():
    # Gestisci la richiesta API qui
#    return "Risposta da marte4"

"""

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=5000) 