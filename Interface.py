# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:45:23 2021

@author: sofie
"""

import datetime as dt


import urllib.request
import xmltodict   

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

import re

#Elements graphiques:
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

btnState = False
navbarWidth = 170
WIDTH = 1300
HEIGHT = 800
root = tk.Tk()

#parametrage du menu principal
root.title("Text mining")
root.geometry('1150x710')
root.configure(bg="gray17")
root.resizable(True, True)
root.minsize(1140,700)

#ce frame représente la page principale
rightFrame = tk.Frame(root, bg='gray17')
rightFrame.grid(row=15, column=5)


#police de caractère
font1 = tkFont.Font(family="Calibri",size="30",weight="bold")
font2 = tkFont.Font(family="Arial",size="15",weight="bold")

def Analyse_TFIDF():
    analyseFrame.grid(row=1,column=1)
    rightFrame.grid_forget()
    SerieFrame.grid_forget()
   
    
def Serie_Temporelle():
    SerieFrame.grid(row=1,column=1)
    rightFrame.grid_forget()
    analyseFrame.grid_forget()
    
    
def Retour_menu():
    rightFrame.grid(row=15, column=5)
    analyseFrame.grid_forget()
    SerieFrame.grid_forget()
   
analyseFrame=tk.Frame(root,bg="gray17")
label_a=tk.Label(analyseFrame, text="Analyse TF-IDF", foreground='cyan', bg="gray17", font=font1)
label_a.grid(row=0, column=5,pady=5, ipady=10, ipadx=10, padx=300)
retour=ttk.Button(analyseFrame,text="Retour menu",width=20, command=Retour_menu)
retour.grid(row=10, column=6,pady=5, ipady=10, ipadx=10) 
   
Analyse_TFIDF = ttk.Button(rightFrame, text="Anlyse textuelle", width=20, style="style1.TButton",command=Analyse_TFIDF)
Analyse_TFIDF.grid(row=3, column=2, columnspan=2,sticky='nesw', padx=50, pady=50, ipady=50, ipadx=50)

def recup_mot():
    mot=txt_Temp.get()
    data=pd.read_csv('Donnees.csv')
    data.columns=['mot','freq','mois']
    affich_T(data,mot)

def affich_T(data,mot):
            #Figure contenant la courbe
            f = Figure(figsize=(10,6), dpi=80)
            canvas = FigureCanvasTkAgg(f,SerieFrame)
            liste=[0,0,0,0,0,0,0,0,0,0,0,0]
            if (mot!=''):
                l=len(data)
                for i in range(l):
                    if (mot == data.loc[data.index[i],'mot']):
                        print("mot trouvé")
                        
                        if (str(data.loc[data.index[i],'mois'])=="janvier"):
                            liste[0]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="février"):
                            liste[1]=(data.loc[data.index[i],'freq'])*100                               
                        if (str(data.loc[data.index[i],'mois'])=="mars"):
                            liste[2]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="avril"):
                            liste[3]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="mai"):
                            liste[4]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="juin"):
                            liste[5]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="juillet"):
                            liste[6]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="août"):
                            liste[7]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="septembre"):
                            liste[8]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="octobre"):
                            liste[9]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="novembre"):
                            liste[10]=(data.loc[data.index[i],'freq'])*100
                        if (str(data.loc[data.index[i],'mois'])=="décembre"):
                            liste[11]=(data.loc[data.index[i],'freq'])*100

                canvas.get_tk_widget().grid(row=5, column=1)#side=tk.BOTTOM, fill=tk.BOTH, expand=1
                a = f.add_subplot(111)
                a.plot(["janv","fev","mars","avril","mai","juin","juillet","aout","sept","oct","nov","dec"],liste)


SerieFrame=tk.Frame(root,bg="gray17")
txt_Temp=tk.Entry(SerieFrame)
txt_Temp.grid(row=2, column=1,columnspan=1, sticky='nesw', padx=10, pady=5, ipady=10, ipadx=10)
bout_Temp=tk.Button(SerieFrame,text="valider ce mot" , command=lambda:[recup_mot()])
bout_Temp.grid(row=2, column=2,columnspan=1, sticky='nesw', padx=10, pady=5, ipady=10, ipadx=10)


Serie_Temporelle = ttk.Button(rightFrame, text="Evolution fréquence mot", width=20, style="style1.TButton",command=Serie_Temporelle)
Serie_Temporelle.grid(row=2, column=2,columnspan=2, sticky='nesw', padx=50, pady=50, ipady=50, ipadx=50)

label_c=tk.Label(SerieFrame, text="Serie temporelle", foreground='cyan', bg="gray17", font=font1)
label_c.grid(row=0, column=1, columnspan=2, sticky='nesw', pady=5, ipady=10, ipadx=10, padx=30)
retour=ttk.Button(SerieFrame,text="Retour menu",width=20, command=Retour_menu)
retour.grid(row=10, column=4,pady=5, ipady=10, ipadx=10) 

#boutons invisibles pour centrer 
haut = tk.Button(rightFrame, width=20, state= tk.DISABLED,bg="gray17",relief="flat")
haut.grid(row = 0, column=0, columnspan = 3 ,sticky='nesw',padx=5, pady=20, ipady=30, ipadx=10)

gauche = tk.Button(rightFrame, width=20, state= tk.DISABLED,bg="gray17",relief="flat")
gauche.grid(row = 2, column=1, rowspan=3, columnspan = 1 ,sticky='nesw',padx=80, pady=30, ipady=30, ipadx=40)


root.mainloop()
