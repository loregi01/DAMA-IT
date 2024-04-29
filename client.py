from views.login_page import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inizializza l'interfaccia utente generata da Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Crea e mostra la finestra principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

'''import socketio
import threading
import PySide6.QtCore

sio = socketio.Client()


def send_messages():
    #while True:
    msg = input("\nEnter your message (or 'exit' to quit): ")
    
    if msg == 'exit':
        sio.emit('message', msg)
    else:
        sio.emit('message', msg)
        print("Waiting answer...\n")

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

@sio.event
def disconnect():
    print("Disconnessione in corso")
    sio.disconnect()

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5000')

    sio.wait()

'''

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
