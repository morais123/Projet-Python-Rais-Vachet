# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 08:47:10 2020

@author: Marie
"""

import Corpus as cp
import Document as dc
import datetime as dt
import Author as au
import pickle
import numpy as np

from gensim import corpora
from gensim.summarization import bm25

import praw

import urllib.request
import xmltodict   

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords.words('english')
import pandas as pd
import nltk


################################## Création du Corpus ##################################

corpusArxiv = cp.Corpus("Corona")
corpusReddit = cp.Corpus("Corona")

reddit = praw.Reddit(client_id='psCF_Nxnbm2M3g', client_secret='5-GUEVBV4VU7WsirQyxBoyQIdNw', user_agent='rais')
hot_posts = reddit.subreddit('Coronavirus').hot(limit=450)
for post in hot_posts:
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = dc.RedditDocument(datet,
                   post.title,
                   post.author_fullname,
                   txt,
                   post.url,"",5) #Attention ici calculer le nombre de commentaires
    corpusReddit.add_doc(doc)


url = 'http://export.arxiv.org/api/query?search_query=all:coronavirus&start=0&max_results=450'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

for i in docs:
    datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
    try:
        author = [aut['name'] for aut in i['author']][0]
    except:
        author = i['author']['name']
    txt = i['title']+ ". " + i['summary']
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = dc.Document(datet,
                   i['title'],
                   author,
                   txt,
                   i['id'],
                   ""
                   )
    corpusArxiv.add_doc(doc)


print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))


print("Corpus trié par titre (4 premiers)")
res = corpus.sort_title(4)
print(res)
    
print()

print("Corpus trié par date (4 premiers)")
res = corpus.sort_date(4)
print(res)

print(corpus)

print("Enregistrement du corpus sur le disque...")   
corpus.save("Corona.crp")  

for x in range(500):
    print(corpusReddit.get_doc(x).get_date())
    
New2=dc.ArxivDocument(45,"fff","fdsfs","fsdfdsfdsfs","url","rrr","coAut")
print(New2.co_aut)
Ncorpus=cp.Corpus("test")
Ncorpus.add_doc(New2)
res1 = Ncorpus.sort_title(4)
res1



vocReddit=corpusReddit.vocab()

vocArxiv=corpusArxiv.vocab()

from nltk.tokenize import word_tokenize
stop_words=set(stopwords.words("english"))
words=word_tokenize(vocReddit)
def stopwords(Corpus):
    for words in Corpus:
        if words not in stopwords.words('english'):
            return Corpus    
stopwords(vocReddit)  
vocReddit.stopwords() 
vocArxiv.stopwords()
#count the words Reddit 

uniqueWords = vocReddit.union(vocArxiv)
number_words_Reddit=dict.fromkeys(uniqueWords,0)
for word in vocReddit:
    number_words_Reddit[word]+=1
    
print(number_words_Reddit)

# Count words for Arxiv
number_words_Arxiv=dict.fromkeys(uniqueWords,0)
for word in vocArxiv:
    number_words_Arxiv[word]+=1
    
print(number_words_Arxiv)

# Preprocessing Data
np.char.lower(vocReddit)


#count the words


# enlever les stop_words
DocuReddit=list(vocReddit)
DocuArxiv=list(vocArxiv)
new_text=""
for word in words:
    if word not in stopwords:
        new_text = new_text + " " + word
            
def computeTF(wordDict, Vocab):
    tfDict = {}
    Count_words = len(Vocab)
    for word, count in wordDict.items():
        tfDict[word] = count / float(Count_words)
    return tfDict

tf_Reddit=computeTF(number_words_Reddit,vocReddit)
tf_Arxiv=computeTF(number_words_Arxiv,vocArxiv)



print(tf_Reddit)
print(tf_Arxiv)



def computeIDF(documents):
    import math
    N = len(documents)
    
    #On compte le nombre de documents contenant un mot 
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for w, val in document.items():
            if val > 0:
                idfDict[w] += 1
    #on applique la formule de la "idf" c'est a dire log(nombre de documents/nombre de mots contenus dans tout les documents)
    for w, val in idfDict.items():
        idfDict[w] = math.log(N / float(val))
    return idfDict


number_words_Reddit.keys()
idfs = computeIDF([number_words_Reddit,number_words_Arxiv])
idfs
#tfidf : term frequency from message then it divise it with how 
#many documents contain this word


def computeTFIDF(tfVocab,idfs):
    tfidf={}
    for w,val in tfVocab.items():
        tfidf[w]=val*idfs[w]
    return tfidf

tfidfVocReddit=computeTFIDF(tf_Reddit,idfs)
tfidfVocArxiv=computeTFIDF(tf_Arxiv,idfs)

Data_tfidf=pd.DataFrame([tfidfVocReddit,tfidfVocArxiv])
Data_tfidf    

Data_tfidf.to_csv('tf-idf.csv')

# methode OKAPI BM25 
from rank_bm25 import BM25Okapi
bm25 = BM25Okapi(vocReddit)
query="Coronavirus"
doc_scores_R=bm25.get_scores(query)
print(doc_scores_R)

bm25 = BM25Okapi(vocArxiv)
query="Coronavirus"
doc_scores_A=bm25.get_scores(query)
print(doc_scores_A)

BM_word=pd.DataFrame([doc_scores_R,doc_scores_A])
BM_word.to_csv('BMword.csv',index=False)

print(BM_word)


#AUTRE METHODE NLTK
vect=CountVectorizer()
DocuReddit
vocReddit

Documents=list([vocReddit,vocArxiv])
data_voc=pd.DataFrame([DocuReddit,DocuArxiv])
str_doc=" ".join(map(str,Documents))
docu_t=vect.transform(data_voc)

vectors = vect.fit_transform(data_voc)
feature_names = vect.get_feature_names()
print(feature_names)
dense = vectors.todense()
denselist = dense.tolist()
tfvectorizer = TfidfVectorizer(stop_words={'english'})
tranform=tfvectorizer.fit_transform(data_voc)
g
len(feature_names)
data=pd.DataFrame(tranform.toarray(),columns=tfvectorizer.get_feature_names())

data.describe()
data.value_counts()



