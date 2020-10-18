import numpy as np
import pandas as pd
import spacy
import en_core_web_sm
import re
import timeit

from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer

# Start time
start = timeit.default_timer()


nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("./NEWS.csv")
# df = df[]                               # to limit the size
art = df['Summary']

global counter
counter = 0

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
    global counter
    if counter % 100 == 0:
        print("Article no. " + str(counter))
    counter += 1

    # print(text)
    # print(cleaned)
    return cleaned


cleaned_art = []
print("Cleaning articles-")
# for a in art:
#     cleaned_each = cleaning(a)
#     cleaned_art.append(cleaned_each)


filename = "cleaned_articles_rough.csv"
f = open(filename, "w", encoding='utf-8')
f.write("Id, Articles")
for a in art:
    try:
        # print(a)
        cleaned_each = cleaning(a)
        f.write(cleaned_each+"\n")
        cleaned_art.append(cleaned_each)
    except AttributeError:
        pass
f.close()



# TFIDF
tfidf = TfidfVectorizer(
    min_df =0.0,
    max_df = 0.95,
    max_features = 8000,
    # stop_words = nlp.Defaults.stop_words,
    # vocabulary=vocab,
    ngram_range=(1,2),
)


x = tfidf.fit_transform(cleaned_art)

# saving TFIDF's
filename = "tfidf_main.csv"
f=open(filename, "w", encoding='utf-8')
print("Opened file...")


for each in tfidf.get_feature_names():
    f.write(each+",")
    # print(each+",", end="")
f.write("\n")
# print("\n")
print("Writing tfidf to csv.")
i = 0
for row in x.toarray():
    for element in row:
        f.write(str(element)+",")
        # print(str(element)+",", end="")
    f.write("\n")
    # print("\n")

    if i % 100 == 0:
        print(i)
    i += 1
f.close()
print("closed")
stop = timeit.default_timer()
print(stop-start)



