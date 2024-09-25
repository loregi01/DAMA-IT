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
    surname = str(credentials['surname'])
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
    global connected_clients
    connected_clients[client_id] = {'name': name, 'level': int(level), 'elo': int(elo), 'game': settings['game']}

    socketio.emit('debug', ["game type", settings['game']])
    if settings['game'] == 'classic':
        try_match_clients(client_id)

def try_match_clients(sender_id):
    global connected_clients
    global matched_clients
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

                socketio.emit('matched', ["white","NoFriend"], room=sender_id)
                socketio.emit('matched', ["black","NoFriend"], room=client_id)
                
                room_id.append(sender_id)

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
    type_game = connected_clients[client_id]['game']
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
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat[1]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
        cursor.execute(f'SELECT Statistic FROM user WHERE Username="{opponent_user}"')
        stat_id_opp = cursor.fetchall()[0][0]
        cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id_opp}"')
        stat_opp = cursor.fetchall()[0]
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat_opp[1]) + 1)}" WHERE StatisticID="{stat_id_opp}"')
        connection.commit()
        cursor.execute(f'UPDATE statistic SET TotWins = "{str(int(stat[2]) + 1)}" WHERE StatisticID="{stat_id}"')
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
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat[1]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
        cursor.execute(f'SELECT Statistic FROM user WHERE Username="{username}"')
        stat_id_opp = cursor.fetchall()[0][0]
        cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id_opp}"')
        stat_opp = cursor.fetchall()[0]
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat_opp[1]) + 1)}" WHERE StatisticID="{stat_id_opp}"')
        connection.commit()
        cursor.execute(f'UPDATE statistic SET TotWins = "{str(int(stat[2]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()

    socketio.emit('game_finish', [username, opponent_user, winner, type_game])



@socketio.on('moves')
def handle_message(data):
    sender_id = request.sid
    receiver_id = matched_clients.get(sender_id)

    if receiver_id:
        if receiver_id != sender_id:
            socketio.emit('moves', data, room=receiver_id)

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
    cursor.execute(f'SELECT DISTINCT UserID,Username,Statistic FROM user JOIN friend on (User2=UserID) WHERE User1={id}')
    result_temp = cursor.fetchall()
    list = []
    for temp in result_temp:
        stat_id = temp[2]
        cursor.execute(f'SELECT Elo FROM statistic WHERE StatisticID={stat_id}')
        elo = cursor.fetchall()[0][0]
        list.append((temp[1],elo))
    cursor.execute(f'SELECT Username, Elo FROM user JOIN statistic ON Statistic = StatisticID WHERE Username="{username}"')
    stat = cursor.fetchall()[0]
    list.append(stat[0], stat[1])
    socketio.emit('localchamp', list)

@socketio.on('PlayFriend')
def play_friend(data):
    client_id = request.sid
    #connected_clients[client_id] = {'name': data[0], 'level': 0, 'elo': 0}
    global waiting_queue
    socketio.emit('debug',["1", waiting_queue])
    waiting_queue.append((client_id,data[0],data[1]))
    socketio.emit('debug',["2", waiting_queue])
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
        socketio.emit('debug',["3", waiting_queue])
        waiting_queue = [t for t in waiting_queue if t[0] != client_id]
        waiting_queue = [t for t in waiting_queue if t[0] != sender_id]
        socketio.emit('debug',["4", waiting_queue])
        matched_clients[sender_id] = client_id
        matched_clients[client_id] = sender_id
                
        join_room(client_id)

        socketio.emit('matched', ["white","Friend"], room=sender_id)
        socketio.emit('matched', ["black","Friend"], room=client_id)
                                
        room_id.append(client_id)

    socketio.emit('debug',["5", waiting_queue])


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
    cursor.execute(f'SELECT DISTINCT u2.Username, u2.FirstName, u2.Surname FROM user AS u1, user AS u2, friend AS f WHERE u1.UserID = f.User1 AND u2.UserID = f.User2 AND u1.Username="{data}"')
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
    del messages[0]
    sorted_messages = sorted(messages, key=lambda x: x[2])
    socketio.emit('MessagesData', [user1, sorted_messages])


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)

@socketio.on('withdraw')
def on_withdraw(username):
    socketio.emit("debug", "1")
    client_id = None
    game_result = 2
    for key, value in connected_clients.items():
        if value.get("name") == username:
            client_id = key
            break
    socketio.emit("debug", "2")
    if not client_id:
        return
    socketio.emit("debug", "3")
    opponent_id = matched_clients[client_id] if client_id in matched_clients else None
    if opponent_id == None:
        return
    socketio.emit("debug", "4")
    opponent_user = connected_clients[opponent_id]['name']
    type_game = connected_clients[client_id]['game']
    if opponent_id in matched_clients:
        socketio.emit("debug", "first")
        del matched_clients[opponent_id]
    if client_id in matched_clients:
        socketio.emit("debug", "second")
        del matched_clients[client_id]
    if opponent_id in connected_clients:
        socketio.emit("debug", "third")
        del connected_clients[opponent_id]
    if client_id in connected_clients:
        socketio.emit("debug", "fourth")
        del connected_clients[client_id]
    socketio.emit("debug", connected_clients)
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
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat[1]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
        cursor.execute(f'SELECT Statistic FROM user WHERE Username="{opponent_user}"')
        stat_id_opp = cursor.fetchall()[0][0]
        cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id_opp}"')
        stat_opp = cursor.fetchall()[0]
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat_opp[1]) + 1)}" WHERE StatisticID="{stat_id_opp}"')
        connection.commit()
        cursor.execute(f'UPDATE statistic SET TotWins = "{str(int(stat[2]) + 1)}" WHERE StatisticID="{stat_id}"')
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
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat[1]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
        cursor.execute(f'SELECT Statistic FROM user WHERE Username="{username}"')
        stat_id_opp = cursor.fetchall()[0][0]
        cursor.execute(f'SELECT * FROM statistic WHERE StatisticID="{stat_id_opp}"')
        stat_opp = cursor.fetchall()[0]
        cursor.execute(f'UPDATE statistic SET TotGames = "{str(int(stat_opp[1]) + 1)}" WHERE StatisticID="{stat_id_opp}"')
        connection.commit()
        cursor.execute(f'UPDATE statistic SET TotWins = "{str(int(stat[2]) + 1)}" WHERE StatisticID="{stat_id}"')
        connection.commit()
    #socketio.emit("debug", [username, opponent_user, winner])
    socketio.emit('game_finish', [username, opponent_user, winner, type_game])

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
        channel.basic_publish(exchange='', routing_key='chat', body=message)
        emit('message', {'message': message, 'sender': sender}, room=room)

def rabbitmq_callback(ch, method, properties, body):
    message = body.decode()
    socketio.emit('message', {'message': message}, broadcast=True)

channel.basic_consume(queue='chat', on_message_callback=rabbitmq_callback, auto_ack=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)