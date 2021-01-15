# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:45:23 2021

@author: sofie
"""

import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import pandas as pd
from tkinter import filedialog, messagebox, ttk

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
Analyse_TFIDF.grid(row=6, column=16, columnspan=2,sticky='nesw', padx=5, pady=5, ipady=60, ipadx=0)

SerieFrame=tk.Frame(root,bg="gray17")
Serie_Temporelle = ttk.Button(rightFrame, text="Evolution au cours du temps", width=20, style="style1.TButton",command=Serie_Temporelle)
Serie_Temporelle.grid(row=7, column=16,columnspan=2, sticky='nesw', padx=10, pady=5, ipady=60, ipadx=10)
label_c=tk.Label(SerieFrame, text="Serie temporelle", foreground='cyan', bg="gray17", font=font1)
label_c.grid(row=0, column=5,pady=5, ipady=10, ipadx=10, padx=300)
retour=ttk.Button(SerieFrame,text="Retour menu",width=20, command=Retour_menu)
retour.grid(row=10, column=6,pady=5, ipady=10, ipadx=10) 

#boutons invisibles pour centrer 
droit = tk.Button(rightFrame, width=20, state= tk.DISABLED,bg="gray17",relief="flat")
droit.grid(row = 6, column=0, rowspan=3, columnspan = 14 ,sticky='nesw',padx=5, pady=5, ipady=60, ipadx=10)

gauche = tk.Button(rightFrame, width=20, state= tk.DISABLED,bg="gray17",relief="flat")
gauche.grid(row = 6, column=18, rowspan=3, columnspan = 15 ,sticky='nesw',padx=5, pady=5, ipady=60, ipadx=10)

#Affichage TF-IDF et BM25
tree=ttk.Treeview(frame)


def file_open():
    filename=filedialog.askopenfilename(
        initialdir="C:/",
        title="Ouvrir Fichier",
        filetype=(('CSV Files','*.csv'),('All Files','*,*')))
    if filename:
        try:
            filename=r"{}".format(filename)
            df=pd.read_csv(filename)
        except ValueError:
            my_label.config(text="File error")
        clear_tree()
        
        def clear_tree():
            tree.delete(*tree.getchildren())
        
        tree["column"]=list(df.columns)
        tree["show"]="headings"
        
        for column in tree["column"]:
            tree.heading(column,text=column)
            
            df_rows=df.to_numpy().toliste()
            for row in df_rows:
                tree.insert("","end",values=row)
                
        tree.pack()
frame=Frame(root)
frame.pack(pady=20)
Menu=Menu(analyseFrame)
root.config(menu=Menu)

file_menu=Menu(Menu, tearoff=False)
Menu.add_cascade(label="CSV file",menu=file_menu)
file_menu.add_command(label="Open",command=file_open)

root.mainloop()
