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

import praw

import urllib.request
import xmltodict   

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import pandas as pd
import nltk

import re


################################## Création du Corpus ##################################

corpusReddit = cp.Corpus("Corona")

reddit = praw.Reddit(client_id='psCF_Nxnbm2M3g', client_secret='5-GUEVBV4VU7WsirQyxBoyQIdNw', user_agent='rais')
subreddit = reddit.subreddit('all')

for post in subreddit.top(limit=1000):
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = dc.RedditDocument(datet,
                   post.title,
                   post.author,
                   txt,
                   post.url,"",5) #Attention ici calculer le nombre de commentaires
    corpusReddit.add_doc(doc)


corpusReddit.ndoc


corpusArxiv = cp.Corpus("Corona")


url = url='http://export.arxiv.org/api/query?search_query=all&start=0&max_results=10000'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

url2 = 'http://export.arxiv.org/api/query?search_query=all&start=28817&max_results=8000'
data2 =  urllib.request.urlopen(url2).read().decode()
docs = xmltodict.parse(data2)['feed']['entry']

data2

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

corpusArxiv.ndoc

dates=list()
for x in range(corpusArxiv.ndoc):
    dates.append(str(corpusArxiv.get_doc(x).get_date()))

print(dates)

def vocab(liste):
        caract=[",",".","(",")",":",";","?","!","[","]","{","}","/" ,"|","<",">","$","\"","=","\\"]
        vocabulaire=set()
        for x in liste:
            docu=corpusArxiv.get_doc(x)
            text= docu.get_text()
            words=text.replace(".","").split()
            for w in range(len(words)):
                words[w]=words[w].lower()
                for c in caract:
                    words[w]=words[w].replace(c,"")
                if (re.search('[0-9]',words[w])):
                    re.sub('[0-9]', '', words[w])
                if "https" and "http" and "\\" not in words[w]:
                    vocabulaire.add(words[w])
        return vocabulaire

janvier=list()
fev=list()
mars=list()
avr=list()
mai=list()
juin=list()
juil=list()
aout=list()
sept=list()
octo=list()
nov=list()
dec=list()

for x in range(corpusArxiv.ndoc):
    if re.search("^2020-01", dates[x]):
       janvier.append(x)
    if re.search("^2020-02", dates[x]):
       fev.append(x)
    if re.search("^2020-03", dates[x]):
       mars.append(x)
    if re.search("^2020-04", dates[x]):
       avr.append(x)   
    if re.search("^2020-05", dates[x]):
       mai.append(x)
    if re.search("^2020-06", dates[x]):
       juin.append(x)
    if re.search("^2020-07", dates[x]):
       juil.append(x)
    if re.search("^2020-08", dates[x]):
       aout.append(x)
    if re.search("^2020-09", dates[x]):
       sept.append(x)
    if re.search("^2020-10", dates[x]):
       octo.append(x)
    if re.search("^2020-11", dates[x]):
       nov.append(x)
    if re.search("^2020-12", dates[x]):
       dec.append(x)
    
print(janvier)

janvier=vocab(janvier)
len(janvier)

fev=vocab(fev)
mars=vocab(mars)
avr=vocab(avr)
mai=vocab(mai)
juin=vocab(juin)
juil=vocab(juil)
aout=vocab(aout)
sept=vocab(sept)
octo=vocab(octo)
nov=vocab(nov)
dec=vocab(dec)


def count_words(ens):
    # Count words for janvier
    number_words=dict.fromkeys(ens,0)
    for word in ens:
        number_words[word]+=1
    return number_words

nb_janv=count_words(janvier)
nb_fev=count_words(fev)
nb_mars=count_words(mars)
nb_avr=count_words(avr)
nb_mai=count_words(mai)
nb_juin=count_words(juin)
nb_juil=count_words(juil)
nb_aout=count_words(aout)
nb_sept=count_words(sept)
nb_octo=count_words(octo)
nb_nov=count_words(nov)
nb_dec=count_words(dec)

           
def computeTF(wordDict, Vocab):
    tfDict = {}
    Count_words = len(Vocab)
    for word, count in wordDict.items():
        tfDict[word] = count / float(Count_words)
    return tfDict


tf_janv=computeTF(nb_janv,janvier)
tf_f=computeTF(nb_fev,fev)
tf_mars=computeTF(nb_mars,mars)
tf_avr=computeTF(nb_avr,avr)
tf_mai=computeTF(nb_mai,mai)
tf_juin=computeTF(nb_juin,juin)
tf_juil=computeTF(nb_juil,juil)
tf_aout=computeTF(nb_aout,aout)
tf_sept=computeTF(nb_sept,sept)
tf_oct=computeTF(nb_octo,octo)
tf_nov=computeTF(nb_nov,nov)
tf_dec=computeTF(nb_dec,dec)

import pandas as pd
Donnees=pd.Series(tf_janv).to_frame()
Donnees['mois']="janvier"

Data_f=pd.Series(tf_f).to_frame()
Data_f["mois"]="février"

Data_mars=pd.Series(tf_mars).to_frame()
Data_mars["mois"]="mars"

Data_avr=pd.Series(tf_avr).to_frame()
Data_avr["mois"]="avril"

Data_mai=pd.Series(tf_mai).to_frame()
Data_mai["mois"]="mai"

Data_juin=pd.Series(tf_juin).to_frame()
Data_juin["mois"]="juin"

Data_juil=pd.Series(tf_juil).to_frame()
Data_juil["mois"]="juillet"

Data_a=pd.Series(tf_aout).to_frame()
Data_a["mois"]="août"

Data_s=pd.Series(tf_sept).to_frame()
Data_s["mois"]="septembre"

Data_o=pd.Series(tf_oct).to_frame()
Data_o["mois"]="octobre"

Data_n=pd.Series(tf_nov).to_frame()
Data_n["mois"]="novembre"


Data_dec=pd.Series(tf_dec).to_frame()
Data_dec["mois"]="décembre"

Data=pd.concat([Donnees,Data_f,Data_mars,Data_avr,Data_mai,Data_juin,Data_juil,Data_a,Data_s,Data_o])
Data_Frame=pd.concat([Data,Data_n,Data_dec])

Data_Frame

corpusArxiv.ndoc

Data_Frame.to_csv('Donnees.csv')

data=pd.read_csv('Donnees.csv')

data.columns=['mot','freq','mois']

data

len(data)

for x in range(500):
    print(corpusReddit.get_doc(x).get_date())



vocReddit=corpusReddit.vocab()

vocArxiv=corpusArxiv.vocab()

from nltk.tokenize import word_tokenize
stop_words=set(stopwords.words("english"))
words=word_tokenize(vocReddit)
def stopwords(Corpus):
    for words in Corpus:
        if words not in stopwords.words('english'):
            return Corpus    
        
print(stopwords(vocReddit))    
stopwords.words("english")
print(stop_words)
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

len(feature_names)
data=pd.DataFrame(tranform.toarray(),columns=tfvectorizer.get_feature_names())

data.describe()
data.value_counts()
