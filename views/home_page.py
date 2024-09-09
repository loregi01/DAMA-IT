from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        Form.setMinimumSize(QSize(900, 600))
        Form.setMaximumSize(QSize(900, 600))
        Form.setStyleSheet(u"background-image: url(views/graphics/background1.png);")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(270, 40, 361, 91))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 36pt \"Times New Roman\";")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 50, 141, 41))
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 20pt \"Times New Roman\";")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(340, 225, 221, 61))
        self.pushButton.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(340, 305, 221, 61))
        self.pushButton_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_4 = QPushButton(Form)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setGeometry(QRect(0, 500, 301, 101))
        self.pushButton_4.setStyleSheet(u"color: rgb(125, 125, 125);\n"
"font: 10pt \"Times New Roman\";")
        self.pushButton_5 = QPushButton(Form)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(300, 500, 301, 101))
        self.pushButton_5.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"Times New Roman\";")
        self.pushButton_6 = QPushButton(Form)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(600, 500, 301, 101))
        self.pushButton_6.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"Times New Roman\";")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"DAMA-IT", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Hi, Lorenzo", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"START GAME", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"PLAY WITH FRIENDS", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"HOMEPAGE", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"ACCOUNT", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"STATISTICS", None))

