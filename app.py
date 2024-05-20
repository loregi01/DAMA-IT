from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room
from flask import request
import pika
import os
import sys
from my_email import email_functions
import mysql.connector
from dotenv import load_dotenv
import hashlib

load_dotenv()
connected_clients = {}

room_id = []

connection = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"), password=os.getenv("MYSQL_PASSWORD"), host='mysql', port="3306", database=os.getenv("MYSQL_DB"))
print("DB connected")
cursor = connection.cursor()

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('credentials')
def handle_credentials(credentials):
    can_insert = True
    cursor.execute(f'INSERT INTO statistic(TotGames, TotWins, TotDraw, Elo, SLevel) VALUES(0,0,0,0,0)')
    connection.commit()
    cursor.execute('SELECT MAX(StatisticID) FROM statistic')
    statistic_id = int(cursor.fetchall()[0][0])
    firstName = str(credentials['name'])
    #firstName[0] = firstName[0].capitalize()
    surname = str(credentials['surname'])
    #surname[0] = surname[0].capitalize()
    email = str(credentials['email'])
    password = str(credentials['password'])
    username = str(credentials['username'])
    birthdate = str(credentials['birthdate'])    

    cursor.execute(f'SELECT * FROM user WHERE Username="{username}"')
    result = cursor.fetchall()

    if result:
        can_insert = False
        socketio.emit('credentials_error', 'username', room = request.sid)    

    if can_insert:
        cursor.execute(f'INSERT INTO user(FirstName, Surname, Email, UPassword, Username, Birthdate, Statistic) VALUES ("{firstName}","{surname}","{email}","{password}","{username}","{birthdate}",{statistic_id});')
        connection.commit()
        socketio.emit('confirmation_signup')

@socketio.on('login_credentials')
def handle_login_credentials (data):
    inserted_email = data['email']
    inserted_password = data['password']

    password_encoded = inserted_password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(password_encoded)
    password = hash_object.hexdigest()

    cursor.execute(f'SELECT * FROM user WHERE Email="{inserted_email}" AND UPassword="{password}"')
    result = cursor.fetchall()    

    if result:
        socketio.emit('login_success',result, room = request.sid)   
    else:
        socketio.emit('login_unsuccess', room = request.sid) 

@socketio.on('connect_client')
def handle_connect():
    client_id = request.sid

connected_clients = {}
matched_clients = {}
@socketio.on('connect_match')
def handle_connect_match(settings):
    client_id = request.sid
    name = settings['name']
    level = settings['level']
    elo = settings['elo']

    connected_clients[client_id] = {'name': name, 'level': int(level), 'elo': int(elo)}
    print(f"{name} connected with level {level}")

    try_match_clients(client_id)

def try_match_clients(sender_id):
    sender_data = connected_clients.get(sender_id)
    sender_name = sender_data['name']
    sender_lv = sender_data['level']
    sender_elo = sender_data['elo']

    for client_id, client_data in connected_clients.items():
        if client_data['name'] != sender_name:
            if sender_elo - 50 <= client_data['level'] <= sender_elo + 50:

                matched_clients[sender_id] = client_id
                matched_clients[client_id] = sender_id
                
                join_room(sender_id)
                #join_room(client_id)

                socketio.emit('matched', f"{sender_name} is matched with {client_data['name']} in room {sender_id}", room=sender_id)
                socketio.emit('matched', f"{client_data['name']} is matched with {sender_name} in room {sender_id}", room=client_id)
                
                room_id.append(sender_id)

                #first that can send message
                #socketio.emit('starting', room=sender_id)
                break

@socketio.on('moves')
def handle_message(data):
    sender_id = request.sid
    receiver_id = matched_clients.get(sender_id)

    #if data == 'exit':
    #    socketio.emit('disconnect', room=sender_id)
    #    socketio.emit('disconnect', room=receiver_id)
    #else:
    if receiver_id:
        if receiver_id != sender_id:
            sender_name = connected_clients[sender_id]['name']
            #receiver_name = connected_clients[receiver_id]['name']
        
            socketio.emit('moves', f'{sender_name}: {data}', room=receiver_id)
            #socketio.emit('message', f'{sender_name}: {data}', room=sender_id)

@socketio.on('Statistics')
def send_statistics (username):
    cursor.execute(f'SELECT * FROM user WHERE Username="{username}"')
    result = cursor.fetchall()
    stat_id = result[0][7]
    cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id}"')
    result = cursor.fetchall()
    socketio.emit('statistic', result, room = request.sid) 

@socketio.on('Account')
def send_stats_for_account (username):
    cursor.execute(f'SELECT * FROM user WHERE Username="{username}"')
    result = cursor.fetchall()
    stat_id = result[0][7]
    cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id}"')
    result = cursor.fetchall()
    socketio.emit('account', result, room = request.sid) 

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)