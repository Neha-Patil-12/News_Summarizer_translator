import transformers
from transformers import pipeline

summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", device=-1)
text1='''Barack Hussein Obama II is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African American to serve as president. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004. Obama was born in Honolulu, Hawaii, and graduated from Columbia University in 1983. He then worked as a community organizer before attending law school at Harvard University, where he received his law degree in 1991.'''
summary = summarizer(text1, max_length=300, min_length=100, do_sample=False)


print(summary[0]['summary_text'])