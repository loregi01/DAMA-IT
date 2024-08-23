from views.login_page import Ui_MainWindow
from views.sign_up_page import Ui_Form
from views.home_page import Ui_Form as Ui_HomePage
from views.statistics_page import Ui_Form as Ui_StatisticsPage
from views.account_page import Ui_Form as Ui_AccountPage
from views.local_championship import Ui_Form as Ui_LocalChampionshipPage
from views.global_championship import Ui_Form as Ui_GlobalChampionshipPage
from views.friends_page import Ui_MainWindow as Ui_FriendsPage
from views.chat_page import Ui_MainWindow as Ui_ChatPage
from views.board import Board
import views.sign_up_page
import views.login_page
from views.waiting import Ui_MainWindow as Ui_WaitingWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal, QSize, Qt, QRect, Signal
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
color = None

#User stats
stats = None
openStatisticPage = False

authenticated = False
Semail = None
globalChampList = []

currentpage = None

class SignUp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_window_instance = None
        self.setup_ui()
        self.ui.confirm_button.clicked.connect(self.send_credentials)
        #self.ui.confirm_button.clicked.connect(self.on_confirm_clicked)
        self.ui.go_back_label.mousePressEvent = self.on_go_back_label_clicked

    def new_window(self):
        self.close()
        window.show()
        #self.new_window_instance = HomePage()
        #self.new_window_instance = MainWindow()
        #window.homepage_window = self.new_window_instance  
        #self.new_window_instance.show()

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
        
        print("Confirm button clicked")
        self.new_window()
        
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
    new_friend_data_view = Signal(list)
    friends_data_view = Signal(list)

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
        self.new_friend_data_view.connect(self.on_new_friend_data_view)
        self.friends_data_view.connect(self.on_friends_data_view)

    def on_new_friend_data_view(self, data):
        print(data)
        self.account_page_window.friend_window.show_new_friend(data)
    
    def on_friends_data_view(self, data):
        print(data)
        self.account_page_window.friend_window.show_friend(data)
        self.account_page_window.chat_window.show_new_friend(data)
        

    def on_glob_champ_view(self):
        #self.statisticspage_window.close()
        print("CIAO")
        #print(data)
        self.statisticspage_window.close()
        self.globalchampionshippagewindow = GlobalChampionshipPage()
        self.globalchampionshippagewindow.show()

    def on_statistic_view (self):
        print("CurrentPage Statistic: ", str(currentpage))
        if currentpage == 0:   
            self.statistic_window(self.homepage_window)
        elif currentpage == 1:
            self.statistic_window(self.account_page_window)

    def on_account_view(self):
        print("CurrentPage Account: ", str(currentpage))
        if currentpage == 0:   
            self.account_window(self.homepage_window)
        elif currentpage == 2:
            self.account_window(self.statisticspage_window)

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
        self.signup_window = SignUp()  
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
    showBoard = Signal(QMainWindow)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.ui.pushButton.clicked.connect(self.game_start)
        self.ui.pushButton_6.clicked.connect(self.statistics_page)
        self.ui.pushButton_5.clicked.connect(self.account_page)
        self.statisticspage_window = None
        self.accountpage_window = None

        self.update_board.connect(self.on_update_board)
        self.showBoard.connect(self.on_showBoard)

    def on_update_board(self, data):
        #self.board._game._pieceBoard = data
        print("From on_update_board", data)
        #self.board._game._isThinking = False
        #self.board._game._myTurn = True
        self.board.updateBoard_fromOpponent(data)

    '''def setup_ui(self):
        self.ui = Ui_StatisticsPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        total_games=stats[0][1]
        total_wins=stats[0][2]
        elo=stats[0][4]
        level=stats[0][5]
        self.ui.info_label.setText(f"Total Games: {total_games}\nTotal Wins: {total_wins}\nELO: {elo}\nLevel: {level}")'''

    def statistics_page (self):
        #Retrieve data for the page
        sio.emit('Statistics', username)

    def account_page (self):
        sio.emit('Account', username)

    def setup_ui(self):
        self.ui = Ui_HomePage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        self.user_field = self.ui.label_3
        global currentpage
        currentpage = 0
    
    def game_start(self):
        window.homepage_window.close()

        connect_with_opponent()

        self.close()
        self.waitingpage = WaitingPage()
        self.waitingpage.show()

    def on_showBoard(self):
        global color
        self.board = Board("HUMAN_VS_AI", 0, color, False, False, sio)  # Create an instance of the Board class
        self.board.setFixedSize(QSize(900, 600))
        self.waitingpage.close()
        self.board.show()

class WaitingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_WaitingWindow()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

class LocalChampionshipPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_LocalChampionshipPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

