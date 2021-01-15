# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 08:18:12 2020
@author: Marie
"""

from gensim.summarization.summarizer import summarize

class Document():

    # constructeur
    def __init__(self, date, title, author, text, url, type_d):
      self.date = date
      self.title = title
      self.author = author
      self.text = text
      self.url = url
      self.type_d=""
   # accepteurs (getters)

    def get_author(self):
      return self.author

    def get_title(self):
      return self.title

    def get_date(self):
      return self.date

    def get_source(self):
      return self.source

    def get_text(self):
      return self.text
    def get_type(self):
      return self.type_d
   # autre fonctions

    def __str__(self):
      return "Document " + str(self.getType()) + " : " + self.title

    def __repr__(self):
      return self.title
  
    def getType(self):
        pass
       
    def sumup(self,ratio):
        try:
            auto_sum = summarize(self.text,ratio=ratio,split=True)
            out = " ".join(auto_sum)
        except:
            out =self.title            
        return out
  
    def nettoyer_texte(self,chaine):
        chaine=chaine.lower()
        chaine=chaine.replace("\n"," ")
        chaine=chaine.replace("[0-9].:;,!*","")
    
class RedditDocument(Document):    
    def __init__(self, date, title, author, text, url, type_d, n_com):
        self.n_com=n_com
        self.type_d = "Reddit"
        super().__init__(date, title, author, text, url, type_d)
        
    def get_Type(self):
        return self.type_d
    
    def get_n_com(self):
        return self.n_com
    
    def set_n_com(self,n_com):
        self.n_com=n_com

    def __str__(self):
        return "Doc Reddit "+ self.get_n_com

class ArxivDocument (Document):
    def __init__(self, date, title, author, text, url, type_d, co_aut):
        self.co_aut=co_aut
        super().__init__(date, title, author, text, type_d, url)
        self.type="Arxiv"
    
    def get_co_aut(self):
        return self.co_aut
    
    def set_n_com(self,co_aut):
        self.co_aut=co_aut

    def get_Type(self):
        return self.type_d
    
    
    
Arv= ArxivDocument(45,"fff","fdsfs","fsdfdsfdsfs","url","rrr","coAut")
print(Arv)