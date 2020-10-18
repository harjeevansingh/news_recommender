
import numpy as np
import pandas as pd
import spacy
import en_core_web_sm
from spacy.tokenizer import Tokenizer
import timeit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


# Tokenizer
def tokenize(text):
    global counter
    tokens = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for t in doc:
        tokens.append(t.text)

    return doc, tokens


counter = 1


# Lemmatizer
def lemmatize(text):
    lemms = []
    doc, _ = tokenize(text)
    for t in doc:
        lemms.append(t.lemma_)
        # print(t.lemma_)
    global counter
    print("Article: "+str(counter))

    counter += 1
    return lemms


# Remove stop words
def remove_stopwords_and_puncs(words):
    no_stop = set([])
    puncs = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n'"
    for word in words:
        word = word.lower()
        if word not in nlp.Defaults.stop_words and word not in puncs and word.isalpha():
            if word[-1] in puncs:
              word = word[:-1]
            no_stop.add(word)
            #print(word)
    return no_stop


# Extract vocab for the articles
def get_vocab(corpus):
    lemm_words = set([])
    for s in corpus:
        lemms = lemmatize(s)  # getting lemmatized words
        for lemm in lemms:
            if lemm[-1] == "^":
                lemm = lemm[:-1]
            lemm_words.add(lemm)       # avoiding repitition of words by using set

    vocab = remove_stopwords_and_puncs(lemm_words)

    return vocab


# getting articles
nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("NEWS.csv")
df = df[:50]                               # to limit the size
df.drop(["Unnamed: 5"], axis=1, inplace=True)
art = df['Summary']

# getting vocab and saving as csv
vocab = get_vocab(art)
filename = "vocab_debug.csv"
f = open(filename, "w", encoding='utf-8')
print(vocab)
f.write("DocId,")
for each in vocab:
    f.write(each+",")
print("Opened file...")
f.close()
print("closed")
print(len(vocab))