from flask import Flask, render_template,session,g, jsonify,Response
from flask_session import Session
from flask import request
import sqlite3
import requests
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
    return render_template('index.html')


@app.route('/result', methods=['GET','POST'])
def result():
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
    
        
        try:
            ####translation code:
            value=request.form.get("trans",False)
            
            translater=Translator()
            para1=session.get('summary')
            
            t1=session.get('title')

            #sentence="Pune: H3N2 Virus Claims Second Life In Pimpri-Chinchwad As COVID-19 Cases Rise Again"
            TitleTransLang=translater.translate(t1, dest=value)
            textTitle=TitleTransLang.text

            # Extract text from summary
            summary_text = ""
            for s in para1:
                summary_text += s['summary_text']

            # Store summary_text in session
            summ_text = summary_text

            ParaTransLang=translater.translate(summ_text, dest=value)
            textPara=ParaTransLang.text

        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        return render_template('translate.html', textTitle=textTitle,textPara=textPara)

# route for favourites

@app.route('/add_favourite', methods=['GET', 'POST'])
def add_favourite():
    if request.method == 'POST':
        try:
            #text1 = request.form['text1']
            #s1 = BeautifulSoup(text1, 'html.parser')
            #cont = s1.find('div', {'id': 'disp'})
            #if cont is not None:
            #    div = cont.find_all('h2')
            #else:
            #    div = []
            
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO favourite (name, content) VALUES (?, ?)", (name, content))
            db.commit()
            return "Page added to favorites!"
        except Exception as e:
            return str(e)
        return render_template('add_favourite.html')



@app.route('/show_fav',methods=['GET','POST'])
def show_fav():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM favourite")
    favorites = cursor.fetchall()
    return render_template('show_fav.html', favorites=favorites)



if __name__ == "__main__":
    app.run(debug=True)