import numpy as np
import pandas as pd
import spacy
import en_core_web_sm
import re

from spacy.lang.en.stop_words import STOP_WORDS


nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("./NEWS sample.csv")
df = df[:10]                               # to limit the size
art = df['Summary']


# spacy for everything
def cleaning(text):
    nlp = spacy.load("en_core_web_sm")

    text_lower= text.lower()                           #convert to lower case
    num_removed = re.sub("\d+", "", text_lower)        #remove numbers
    removed_lines=re.sub('\n','',num_removed)               #remove \n
    removed_html = re.compile(r'<.*?>').sub('', removed_lines)     #remove html tags
    result=removed_html

    doc = nlp(result)
    lemmas = [t.lemma_ for t in doc if t.lemma_ not in STOP_WORDS]

    no_stop = []
    puncs = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n'"
    for lemma in lemmas:
      if lemma[-1] in puncs:
          lemma = lemma[:-1]
      if lemma not in puncs and lemma.isalpha():
          no_stop.append(lemma)

    cleaned = " ".join(no_stop)
    print(text)
    print(cleaned)
    return cleaned


cleaned_art = []
filename = "cleaned_articles_rough.csv"
f = open(filename, "w", encoding='utf-8')
# f.write("Article:\n")
for a in art:
    cleaned_each = cleaning(a)
    # f.write(cleaned_each+"\n")
    cleaned_art.append(cleaned_each)
# f.close()
df['Summary'] = cleaned_art
print(df['Summary'].head())
for a in df['Summary']:
    f.write(a+"\n")
f.close()







