from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        Form.setStyleSheet(u"background-image: url(views/graphics/background1.png);")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(300, 40, 311, 151))
        self.frame.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 20px; \n"
"border: 2px solid #333;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 10, 141, 31))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Times New Roman\";")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 40, 141, 31))
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Times New Roman\";")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 80, 51, 31))
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(180, 80, 31, 31))
        self.label_4.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(210, 80, 41, 41))
        self.widget_2.setStyleSheet(u"image: url(views/graphics/arrow.jpg);")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(360, 120, 41, 31))
        self.widget.setStyleSheet(u"image: url(views/graphics/star.jpg);")
        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(300, 300, 301, 151))
        self.widget_3.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 20px; \n"
"border: 2px solid #333;")
        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(90, 30, 81, 41))
        self.label_5.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";")
        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(90, 80, 81, 41))
        self.label_6.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";")
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(50, 30, 41, 41))
        self.widget_4.setStyleSheet(u"image: url(views/graphics/chat.jpg);\n"
"border-color: rgb(0, 0, 0);")
        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(40, 80, 51, 41))
        self.widget_5.setStyleSheet(u"image: url(views/graphics/friends.jpg);\n"
"border-color: rgb(0, 0, 0);")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(0, 500, 301, 101))
        self.pushButton_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"Times New Roman\";")
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QRect(300, 500, 301, 101))
        self.pushButton_3.setStyleSheet(u"color: rgb(125, 125, 125);\n"
"font: 10pt \"Times New Roman\";")
        self.pushButton_4 = QPushButton(Form)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(600, 500, 301, 101))
        self.pushButton_4.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"Times New Roman\";")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Lorenzo", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Gizzi", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"10", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"10", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Chat", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Friends", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"HOMEPAGE", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"ACCOUNT ", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"STATISTICS", None))

