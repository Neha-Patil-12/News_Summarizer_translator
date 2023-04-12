from googletrans import Translator

translater=Translator()

sentence="Pune: H3N2 Virus Claims Second Life In Pimpri-Chinchwad As COVID-19 Cases Rise Again"
out=translater.translate(sentence, dest="hi")
print(out.text)