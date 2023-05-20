from flask import Flask, render_template,session,g, jsonify,Response,redirect,url_for
from flask_session import Session
from flask import request
import sqlite3
import requests
import json
from bs4 import BeautifulSoup
from googletrans import Translator
import secrets
import transformers
from transformers import pipeline


app = Flask(__name__)

# ***Data base connection****

DATABASE="NewsProject.db"

def get_db():
    db=getattr(g,'_database',None)
    if db is None:
        db=g._database=sqlite3.connect((DATABASE))
    return db

@app.teardown_appcontext
def close_conn(exception):
    db=getattr(g,' _database',None)
    if db is not None:
        db.close()

# *** End database ***

link=""

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
secret_key = secrets.token_hex(16)
# example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000
app.config['SECRET_KEY'] = secret_key

#front page of website
@app.route('/')
def index():
        # Check if the user is logged in
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template('index.html', logged_in=logged_in)

@app.route('/loading',methods=['GET','POST'])
def loading():
    return render_template('loading.html')

@app.route('/result', methods=['GET','POST'])
def result():
    #session.clear()  # Clear session data before starting a new search
    if request.method=="POST":
        
        try:
            url=request.form["link"]
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            session['title']=soup.title.text
            para=soup.find_all("p")
            para_text = ""
            for p in para:
                para_text += p.get_text() + " "
            
            ####summarization code:
            summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", device=-1)

            session['summary'] = summarizer(para_text, max_length=300, min_length=100, do_sample=False)

    
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        return render_template('dispDiv.html',summary=session['summary'],title=session['title'])




@app.route('/translate', methods=['GET','POST'])
def translate():
        #session.clear()  # Clear session data before starting a new search
        
        try:
            ####translation code:
            session['value']=request.form.get("trans",False)
            
            translater=Translator()
            para1=session.get('summary')
            
            t1=session.get('title')

            TitleTransLang=translater.translate(t1, dest=session['value'])
            textTitle=TitleTransLang.text
            session['fav_textTitle']=textTitle
            # Extract text from summary
            summary_text = ""
            for s in para1:
                summary_text += s['summary_text']

            # Store summary_text in session
            summ_text = summary_text
            session['fav_summ_text']=summ_text

            ParaTransLang=translater.translate(summ_text, dest=session['value'])
            textPara=ParaTransLang.text
            session['fav_textPara']=textPara
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        return render_template('translate.html', textTitle=textTitle,textPara=textPara)

@app.route('/cancel', methods=['GET','POST'])
def cancel():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('index'))
    
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        uname=request.form.get('name')
        user_pass=request.form.get('password')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO register (username, password) VALUES (?, ?)", (uname,user_pass))
        db.commit()
        return render_template('login.html')
    else:
        return render_template('register.html')


# route for favorites
@app.route('/add_favorite', methods=['GET','POST'])
def add_favorite():
    
        fav_title=session.get('title')
        fav_summary=session.get('summary')
        fav_summ=json.dumps(fav_summary)
        fav_tranTitle=session.get('fav_textTitle')
        fav_tranPara=session.get('fav_textPara')
        if 'username' in session:

# insert the page into the database
            db = get_db()
            cursor = db.cursor()
            if fav_title is not None and len(fav_title.strip()) > 0:
                cursor.execute("INSERT INTO Page (title, description,transTitle,transPara,user_id) VALUES (?, ?,?,?,?)", (fav_title, fav_summ,fav_tranTitle,fav_tranPara,session['user_id']))
                page_id = cursor.lastrowid
                db.commit()
            else:
                print("Title is empty or null")
        
            return redirect(url_for('protected_page'))
        
        else:
    #  The user is not logged in, redirect to login page
            return redirect(url_for('login'))


@app.route('/show_fav',methods=['GET','POST'])
def show_fav():
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Page WHERE user_id=? ",(session['user_id'],))
        favorites = cursor.fetchall()
        return render_template('show_fav.html', favorites=favorites)
    else:
        return redirect(url_for('login'))

@app.route('/delete_fav/<int:page_id>',methods=['GET','POST'])
def delete_fav(page_id):
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM Page WHERE id = ?', (page_id,))
        db.commit()
        #flash('Page has been deleted.')
        return redirect(url_for('show_fav'))


# ***Login****
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check user credentials and authenticate
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id, username FROM register WHERE username = ? AND password = ?', (request.form['username'], request.form['password']))
        result = cursor.fetchone()
        if result is not None:
            # Store user ID in session
            session['user_id'] = result[0]
            session['username'] = result[1]
            db.close()
            return redirect(url_for('protected_page'))

        db.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/protected-page')
def protected_page():
    # Check if user is logged in
    if 'user_id' in session:
        # Retrieve user data from database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM register WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        message = 'Welcome, {}'.format(user[1])
        
        db.close()
        return render_template('protected.html', message=message)
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)