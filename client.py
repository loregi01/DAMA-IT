from views.login_page import Ui_MainWindow
from views.sign_up_page import Ui_Form
from views.home_page import Ui_Form as Ui_HomePage
from views.board import Board
import views.sign_up_page
import views.login_page
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, QSize
import sys
import hashlib
import time
import os
from my_email.email_functions import send_email

from dotenv import load_dotenv

load_dotenv()

import socketio
sio = socketio.Client()

Uname = ""

#@sio.event
#def connect():
    #sio.emit('connect_client')
    #name = input("Enter your name: ")
    #lv = input("Your game level: ")
    
    #settings = {'name': name, 'level': lv}
    #sio.emit('connect_client', settings)

authenticated = False
Semail = None
#signup_window = None
#homepage_window = None

class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_window_instance = None
        self.setup_ui()
        self.ui.confirm_button.clicked.connect(self.send_credentials)
        #self.ui.confirm_button.clicked.connect(self.on_confirm_clicked)
        self.ui.go_back_label.mousePressEvent = self.on_go_back_label_clicked

    def new_window(self):
        self.close()
        self.new_window_instance = HomePage()
        global homepage_window
        homepage_window = self.new_window_instance  
        self.new_window_instance.show()

    def on_confirm_clicked(self):
        print("Confirm button clicked")
        self.new_window()

    def main_window(self):
        self.close()
        #self.new_window_instance = SignIn()
        #global signup_window
        #self.signup_window = new_window_instance  
        self.signup_window = MainWindow()  
        self.signup_window.show()

    def on_go_back_label_clicked(self, event):
        print("Sign In label clicked")
        self.main_window()

    def setup_ui(self):
        self.ui = Ui_Form()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

    def send_credentials(self):
        self.ui.retrieve_credentials()
        name = self.ui.Rname
        if len(name) < 2:
            print("Nome troppo corto")
            self.ui.first_name.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            self.ui.first_name.setText("")
            self.ui.first_name.setPlaceholderText("Name too short")
            return
        self.ui.first_name.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")
        name = name[0].upper() + name[1:]
        surname = self.ui.Rsurname
        if len(surname) < 2:
            print("Cognome troppo corto")
            self.ui.surname.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            self.ui.surname.setText("")
            self.ui.surname.setPlaceholderText("Surname too short")
            return
        self.ui.surname.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")
        surname = surname[0].upper() + surname[1:]
        email = self.ui.Remail
        global Semail
        Semail = self.ui.Remail
        if '@' not in email:
            print('email non corretta')
            self.ui.email.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            self.ui.email.setText("")
            self.ui.email.setPlaceholderText("Missing @")
            return
        self.ui.email.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")
        birthdate = self.ui.Rbirthdate
        if len(birthdate.split('/')) != 3:
            print('data non corretta')
            self.ui.birthdate.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            self.ui.birthdate.setText("")
            self.ui.birthdate.setPlaceholderText("DD/MM/YYYY")
            return
        self.ui.birthdate.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")
        password = self.ui.Rpassword
        confirm_passwrd = self.ui.RConfirmPassword
        if password != confirm_passwrd or password == "":
            print("Password diverse")
            self.ui.password.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            self.ui.confirm_password.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            return
        self.ui.password.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")
        self.ui.confirm_password.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")
        username = self.ui.RUsername
        if len(username) < 1:
            print("Username troppo corto")
            self.ui.username.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
            self.ui.username.setText("")
            self.ui.username.setPlaceholderText("Username")
        self.ui.username.setStyleSheet("border: 2px solid white; border-radius: 10px; color: white;")

        password_encoded = password.encode('utf-8')
        hash_object = hashlib.sha256()
        hash_object.update(password_encoded)
        password = hash_object.hexdigest()

        data = {'name': name, 'surname': surname, 'email': email, 'password': password, 'username': username, 'birthdate': birthdate}
        print(f"My credentials sent... name:{name}, surname:{surname}, email:{email}, birthdate:{birthdate}, password:{password}, username:{username}")
        sio.emit('credentials', data)

    def change_username (self):
        self.ui.username.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
        self.ui.username.setText("")
        self.ui.username.setPlaceholderText("Username is already used")

