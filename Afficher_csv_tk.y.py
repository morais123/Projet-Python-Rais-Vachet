# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:55:04 2021

@author: sofie
"""
from tkinter import *
import pandas as pd
from tkinter import ttk,filedialog
import numpy


root=Tk()
root.title("Affichage des CSV ")
root.geometry("700x500")
frame=Frame(root)
frame.pack(pady=20)
Menu1=Menu(root)
root.config(menu=Menu1)
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
            label.config(text="File error")
    clear_tree()
  
    tree["column"]=list(df.columns)
    tree["show"]="headings"          
    for column in tree["column"]:
        tree.heading(column,text=column)
                
        df_rows=df.head().to_numpy().tolist()
    for row in df_rows:   
       tree.insert("","end",values=row)
    tree.pack()      
def clear_tree():
   tree.delete(*tree.get_children())
            
  



file_menu=Menu(Menu1, tearoff=False)
Menu1.add_cascade(label="CSV file",menu=file_menu)
file_menu.add_command(label="Open",command=file_open)

label=Label(root,text='')
label.pack(pady=20)


root.mainloop()
