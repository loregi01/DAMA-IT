import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path=None):
    # Configura i dettagli del messaggio
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Aggiungi il corpo del messaggio
    message.attach(MIMEText(body, 'plain'))

    # Connettiti al server SMTP di Gmail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Avvia il server in modalità TLS
        server.login(sender_email, sender_password)  # Effettua l'accesso all'account Gmail

        # Invia il messaggio
        server.sendmail(sender_email, receiver_email, message.as_string())


'''
 Esempio di utilizzo
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = "russolorenzo58@gmail.com"
    subject = "Test email"
    body = "Questo è un test email inviato da Python!"
    email_functions.send_email(sender_email, sender_password, receiver_email, subject, body)
    print("Mail inviata")
'''