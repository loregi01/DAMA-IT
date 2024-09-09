
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 0, 900, 600))
        self.label_2.setMouseTracking(True)
        self.label_2.setPixmap(QPixmap(u"views/graphics/background1.png"))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(360, 30, 161, 51))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 20pt \"Times New Roman\";")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(190, 190, 491, 101))
        self.scrollArea.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 489, 99))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.search = QPushButton(self.centralwidget)
        self.search.setObjectName(u"search")
        self.search.setGeometry(QRect(510, 100, 71, 41))
        self.search.setStyleSheet(u"border-radius: 8px;\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(280, 100, 221, 41))
        self.lineEdit.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 8px;\n"
"padding-left: 5px\n"
"")
        self.homepage = QPushButton(self.centralwidget)
        self.homepage.setObjectName(u"homepage")
        self.homepage.setGeometry(QRect(0, 500, 301, 101))
        self.homepage.setStyleSheet(u"font: 10pt \"Times New Roman\";\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(views/graphics/background1.png);")
        self.account = QPushButton(self.centralwidget)
        self.account.setObjectName(u"account")
        self.account.setGeometry(QRect(300, 500, 301, 101))
        self.account.setStyleSheet(u"font: 10pt \"Times New Roman\";\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(views/graphics/background1.png);")
        self.statistics = QPushButton(self.centralwidget)
        self.statistics.setObjectName(u"statistics")
        self.statistics.setGeometry(QRect(600, 500, 301, 101))
        self.statistics.setStyleSheet(u"font: 10pt \"Times New Roman\";\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(views/graphics/background1.png);")
        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setGeometry(QRect(190, 320, 491, 171))
        self.scrollArea_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 489, 169))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 170, 191, 16))
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(190, 300, 251, 16))
        self.label_6.setStyleSheet(u"color: rgb(255, 255, 255);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"FRIENDS", None))
        self.search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search to follow someone...", None))
        self.homepage.setText(QCoreApplication.translate("MainWindow", u"HOMEPAGE", None))
        self.account.setText(QCoreApplication.translate("MainWindow", u"ACCOUNT", None))
        self.statistics.setText(QCoreApplication.translate("MainWindow", u"STATISTICS", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Searched friend:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Players you already follow:", None))

