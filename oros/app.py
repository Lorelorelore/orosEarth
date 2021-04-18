from flask import Flask, render_template, request,redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime, time
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'oros'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'sDX7QWuuqTS9axnCndhSHnPQZyVgSI'

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '99b318c7eb3871'
app.config['MAIL_PASSWORD'] = 'c83f0cca8003fa'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mysql = MySQL(app)
mail = Mail(app)
#@TODO Number of inbox, sent, drafts, junk thrash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inbox')
def inbox():
  cur = mysql.connection.cursor()
  cur.execute("SELECT email, isRead FROM conversation order by lastUpdate desc")
  inbox = cur.fetchall()
  cur.close()

  subjects = []

  for item in inbox:
    temp = item['email']
    cur = mysql.connection.cursor()
    cur.execute("SELECT subject, creation_date FROM messages where email = %s order by creation_date limit 1", [temp])
    user = cur.fetchone()
    cur.close()
    subjects.append( {"email": item['email'] , "subject": user['subject'], "creation_date": user['creation_date'], "isRead": item['isRead'] })
    
  return render_template('mailbox.html', inbox = subjects)

@app.route('/compose')
def compose():
    return render_template('compose.html', email = None)

@app.route('/reply/<email>')
def reply(email):
    return render_template('compose.html', email = email)

@app.route('/read/<email>')
def reread(email):

  cur =  mysql.connection.cursor()
  cur.execute("UPDATE conversation SET isRead=1 WHERE email=%s", [email])
  mysql.connection.commit()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM messages where email = %s order by creation_date desc" , [email])
  conversation = cur.fetchall()
  cur.close()

  return render_template('read-mail.html', conversation = conversation, email = email)

@app.route('/sendEmail', methods=['GET', 'POST'])
def sendEmail():
  if request.method == 'POST':
    receiver = request.form['receiver']
    subject = request.form['subject']
    body = request.form['messageBody']

    print(receiver, subject, body)
    msg = Message(subject , sender= "fdf7ed80a4-de2229@inbox.mailtrap.io", recipients  = ['fdf7ed80a4-de2229@inbox.mailtrap.io'])
    msg.html = body
    mail.send(msg)
    return redirect(url_for('inbox'))

  else:
    return redirect(url_for('inbox'))

@app.route('/mailing')
def mailing():
  return "Pass"


app.run(debug = True)