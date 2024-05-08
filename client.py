from views.login_page import Ui_MainWindow
from views.sign_up_page import Ui_Form
import views.login_page
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
import sys
import hashlib

import socketio
sio = socketio.Client()

class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.ui.confirm_button.clicked.connect(self.send_credentials)

    def setup_ui(self):
        self.ui = Ui_Form()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

    def send_credentials(self):
        self.ui.retrieve_credentials()
        name = self.ui.Rname
        surname = self.ui.Rsurname
        email = self.ui.Remail
        birthdate = self.ui.Rbirthdate
        password = self.ui.Rpassword
        username = self.ui.RUsername

        password_encoded = password.encode('utf-8')
        hash_object = hashlib.sha256()
        hash_object.update(password_encoded)
        password = hash_object.hexdigest()

        data = {'name': name, 'surname': surname, 'email': email, 'password': password, 'username': username, 'birthdate': birthdate}
        print(f"My credentials sent... name:{name}, surname:{surname}, email:{email}, birthdate:{birthdate}, password:{password}, username:{username}")
        sio.emit('credentials', data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_window_instance = None
        sio.connect('http://127.0.0.1:5000')

        # Inizializza l'interfaccia utente generata da Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_login.clicked.connect(self.send_credentials)
        self.ui.lbl_signin.mousePressEvent = self.on_signin_clicked
    
    def new_window(self):
        self.close()
        self.new_window_instance = SignIn()  
        self.new_window_instance.show()

    def on_signin_clicked(self, event):
        print("Sign In label clicked")
        self.new_window()

    def send_credentials(self):
        self.ui.retrieve_credentials()
        email = self.ui.email
        password = self.ui.password
        #sio.connect('http://127.0.0.1:5000')
        #sio.wait()
        data = f"{email},{password}"
        print(f"My credentials sent... email:{email}, pass:{password}")
        sio.emit('credentials', data)


if __name__ == "__main__":

    #sio.connect('http://127.0.0.1:5000')
    #sio.wait()

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