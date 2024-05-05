from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    Rname = ""
    Rsurname = ""
    Remail = ""
    Rbirthdate = ""
    Rpassword = ""

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 680, 600))
        self.widget.setStyleSheet(u"background-image: url(C:/Users/gizzi/OneDrive/Desktop/DAMA-IT/views/graphics/background2.jpg);")
        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(650, 0, 251, 600))
        self.widget_2.setStyleSheet(u"background-image: url(C:/Users/gizzi/OneDrive/Desktop/DAMA-IT/views/graphics/background1.png);")
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(40, 40, 181, 91))
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 121, 51))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-size: 20pt;\n"
"text-align: center;\n"
"font-family: Times New Roman;")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(60, 140, 161, 251))
        self.widget_4.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.first_name = QTextEdit(self.widget_4)
        self.first_name.setObjectName(u"first_name")
        self.first_name.setGeometry(QRect(0, 10, 151, 31))
        self.first_name.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.first_name.setInputMethodHints(Qt.InputMethodHint.ImhHiddenText|Qt.InputMethodHint.ImhMultiLine)
        self.first_name.setFrameShape(QFrame.Shape.Box)
        self.surname = QTextEdit(self.widget_4)
        self.surname.setObjectName(u"surname")
        self.surname.setGeometry(QRect(0, 50, 151, 31))
        self.surname.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;\n"
"")
        self.surname.setFrameShape(QFrame.Shape.Box)
        self.email = QTextEdit(self.widget_4)
        self.email.setObjectName(u"email")
        self.email.setGeometry(QRect(0, 90, 151, 31))
        self.email.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;\n"
"")
        self.email.setFrameShape(QFrame.Shape.Box)
        self.birthdate = QTextEdit(self.widget_4)
        self.birthdate.setObjectName(u"birthdate")
        self.birthdate.setGeometry(QRect(0, 210, 151, 31))
        self.birthdate.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.birthdate.setFrameShape(QFrame.Shape.Box)
        self.lineEdit = QLineEdit(self.widget_4)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(0, 130, 151, 31))
        self.lineEdit.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_2 = QLineEdit(self.widget_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(0, 170, 151, 31))
        self.lineEdit_2.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(80, 390, 120, 41))
        self.confirm_utton = QPushButton(self.widget_5)
        self.confirm_utton.setObjectName(u"confirm_utton")
        self.confirm_utton.setGeometry(QRect(20, 10, 75, 24))
        self.confirm_utton.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 430, 121, 16))
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_2.setOpenExternalLinks(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"DAMA-IT", None))
        self.first_name.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.first_name.setPlaceholderText(QCoreApplication.translate("Form", u"First Name", None))
        self.surname.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.surname.setPlaceholderText(QCoreApplication.translate("Form", u"Surname", None))
        self.email.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.email.setPlaceholderText(QCoreApplication.translate("Form", u"Email", None))
        self.birthdate.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.birthdate.setPlaceholderText(QCoreApplication.translate("Form", u"Birthdate", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Password", None))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Form", u"Confirm Password", None))
        self.confirm_utton.setText(QCoreApplication.translate("Form", u"Confirm", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Click here to go back", None))
    # retranslateUi
     
    def retrieve_credentials (self):
        self.Rname = self.first_name.toPlainText()
        self.Rsurname = self.surname.toPlainText()
        self.Remail = self.email.toPlainText()
        self.Rbirthdate = self.birthdate.toPlainText()
        self.Rpassword = self.lineEdit.text()