class RectWidget(QWidget):
    def __init__(self, username, elo):
        super().__init__()

        # Create layout
        layout = QVBoxLayout()

        # Create and style labels
        username_label = QLabel(f"Username: {username}\nELO: {elo}")
        username_label.setStyleSheet("color: white;")
        layout.addWidget(username_label)

        # Set widget style
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: black; border-radius: 10px; border: 2px solid white;")

        # Set layout to widget
        self.setLayout(layout)

        self.setFixedSize(530, 100)

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
        layout.setAlignment(Qt.Alignment.AlignTop)
        layout.setSpacing(0)

        print(data[0])
        # Aggiungi i rettangoli al layout
        for value in data:
            rect_widget = RectWidget(value[0], value[1])
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
        
        self.ui.home_page_button.clicked.connect(self.home_page)
        self.ui.account_button.clicked.connect(self.account_page)

    def setup_ui(self):
        self.ui = Ui_StatisticsPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        total_games=stats[0][1]
        total_wins=stats[0][2]
        elo=stats[0][4]
        level=stats[0][5]
        self.ui.info_label.setText(f"Total Games: {total_games}\nTotal Wins: {total_wins}\nELO: {elo}\nLevel: {level}")

        global currentpage
        currentpage = 2

    def localchampionshippage(self):
        self.close()
        self.localchampionshippagewindow = LocalChampionshipPage()
        self.localchampionshippagewindow.show()

    def globalchampionshippage(self):
        sio.emit('GlobalChamp')

    def home_page(self):
        global currentpage
        currentpage = 0
        self.close()
        window.homepage_window.show()

    def account_page(self):
        #self.close()
        sio.emit('Account', username)
        #window.statisticspage_window.close()

class AccountPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.friend_window = FriendsPage()
        self.chat_window = ChatPage()

        self.ui.pushButton_2.clicked.connect(self.home_page)
        self.ui.pushButton_4.clicked.connect(self.statistics_page)
        self.ui.label_6.mousePressEvent = self.on_friend_clicked
        self.ui.label_5.mousePressEvent = self.on_chat_clicked

    def setup_ui(self, friend=False):

        self.ui = Ui_AccountPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale
        self.ui.label.setText(f"{firstName}")
        self.ui.label_2.setText(f"{surname}")
        level = stats[0][5]
        elo = stats[0][4]
        self.ui.label_3.setText(f"{level}")
        self.ui.label_4.setText(f"{elo}")

        global currentpage
        currentpage = 1

    def on_friend_clicked(self, event):
        self.close()
        self.friend_window.show()

    def on_chat_clicked (self, event):
        self.close()
        self.chat_window.show()

    def home_page(self):
        global currentpage
        currentpage = 0
        self.close()
        window.homepage_window.show()

    def statistics_page(self):
        #self.close()
        sio.emit('Statistics', username)
        #window.account_page_window.close()

class RectWidget1(QWidget):
    def __init__(self, name, surname, username):
        super().__init__()

        # Create layout
        layout = QVBoxLayout()

        # Create and style labels
        username_label = QLabel(f"Username: {username}\nName: {name}\nSurname: {surname}")
        username_label.setStyleSheet("color: black;")
        layout.addWidget(username_label)

        # Set widget style
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid black;")

        # Set layout to widget
        self.setLayout(layout)

        self.setFixedSize(400, 80)

class FriendsPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.take_friend()

        self.setup_ui()

        self.ui.homepage.clicked.connect(self.home_page)
        self.ui.account.clicked.connect(self.account_page)
        self.ui.statistics.clicked.connect(self.statistics_page)
        self.ui.search.clicked.connect(self.search_friend)

    def setup_ui(self):
        self.ui = Ui_FriendsPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

        global currentpage
        currentpage = 2

    def show_new_friend(self, data):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.Alignment.AlignTop)
        layout.setSpacing(10)

        # Itera su ciascun valore nei dati ricevuti
        for value in data:
            # Crea un widget orizzontale che conterrà RectWidget1 e il pulsante
            h_layout = QHBoxLayout()

            # Crea RectWidget1 (presumibilmente un widget personalizzato che mostra informazioni sull'amico)
            rect_widget = RectWidget1(value[1], value[2], value[5])

            # Crea il pulsante associato al valore corrente
            button = QPushButton("Azione per " + value[1])  # Usa value[1] per il testo del pulsante, ad esempio

            # Connetti il pulsante a un metodo che esegue un'azione
            button.clicked.connect(lambda checked, v=value[5]: self.on_friend_button_clicked(v))

            # Aggiungi RectWidget1 e il pulsante al layout orizzontale
            h_layout.addWidget(rect_widget)
            h_layout.addWidget(button)

            # Aggiungi il layout orizzontale al layout principale
            layout.addLayout(h_layout)

        container.setLayout(layout)
        self.ui.scrollArea.setWidget(container)
        self.ui.scrollArea.setWidgetResizable(True)

    def on_friend_button_clicked(self, value_friend):
        print(f"Pulsante cliccato per l'amico: {value_friend}")  # Esegui un'azione specifica con i dati dell'amico
        sio.emit('AddFriend', [username, value_friend])

    def take_friend(self):
        sio.emit('ShowFriends', username)

    def show_friend(self, data):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.Alignment.AlignTop)
        layout.setSpacing(0)
        # Aggiungi i rettangoli al layout
        for value in data:
            rect_widget = RectWidget1(value[0], value[1], value[2])
            layout.addWidget(rect_widget)

        container.setLayout(layout)
        self.ui.scrollArea_2.setWidget(container)
        self.ui.scrollArea_2.setWidgetResizable(True)

    def search_friend(self):
        new_friend = self.ui.lineEdit.text()

        if new_friend == "":
            self.ui.lineEdit.setStyleSheet("QLineEdit { border: 2px solid red; }")
        else:
            sio.emit('SearchFriend', new_friend)

    def home_page(self):
        global currentpage
        currentpage = 0
        self.close()
        window.homepage_window.show()

    def account_page(self):
        sio.emit('Account', username)
    
    def statistics_page(self):
        sio.emit('Statistics', username)

class ChatPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.take_friend()

        self.setup_ui()

        self.ui.homepage.clicked.connect(self.home_page)
        self.ui.account.clicked.connect(self.account_page)
        self.ui.statistics.clicked.connect(self.statistics_page)
        self.ui.search.clicked.connect(self.search_friend)

    def setup_ui(self):
        self.ui = Ui_ChatPage()  # Inizializza Ui_Form
        self.ui.setupUi(self)  # Imposta Ui_Form sulla finestra principale

        global currentpage
        currentpage = 2

    def show_new_friend(self, data):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.Alignment.AlignTop)
        layout.setSpacing(10)

        # Itera su ciascun valore nei dati ricevuti
        for value in data:
            # Crea un widget orizzontale che conterrà RectWidget1 e il pulsante
            h_layout = QHBoxLayout()

            # Crea RectWidget1 (presumibilmente un widget personalizzato che mostra informazioni sull'amico)
            rect_widget = RectWidget1(value[0], value[1], value[2])

            # Crea il pulsante associato al valore corrente
            button = QPushButton("Chat")  # Usa value[1] per il testo del pulsante, ad esempio

            # Connetti il pulsante a un metodo che esegue un'azione
            button.clicked.connect(lambda checked, v=value[0]: self.on_chat_button_clicked(v))

            # Aggiungi RectWidget1 e il pulsante al layout orizzontale
            h_layout.addWidget(rect_widget)
            h_layout.addWidget(button)

            # Aggiungi il layout orizzontale al layout principale
            layout.addLayout(h_layout)

        container.setLayout(layout)
        self.ui.scrollArea.setWidget(container)
        self.ui.scrollArea.setWidgetResizable(True)

    def on_chat_button_clicked(self, value_friend):
        print(value_friend)

    def take_friend(self):
        sio.emit('ShowFriends', username)

    def search_friend(self):
        new_friend = self.ui.lineEdit.text()

        if new_friend == "":
            self.ui.lineEdit.setStyleSheet("QLineEdit { border: 2px solid red; }")
        else:
            sio.emit('SearchFriend', new_friend)

    def home_page(self):
        global currentpage
        currentpage = 0
        self.close()
        window.homepage_window.show()

    def account_page(self):
        sio.emit('Account', username)
    
    def statistics_page(self):
        sio.emit('Statistics', username)

@sio.event
def FriendsData(data):
    print("FRIENDS: ")
    print(data)
    window.friends_data_view.emit(data)

@sio.event
def newFriendConfirmed(data):
    print(data)
    sio.emit('ShowFriends', username)

@sio.event
def newFriend(data):
    print("New Friend: ", data)
    #window.on_new_friend_data_view(data)
    window.new_friend_data_view.emit(data)

@sio.event
def statistic(data):
    print('Statistics')
    global stats
    stats = data 
    print(data)
    global openStatisticPage
    if openStatisticPage == True:
        window.statistic_view.emit(window)
    openStatisticPage = True
    

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
    global openStatisticPage
    sio.emit('Statistics', username)
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
    #window.signup_confirmed.emit(window.signup_window)

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
    global stats
    lv = stats[0][5]
    elo = stats[0][4]
    
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
    global color
    if data == "white":
        color = True
    else:
        color = False
    window.homepage_window.showBoard.emit(window)
    
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
