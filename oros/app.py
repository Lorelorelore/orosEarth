from flask import Flask, render_template, request,redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime, time


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'oros'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'sDX7QWuuqTS9axnCndhSHnPQZyVgSI'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inbox')
def inbox():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM messages order by creation_date desc")
  inbox = cur.fetchall()
  cur.close()

  return render_template('mailbox.html', inbox = inbox)

@app.route('/compose')
def compose():
    return render_template('compose.html')

@app.route('/reply/<email>')
def reply(email):
    return render_template('compose.html', email = email)

@app.route('/read/<email>')
def reread(email):
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM messages where email = %s order by creation_date desc" , [email])
  conversation = cur.fetchall()
  cur.close()

  return render_template('read-mail.html', conversation = conversation)

@app.route('/mailing')
def mailing():
  return "Pass"


app.run(debug = True)