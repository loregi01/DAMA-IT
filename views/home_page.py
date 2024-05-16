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
        Form.setStyleSheet(u"background-image: url(views/graphics/background1.png);\n"
"font: 14pt \"Times New Roman\";")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 30, 261, 91))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 26pt \"Times New Roman\";")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(250, 140, 211, 81))
        self.pushButton.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_7 = QPushButton(Form)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(250, 240, 211, 81))
        self.pushButton_7.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_8 = QPushButton(Form)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(250, 340, 211, 81))
        self.pushButton_8.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_9 = QPushButton(Form)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setEnabled(False)
        self.pushButton_9.setGeometry(QRect(0, 520, 221, 81))
        self.pushButton_9.setStyleSheet(u"color: rgb(150, 150, 150);")
        self.pushButton_10 = QPushButton(Form)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(220, 520, 231, 81))
        self.pushButton_10.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_11 = QPushButton(Form)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(450, 520, 231, 81))
        self.pushButton_11.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 40, 141, 41))
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 16pt \"Times New Roman\";")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"DAMA-IT", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"CREATE GAME", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"JOIN GAME", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"PLAY WITH FRIENDS", None))
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"HOME PAGE", None))
        self.pushButton_10.setText(QCoreApplication.translate("Form", u"ACCOUNT", None))
        self.pushButton_11.setText(QCoreApplication.translate("Form", u"STATISTICS", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Hi, Lorenzo", None))
    # retranslateUi

