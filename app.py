from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request
import pika
import os
import sys
from my_email import email_functions
import mysql.connector
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()
connected_clients = {}

room_id = []
waiting_queue = []

connection = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"), password=os.getenv("MYSQL_PASSWORD"), host='mysql', port="3306", database=os.getenv("MYSQL_DB"))
print("DB connected")
cursor = connection.cursor()

credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USERNAME"), os.getenv("RABBITMQ_PASSWORD"))
connection_rabbit = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", credentials=credentials))
channel = connection_rabbit.channel()
channel.queue_declare(queue='chat')

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

                socketio.emit('matched', ["white","NoFriend"], room=sender_id)
                socketio.emit('matched', ["black","NoFriend"], room=client_id)
                            

                #socketio.emit('matched', f"{sender_name} is matched with {client_data['name']} in room {sender_id}", room=sender_id)
                #socketio.emit('matched', f"{client_data['name']} is matched with {sender_name} in room {sender_id}", room=client_id)
                
                room_id.append(sender_id)

                #first that can send message
                #socketio.emit('starting', room=sender_id)
                break

@socketio.on('game_end')
def gameEnd(data):
    username = data[0]
    game_result = data[1]

    client_id = None
    for key, value in connected_clients.items():
        if value.get("name") == username:
            client_id = key
            break
    if not client_id:
        return
    opponent_id = matched_clients[client_id] if client_id in matched_clients else None
    if opponent_id == None:
        return
    opponent_user = connected_clients[opponent_id]['name']
    if opponent_id in matched_clients:
        del matched_clients[opponent_id]
    if client_id in matched_clients:
        del matched_clients[client_id]
    if opponent_id in connected_clients:
        del connected_clients[opponent_id]
    if client_id in connected_clients:
        del connected_clients[client_id]
    
    winner = None
    if game_result == 1:
        winner = username
    elif game_result == 2:
        winner = opponent_user

    if game_result == 1:
        cursor.execute(f'SELECT Statistic FROM user WHERE Username="{username}"')
        stat_id = cursor.fetchall()[0][0]
        cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id}"')
        stat = cursor.fetchall()[0]
        cursor.execute(f'UPDATE statistic SET Elo = "{str(int(stat[4]) + 5)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
        cursor.execute(f'UPDATE statistic SET SLevel = "{str(int(stat[5]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
    else:
        cursor.execute(f'SELECT Statistic FROM user WHERE Username="{opponent_user}"')
        stat_id = cursor.fetchall()[0][0]
        cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id}"')
        stat = cursor.fetchall()[0]
        cursor.execute(f'UPDATE statistic SET Elo = "{str(int(stat[4]) + 5)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
        cursor.execute(f'UPDATE statistic SET SLevel = "{str(int(stat[5]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
    
    socketio.emit('game_finish', [username, opponent_user, winner])



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
            #sender_name = connected_clients[sender_id]['name']
            #receiver_name = connected_clients[receiver_id]['name']
        
            #socketio.emit('moves', f'{sender_name}: {data}', room=receiver_id)
            socketio.emit('moves', data, room=receiver_id)
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

@socketio.on('GlobalChamp')
def sendGlobalChamp():
    cursor.execute(f'SELECT Username,Elo FROM user JOIN statistic ON (Statistic=StatisticID)')
    result = cursor.fetchall()
    socketio.emit('globalchamp', result)

@socketio.on('LocalChamp')
def sendLocalChamp(username):
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{username}"')
    id = cursor.fetchall()[0][0]
    cursor.execute(f'SELECT UserID,Username,Statistic FROM user JOIN friend on (User2=UserID) WHERE User1={id}')
    result_temp = cursor.fetchall()
    list = []
    for temp in result_temp:
        stat_id = temp[2]
        cursor.execute(f'SELECT Elo FROM statistic WHERE StatisticID={stat_id}')
        elo = cursor.fetchall()[0][0]
        list.append((temp[1],elo))
    socketio.emit('localchamp', list)

@socketio.on('PlayFriend')
def play_friend(data):
    client_id = request.sid
    waiting_queue.append((client_id,data[0],data[1]))
    found_ab = False
    found_ba = False
    sender_id = None

    for t in waiting_queue:
        if t[1] == data[0] and t[2] == data[1]:
            found_ab = True
        if t[1] == data[1] and t[2] == data[0]:
            found_ba = True
            sender_id = t[0]
    
    if found_ab and found_ba:
        matched_clients[sender_id] = client_id
        matched_clients[client_id] = sender_id
                
        join_room(client_id)

        socketio.emit('matched', ["white","Friend"], room=sender_id)
        socketio.emit('matched', ["black","Friend"], room=client_id)
                                
        room_id.append(client_id)

    socketio.emit('debug',waiting_queue)


@socketio.on('SearchFriend')
def friend(data):
    cursor.execute(f'SELECT * FROM user WHERE Username="{data["friend"]}"')
    result = cursor.fetchall()
    if result:
        socketio.emit('newFriend', {"user":data["user"], "result":result})
    else:
        socketio.emit('newFriend', {"user":data["user"], "result":"No user found"})

@socketio.on('AddFriend')
def add_friend(data):
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{data[0]}"')
    userid1 = cursor.fetchall()[0][0]
    #socketio.emit('newFriendConfirmed', userid1)
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{data[1]}"')
    userid2 = cursor.fetchall()[0][0]
    cursor.execute(f'SELECT * FROM friend WHERE User1={userid1} AND User2={userid2}')
    if not cursor.fetchall():
        cursor.execute(f'INSERT INTO umessage(Content, MDateTime, Sender) values("none", "00/00/0000 00:00:00", "{data[0]}")')
        connection.commit()
        cursor.execute(f'SELECT MessageID FROM umessage WHERE Sender="{data[0]}"')
        messageid = cursor.fetchall()[0][0]
        cursor.execute(f'INSERT INTO friend(User1, User2, Fmessage) values({int(userid1)}, {int(userid2)}, {int(messageid)})')
        connection.commit()
        socketio.emit('newFriendConfirmed', "Friend Added")

@socketio.on('ShowFriends')
def show_friend(data):
    cursor.execute(f'SELECT u2.Username, u2.FirstName, u2.Surname FROM user AS u1, user AS u2, friend AS f WHERE u1.UserID = f.User1 AND u2.UserID = f.User2 AND u1.Username="{data}"')
    friends_data = cursor.fetchall()
    socketio.emit('FriendsData', {"user":data, "data":friends_data})

@socketio.on('retrieveMessages')
def ret_messages(data):
    user1 = data['user1']
    user2 = data['user2']
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{user1}"')
    userid1 = cursor.fetchall()[0][0]
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{user2}"')
    userid2 = cursor.fetchall()[0][0]

    cursor.execute(f'SELECT Sender, Content, MDateTime FROM friend JOIN umessage ON MessageID = Fmessage WHERE (User1 = {userid1} AND User2 = {userid2}) OR (User1 = {userid2} AND User2 = {userid1})')
    messages = cursor.fetchall()

    sorted_messages = sorted(messages, key=lambda x: x[2])
    socketio.emit('MessagesData', sorted_messages)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    #socketio.emit('rabbitmq_test', f'{username} has entered the room {room}.')
    #emit('message', {'message': f'{username} has entered the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    #emit('message', {'message': f'{username} has left the room.'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message']
    sender = data['sender']
    receiver = data['receiver']
    
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{sender}"')
    userid1 = cursor.fetchall()[0][0]
    cursor.execute(f'SELECT UserID FROM user WHERE Username="{receiver}"')
    userid2 = cursor.fetchall()[0][0]
    current_time = time.time()
    cursor.execute(f'INSERT INTO umessage(Content, MDateTime, Sender) values("{message}", "{str(current_time)}", "{sender}")')
    connection.commit()
    cursor.execute(f'SELECT MessageID FROM umessage WHERE Sender="{sender}" AND MDateTime="{str(current_time)}"')
    messageid = cursor.fetchall()[0][0]
    cursor.execute(f'INSERT INTO friend(User1, User2, Fmessage) values({int(userid1)}, {int(userid2)}, {int(messageid)})')
    connection.commit()
    if message:
        # Pubblica il messaggio su RabbitMQ
        channel.basic_publish(exchange='', routing_key='chat', body=message)
        emit('message', {'message': message, 'sender': sender}, room=room)

def rabbitmq_callback(ch, method, properties, body):
    # Invia il messaggio ricevuto a tutti i client connessi alla stanza
    message = body.decode()
    socketio.emit('message', {'message': message}, broadcast=True)
    # Consuma i messaggi dalla coda RabbitMQ

channel.basic_consume(queue='chat', on_message_callback=rabbitmq_callback, auto_ack=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)