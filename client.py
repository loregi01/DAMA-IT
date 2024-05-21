from views.login_page import Ui_MainWindow
from views.sign_up_page import Ui_Form
from views.home_page import Ui_Form as Ui_HomePage
from views.statistics_page import Ui_Form as Ui_StatisticsPage
from views.account_page import Ui_Form as Ui_AccountPage
from views.local_championship import Ui_Form as Ui_LocalChampionshipPage
from views.global_championship import Ui_Form as Ui_GlobalChampionshipPage
from views.board import Board
import views.sign_up_page
import views.login_page
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtGui import QPainter, QColor, QFont
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

#data logged user
firstName = ""
surname = ""
email = ""
username = ""
birthdate = ""

#User stats
stats = None

authenticated = False
Semail = None
globalChampList = []

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
        window.homepage_window = self.new_window_instance  
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
    statistic_view = Signal(QMainWindow)
    account_view = Signal(QMainWindow)
    glob_champ_view = Signal(QMainWindow)

    def __init__(self):
        super().__init__()
        self.new_window_instance = None
        if not sio.connected:
            sio.connect('http://127.0.0.1:5000')
            #sio.connect('http://192.168.232.16:5000')

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
        self.statistic_view.connect(self.on_statistic_view)    
        self.account_view.connect(self.on_account_view)
        self.glob_champ_view.connect(self.on_glob_champ_view)

    def on_glob_champ_view(self):
        #self.statisticspage_window.close()
        print("CIAO")
        #print(data)
        self.globalchampionshippagewindow = GlobalChampionshipPage()
        self.globalchampionshippagewindow.show()

    def on_statistic_view (self):
        self.statistic_window(self.homepage_window)

    def on_account_view(self):
        self.account_window(self.homepage_window)

    def statistic_window (self, old_window):
        old_window.close()
        self.statisticspage_window = StatisticsPage()
        self.statisticspage_window.show()

    def account_window (self, old_window):
        old_window.close()
        self.account_page_window = AccountPage()
        self.account_page_window.show()

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
        self.homepage_window.user_field.setStyleSheet("color: white; font-size: 18px;")
        self.homepage_window.user_field.setText(f"Hi, {username}")

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
    update_board = Signal(QMainWindow)
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.ui.pushButton.clicked.connect(self.game_start)
        self.ui.pushButton_6.clicked.connect(self.statistics_page)
        self.ui.pushButton_5.clicked.connect(self.account_page)
        self.statisticspage_window = None
        self.accountpage_window = None

        self.update_board.connect(self.on_update_board)

    def on_update_board(self, data):
        #self.board._game._pieceBoard = data
        print("From on_update_board", data)
        #self.board._game._isThinking = False
        #self.board._game._myTurn = True
        self.board.updateBoard_fromOpponent(data)

    def setup_ui(self):
        self.ui = Ui_StatisticsPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        total_games=stats[0][1]
        total_wins=stats[0][2]
        elo=stats[0][4]
        level=stats[0][5]
        self.ui.info_label.setText(f"Total Games: {total_games}\nTotal Wins: {total_wins}\nELO: {elo}\nLevel: {level}")

    def statistics_page (self):
        #Retrieve data for the page
        sio.emit('Statistics', username)

    def account_page (self):
        sio.emit('Account', username)

    def setup_ui(self):
        self.ui = Ui_HomePage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        self.user_field = self.ui.label_3
    
    def game_start(self):
        window.homepage_window.close()
        mode = "HUMAN_VS_AI"
        difficulty = 0
        playerIsWhite = input("Enter color white or black (true or false): ")
        # Conversione in variabile booleana
        if playerIsWhite.lower() == 'true':
            playerIsWhite = True
        elif playerIsWhite.lower() == 'false':
            playerIsWhite = False
        up = False
        turn = False
        connect_with_opponent()
        self.board = Board(mode, difficulty, playerIsWhite, up, turn, sio)  # Create an instance of the Board class
        self.board.setFixedSize(QSize(900, 600))
        self.board.show()


class LocalChampionshipPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_LocalChampionshipPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

class RectWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.initUI()
        
    def initUI(self):
        # Imposta un layout per il widget rettangolo
        layout = QVBoxLayout()
        label = QLabel(self.text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(200, 100)  # Dimensioni fisse del rettangolo

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.setBrush(QColor(200, 200, 255))
        painter.drawRect(rect)

class GlobalChampionshipPage(QMainWindow):
    #update_champ = Signal(QMainWindow)
        
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.on_update_champ(globalChampList)
        #self.update_champ.connect(self.on_update_champ)

    def setup_ui(self):
        self.ui = Ui_GlobalChampionshipPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
    
    def on_update_champ(self, data):
        print(data)
        container = QWidget()
        layout = QVBoxLayout()

        # Aggiungi i rettangoli al layout
        for value in data[0]:
            rect_widget = RectWidget(value)
            layout.addWidget(rect_widget)

        container.setLayout(layout)
        self.ui.scrollArea.setWidget(container)
        self.ui.scrollArea.setWidgetResizable(True)


class StatisticsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.localchampionshippagewindow = None
        self.globalchampionshippagewindow = None
        self.ui.local_championship_button.clicked.connect(self.localchampionshippage)
        self.ui.global_championship_button.clicked.connect(self.globalchampionshippage)

    def setup_ui(self):
        self.ui = Ui_StatisticsPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        total_games=stats[0][1]
        total_wins=stats[0][2]
        elo=stats[0][4]
        level=stats[0][5]
        self.ui.info_label.setText(f"Total Games: {total_games}\nTotal Wins: {total_wins}\nELO: {elo}\nLevel: {level}")

    def localchampionshippage(self):
        self.close()
        self.localchampionshippagewindow = LocalChampionshipPage()
        self.localchampionshippagewindow.show()

    def globalchampionshippage(self):
        sio.emit('GlobalChamp')

class AccountPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_AccountPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        self.ui.label.setText(f"{firstName}")
        self.ui.label_2.setText(f"{surname}")
        level = stats[0][5]
        elo = stats[0][4]
        self.ui.label_3.setText(f"{level}")
        self.ui.label_4.setText(f"{elo}")


@sio.event
def statistic(data):
    print('Statistics')
    global stats
    stats = data 
    print(data)
    window.statistic_view.emit(window)

@sio.event
def account(data):
    print('Account')
    global stats
    stats = data
    window.account_view.emit(window)

@sio.event
def login_success(data):
    print('Login Success')
    #global Uname
    #Uname = data
    print(data[0])
    global firstName
    firstName = data[0][1]
    global surname
    surname = data[0][2]
    global email
    email = data[0][3]
    global username
    username = data[0][5]
    global birthdate
    birthdate = data[0][6]
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


def update(data):
    print("UPDATE")
    #window.homepage_window.update_board.emit(data)
    window.homepage_window.on_update_board(data)

def connect_with_opponent():
    name = username
    lv = 10
    elo = 60
    #lv = stats[0][5]
    #elo = stats[0][4]
    
    settings = {'name': name, 'level': lv, 'elo': elo}
    sio.emit('connect_match', settings)
    print('Connected to server')

@sio.event
def moves(data):
    print(data)
    update(data)

'''@sio.event
def starting():
    #print(data)
    send_messages()'''

@sio.event
def matched(data):
    print(data)
    # Start the thread for sending messages ????
    #send_messages()
@sio.event
def globalchamp(data):
    sorted_data = sorted(data, key=lambda x: (int(x[1]), x[0]))
    print(sorted_data)
    global globalChampList
    globalChampList = sorted_data
    window.glob_champ_view.emit(window)
    #window.statisticspage_window.globalchampionshippagewindow.on_update_champ(sorted_data)



if __name__ == "__main__":

    #sio.connect('http://127.0.0.1:5000')
    #sio.wait()

    app = QApplication(sys.argv)

    # Crea e mostra la finestra principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
