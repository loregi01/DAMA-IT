import socketio
import threading
import PySide6.QtCore

sio = socketio.Client()


def send_messages():
    #while True:
    msg = input("\nEnter your message (or 'exit' to quit): ")
    
    if msg.lower() == 'exit':
        sio.disconnect()
    
    sio.emit('message', msg)
    print("Waiting answer...\n")
    #sio.disconnect()

@sio.event
def connect():
    name = input("Enter your name: ")
    lv = input("Your game level: ")
    
    settings = {'name': name, 'level': lv}
    sio.emit('connect_client', settings)
    print('Connected to server')

@sio.event
def message(data):
    print(data)
    send_messages()

@sio.event
def starting():
    #print(data)
    send_messages()

@sio.event
def matched(data):
    print(data)
    # Start the thread for sending messages ????
    #send_messages()

if __name__ == '__main__':
    #sio.connect('http://127.0.0.1:5000')

    #sio.wait()

    # Prints PySide6 version
    print(PySide6.__version__)

    # Prints the Qt version used to compile PySide6
    print(PySide6.QtCore.__version__)


'''import requests

def invia_richiesta_al_server():
    url = 'http://127.0.0.1:5000/api'
    dati = {'key': 'value'}  # Dati da inviare al server Flask
    response = requests.post(url, json=dati)
    if response.status_code == 200:
        print("Richiesta inviata con successo!")
        print("Risposta dal server:", response.text)
    else:
        print("Errore durante l'invio della richiesta:", response.status_code)

if __name__ == "__main__":
    invia_richiesta_al_server()'''
