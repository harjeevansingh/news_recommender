import numpy as np
import pandas as pd
import spacy
import en_core_web_sm
from spacy.tokenizer import Tokenizer


# Tokenizer
def tokenize(text):
    tokens = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for t in doc:
        tokens.append(t.text)

    return doc, tokens


# Lemmatizer
def lemmatize(text):
    lemms = []
    doc, _ = tokenize(text)
    for t in doc:
        lemms.append(t.lemma_)
    return lemms


# Remove stop words
def remove_stopwords(words):
    no_stop = []
    for word in words:
        if word not in nlp.Defaults.stop_words:
            no_stop.append(word)
            print(word)
    return no_stop


# creating vocab for the articles
def get_vocab(corpus):
    lemm_words = set([])
    for s in art:
        lemms = lemmatize(s)  # getting lemmatized words
    for lemm in lemms:
      lemm_words.add(lemm)       # avoiding repitition of words
    lemm_words = lemm_words
    lemm_words = list(lemm_words)  # converting to list

    vocab = remove_stopwords(lemm_words)

    return vocab


nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("NEWS sample.csv")
df = df[:20]                               # to reduce the size

df.drop(["Unnamed: 5"], axis=1, inplace=True)

art = df['Summary']

vocab = get_vocab(art)
print(vocab)