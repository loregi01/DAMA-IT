# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'local_championship.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        Form.setStyleSheet(u"background-image: url(:/newPrefix/graphics/background1.png);")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(170, 60, 561, 451))
        self.scrollArea.setStyleSheet(u"border: 1px solid white;\n"
"border-radius: 10px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 559, 449))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(340, 0, 221, 51))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 16pt \"Times New Roman\";")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(0, 520, 301, 81))
        self.pushButton.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(300, 520, 301, 81))
        self.pushButton_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(600, 520, 301, 81))
        self.pushButton_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 0, 31, 51))
        self.label_2.setPixmap(QPixmap(u":/newPrefix/graphics/arrow.png"))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Local Championship", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"ACCOUNT", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"HOME PAGE", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"STATISTICS", None))
        self.label_2.setText("")
    # retranslateUi

