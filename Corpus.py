
################################## Déclaration des classes ##################################

import datetime as dt
import pickle
import Document
import re
import pandas
import Author as au


class Corpus():
    
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
            
    def add_doc(self, doc):
        
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
            
    def add_aut(self, aut_name,doc):
        
        aut_temp = au.Author(aut_name)
        aut_temp.add(doc)
        
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        
        self.naut += 1

    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]

    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
        
    def search(self, mot):
        chaine=" ".join(self.collection)
        masque="^\w{6}"+chaine+"\w{5}$"
        f=re.findall(masque,chaine)
        print(f)
        
    def concorde(self, n):
        df=pandas.dataFrame()
        chaine=" ".join(self.collection)
        masque="^\w{n}"+chaine+"\w{n}$"
        f=re.findall(masque,chaine)
        df.append(f)
        
    def vocab(self):
        caract=[",",".","(",")",":",";","?","!","[","]","{","}","/" ,"|"]
        vocabulaire=set()
        for x in range(self.ndoc) :
            docu=self.get_doc(x)
            text= docu.get_text()
            words=text.replace(".","").split()
            for w in range(len(words)):
                words[w]=words[w].lower()
                for c in caract:
                    words[w]=words[w].replace(c,"")
                if "https" and "http" not in words[w]:
                    vocabulaire.add(words[w])
        return vocabulaire

        
        
        
        
        
        
        
        