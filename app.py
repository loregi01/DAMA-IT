from flask import Flask, render_template
import mysql.connector
import pika

app = Flask(__name__)

connection = mysql.connector.connect(user='root', password='root', host='mysql', port="3306", database='db')
print("DB connected")

cursor = connection.cursor()
cursor.execute('Select * FROM students')
students = cursor.fetchall()
connection.close()

credentials = pika.PlainCredentials('myuser', 'mypassword')
connection = pika.BlockingConnection (pika.ConnectionParameters('172.20.0.3', 5672, '/', credentials))
channel = connection.channel()
print(channel)

print(students) 

@app.route('/')
def hello():
    return render_template("home_page.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)