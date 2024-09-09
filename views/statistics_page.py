from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)
from PySide6.QtCore import Qt, QUrl, QFileInfo, Signal

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        Form.setMinimumSize(QSize(900, 600))
        Form.setMaximumSize(QSize(900, 600))
        Form.setStyleSheet(u"background-image: url(views/graphics/background1.png);")
        self.statistics_label = QLabel(Form)
        self.statistics_label.setObjectName(u"statistics_label")
        self.statistics_label.setGeometry(QRect(310, 30, 281, 81))
        self.statistics_label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 26pt \"Times New Roman\";")
        self.statistics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label = QLabel(Form)
        self.info_label.setObjectName(u"info_label")
        self.info_label.setGeometry(QRect(310, 140, 281, 141))
        self.info_label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 15pt \"Times New Roman\";")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.global_championship_button = QPushButton(Form)
        self.global_championship_button.setObjectName(u"global_championship_button")
        self.global_championship_button.setGeometry(QRect(340, 300, 221, 71))
        self.global_championship_button.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-bottom-color: rgb(255, 255, 255);\n"
"font: 12pt \"Times New Roman\";")
        self.local_championship_button = QPushButton(Form)
        self.local_championship_button.setObjectName(u"local_championship_button")
        self.local_championship_button.setGeometry(QRect(340, 380, 221, 71))
        self.local_championship_button.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 12pt \"Times New Roman\";")
        self.home_page_button = QPushButton(Form)
        self.home_page_button.setObjectName(u"home_page_button")
        self.home_page_button.setGeometry(QRect(0, 500, 301, 101))
        self.home_page_button.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"Times New Roman\";")
        self.account_button = QPushButton(Form)
        self.account_button.setObjectName(u"account_button")
        self.account_button.setGeometry(QRect(300, 500, 301, 101))
        self.account_button.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"Times New Roman\";")
        self.statistics_button = QPushButton(Form)
        self.statistics_button.setObjectName(u"statistics_button")
        self.statistics_button.setEnabled(False)
        self.statistics_button.setGeometry(QRect(600, 500, 301, 101))
        self.statistics_button.setStyleSheet(u"color: rgb(125, 125, 125);\n"
"font: 10pt \"Times New Roman\";")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.statistics_label.setText(QCoreApplication.translate("Form", u"STATISTICS", None))
        self.info_label.setText(QCoreApplication.translate("Form", u"Total games: 10\n"
"Total Wins: 5\n"
"ELO:4\n"
"Level:5", None))
        self.global_championship_button.setText(QCoreApplication.translate("Form", u"GLOBAL CHAMPIONSHIP", None))
        self.local_championship_button.setText(QCoreApplication.translate("Form", u"LOCAL CHAMPIONSHIP", None))
        self.home_page_button.setText(QCoreApplication.translate("Form", u"HOMEPAGE", None))
        self.account_button.setText(QCoreApplication.translate("Form", u"ACCOUNT", None))
        self.statistics_button.setText(QCoreApplication.translate("Form", u"STATISTICS", None))

