from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


app = Flask(__name__)
link=""
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
            title=soup.title.text
            para=soup.find_all("p")

            ####translation code:

            translater=Translator()

            #sentence="Pune: H3N2 Virus Claims Second Life In Pimpri-Chinchwad As COVID-19 Cases Rise Again"
            out=translater.translate(title, dest="hi")
            textTitle=out.text

        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        return render_template('dispDiv.html', title=title,para=para,textTitle=textTitle)


if __name__ == "__main__":
    app.run(debug=True)