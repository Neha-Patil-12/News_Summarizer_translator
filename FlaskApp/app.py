from flask import Flask, render_template,session
from flask_session import Session
from flask import request
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import secrets


app = Flask(__name__)
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
            
            ####translation code:

    
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        return render_template('dispDiv.html', title=session['title'],para=para)




@app.route('/translate', methods=['GET','POST'])
def translate():
    
        
        try:
            ####translation code:
            value=request.form.get("trans",False)
            
            translater=Translator()
            para1=session.get('para')
            
            t1=session.get('title')

        # sentence="Pune: H3N2 Virus Claims Second Life In Pimpri-Chinchwad As COVID-19 Cases Rise Again"
            TitleTransLang=translater.translate(t1, dest=value)
            textTitle=TitleTransLang.text

           # ParaTransLang=translater.translate(para1, dest=value)
            #textPara=ParaTransLang.text

        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        return render_template('translate.html', textTitle=textTitle#,textPara=textPara
        )


if __name__ == "__main__":
    app.run(debug=True)