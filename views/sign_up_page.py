from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtCore import Qt, QUrl, QFileInfo, Signal
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QWidget)


RUsername = ""

class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("color: blue; text-decoration: underline;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class Ui_Form(object):
    Rname = ""
    Rsurname = ""
    Remail = ""
    Rbirthdate = ""
    Rpassword = ""
    RConfirmPassword = ""
    RUsernameField = None
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        Form.setMinimumSize(QSize(900, 600))
        Form.setMaximumSize(QSize(900, 600))
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 680, 600))
        self.widget.setStyleSheet(u"background-image: url(views/graphics/background2.jpg);")
        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(650, 0, 251, 600))
        self.widget_2.setStyleSheet(u"background-image: url(views/graphics/background1.png);")
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(40, 40, 181, 111))
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 121, 51))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-size: 20pt;\n"
"text-align: center;\n"
"font-family: Times New Roman;")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(60, 140, 161, 281))
        self.widget_4.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.first_name = QTextEdit(self.widget_4)
        self.first_name.setObjectName(u"first_name")
        self.first_name.setGeometry(QRect(0, 0, 151, 31))
        self.first_name.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.first_name.setInputMethodHints(Qt.InputMethodHint.ImhHiddenText|Qt.InputMethodHint.ImhMultiLine)
        self.first_name.setFrameShape(QFrame.Shape.Box)
        self.surname = QTextEdit(self.widget_4)
        self.surname.setObjectName(u"surname")
        self.surname.setGeometry(QRect(0, 40, 151, 31))
        self.surname.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;\n"
"")
        self.surname.setFrameShape(QFrame.Shape.Box)
        self.email = QTextEdit(self.widget_4)
        self.email.setObjectName(u"email")
        self.email.setGeometry(QRect(0, 80, 151, 31))
        self.email.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;\n"
"")
        self.email.setFrameShape(QFrame.Shape.Box)
        self.birthdate = QTextEdit(self.widget_4)
        self.birthdate.setObjectName(u"birthdate")
        self.birthdate.setGeometry(QRect(0, 160, 151, 31))
        self.birthdate.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.birthdate.setFrameShape(QFrame.Shape.Box)
        self.password = QLineEdit(self.widget_4)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(0, 200, 151, 31))
        self.password.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password = QLineEdit(self.widget_4)
        self.confirm_password.setObjectName(u"confirm_password")
        self.confirm_password.setGeometry(QRect(0, 240, 151, 31))
        self.confirm_password.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.username = QTextEdit(self.widget_4)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(0, 120, 151, 31))
        self.username.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"color: white;\n"
"text-align: center;\n"
"")
        self.username.setFrameShape(QFrame.Shape.Box)
        global RUsername
        RUsername = self.username
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(70, 430, 141, 91))
        self.confirm_button = QPushButton(self.widget_5)
        self.confirm_button.setObjectName(u"confirm_button")
        self.confirm_button.setGeometry(QRect(30, 0, 75, 24))
        self.confirm_button.setStyleSheet(u"border: 1px solid #ccc;\n"
"border-radius: 10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.go_back_label = ClickableLabel("go_back_label", parent=self.widget_2)
        self.go_back_label.setObjectName(u"go_back_label")
        self.go_back_label.setGeometry(QRect(80, 470, 121, 16))
        self.go_back_label.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.go_back_label.setOpenExternalLinks(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

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
        self.password.setText("")
        self.password.setPlaceholderText(QCoreApplication.translate("Form", u"Password", None))
        self.confirm_password.setText("")
        self.confirm_password.setPlaceholderText(QCoreApplication.translate("Form", u"Confirm Password", None))
        self.username.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.username.setPlaceholderText(QCoreApplication.translate("Form", u"Username", None))
        self.confirm_button.setText(QCoreApplication.translate("Form", u"Confirm", None))
        self.go_back_label.setText(QCoreApplication.translate("Form", u"Click here to go back", None))

    def retrieve_credentials (self):
        self.Rname = self.first_name.toPlainText()
        self.Rsurname = self.surname.toPlainText()
        self.Remail = self.email.toPlainText()
        self.RUsername = self.username.toPlainText()
        self.Rbirthdate = self.birthdate.toPlainText()
        self.Rpassword = self.password.text()
        self.RConfirmPassword = self.confirm_password.text()