class MainWindow(QMainWindow):

    #signal for comunicate between thread
    signup_confirmed = Signal(QMainWindow)
    login_success_signal = Signal(QMainWindow)
    login_unsuccess = Signal(QMainWindow)

    def __init__(self):
        super().__init__()
        self.new_window_instance = None
        if not sio.connected:
            sio.connect('http://127.0.0.1:5000')

        # Inizializza l'interfaccia utente generata da Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_login.clicked.connect(self.send_credentials)
        self.ui.lbl_signin.mousePressEvent = self.on_signin_clicked

        self.signup_window = None
        self.homepage_window = None

        #signal setup
        self.signup_confirmed.connect(self.on_confirm_clicked)
        self.login_success_signal.connect(self.on_confirm_clicked)
        self.login_unsuccess.connect(self.on_login_unsuccess)

    def on_login_unsuccess(self):
        email_field = views.login_page.email
        password_field = views.login_page.password

        email_field.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
        password_field.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
    
    def new_window1(self, old_window):
        old_window.close()
        #self.new_window_instance = HomePage()
        #global homepage_window
        #homepage_window = self.new_window_instance
        self.homepage_window = HomePage() 
        self.homepage_window.show()
        self.homepage_window.user_field.setText(f"Hi, {Uname}")

    def on_confirm_clicked(self, old_window):
        print("Confirm button clicked from MainWindow after comunication with server")
        self.new_window1(old_window)

    def new_window(self):
        self.close()
        #self.new_window_instance = SignIn()
        #global signup_window
        #self.signup_window = new_window_instance  
        self.signup_window = SignIn()  
        self.signup_window.show()

    def on_signin_clicked(self, event):
        print("Sign In label clicked")
        self.new_window()

    def send_credentials(self):
        self.ui.retrieve_credentials()
        email = self.ui.email
        password = self.ui.password
        data = {}
        data['email'] = email
        data['password'] = password
        print(f"My credentials sent... email:{email}, pass:{password}")
        sio.emit('login_credentials', data)

class HomePage(QMainWindow):
    user_field = None
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.ui.pushButton.clicked.connect(self.game_start)

    def setup_ui(self):
        self.ui = Ui_HomePage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        self.user_field = self.ui.label_3
    
    def game_start(self):
        window.homepage_window.close()
        mode = "HUMAN_VS_HUMAN"
        difficulty = 0
        playerIsWhite = True
        up = False
        turn = False
        self.board = Board(mode, difficulty, playerIsWhite, up, turn)  # Create an instance of the Board class
        self.board.setFixedSize(QSize(900, 600))
        self.board.show()


@sio.event
def login_success():
    print('Login Success')
    #global Uname
    #Uname = data
    window.login_success_signal.emit(window)

@sio.event
def login_unsuccess():
    print('Login unsuccess')
    window.login_unsuccess.emit(window)

@sio.event 
def credentials_error (type_of_error):
    username_field = views.sign_up_page.RUsername
    if type_of_error == 'username':
        print("Username used")
        username_field.setStyleSheet("border: 2px solid red; border-radius: 10px; color: red;")
        #username_field.setText("")
        #username_field.setPlaceholderText("Username is already used")

@sio.event
def confirmation_signup():
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = Semail
    print(Semail)
    subject = "SignUp Email"
    body = "Welcome in Dama-IT, you're now part of our family ;-)"
    send_email(sender_email, sender_password, receiver_email, subject, body)
    print("Mail inviata")

    #signal emit
    window.signup_confirmed.emit(window.signup_window)

    #global authenticated
    #authenticated = True
    #signup_window.on_confirm_clicked()

@sio.event
def connect():
    #name = input("Enter your name: ")
    #lv = input("Your game level: ")
    
    #settings = {'name': name, 'level': lv}
    sio.emit('connect_client')
    print('Connected to server')
'''
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
    #name = input("Enter your name: ")
    #lv = input("Your game level: ")
    
    #settings = {'name': name, 'level': lv}
    #sio.emit('connect_client', settings)
    #print('Connected to server')

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

    '''
if __name__ == "__main__":

    #sio.connect('http://127.0.0.1:5000')
    #sio.wait()

    app = QApplication(sys.argv)

    # Crea e mostra la finestra principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

'''
import socketio
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