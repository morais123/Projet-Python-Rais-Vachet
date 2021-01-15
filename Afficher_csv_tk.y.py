# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:55:04 2021

@author: sofie
"""


from tkinter import *
import pandas as pd
from tkinter import ttk,filedialog
import numpy

#elaboration de la fenetre principale
root=Tk()
root.title("Affichage des CSV ")
root.geometry("700x500")
frame=Frame(root)
frame.pack(pady=20)

def open_new_frame():
    new_frame=Toplevel(root)
    new_frame.geometry("700x500")
    new_frame.title('Affichage comparatif')
    
    Menu2=Menu(new_frame)
    new_frame.config(menu=Menu2)
    file_menu2=Menu(Menu2, tearoff=False)
    Menu1.add_cascade(label="CSV file 2",menu=file_menu2)
    file_menu2.add_command(label="Open",command=file_open)
    lbl=Label(new_frame,text="Cette fenetre vous permet de comparer les scores tf-idf ou BM des 2 corpus")
    btn2=Button(new_frame,text="Retour Menu", command=lambda: new_frame.destroy())
    btn2.pack()
#mise en place du menu 
Menu1=Menu(root)
root.config(menu=Menu1)

btn=Button(root,text="Comparer avec l'autre corpus",command=open_new_frame)
btn.pack(padx=20,pady=20 )
#configuration de l'emplacement d'affichage en mode Treeview
tree=ttk.Treeview(frame)


#fonction permettant d'ouvrir un fichier sous format CSV et de l'afficher sur l'emplacement indiqué
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
            label.config(text="File error")
    #on enleve l'affichage a chaque chargement de nouveau fichier 
    clear_tree()
  
    tree["column"]=list(df.columns)
    tree["show"]="headings"          
    for column in tree["column"]:
        tree.heading(column,text=column)
    #on deroule le dataframe a l'aide de numpy pour pouvoir l'afficher
        df_rows=df.to_numpy().tolist()
    for row in df_rows:   
       tree.insert("","end",values=row)
    tree.pack()   
    #fonction permettant d'enelever les affichage precedents
def clear_tree():
   tree.delete(*tree.get_children())
            
  

file_menu=Menu(Menu1, tearoff=False)
Menu1.add_cascade(label="CSV file",menu=file_menu)
file_menu.add_command(label="Open",command=file_open)


label=Label(root,text='')
label.pack(pady=20)

#mise en place du menu pour la 2eme fenetre 



root.mainloop()
