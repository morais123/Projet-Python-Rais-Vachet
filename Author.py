# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 08:19:29 2020

@author: Marie
"""

class Author():
    def __init__(self,name):
      self.name = name
      self.production = {}
      self.ndoc = 0

    def add(self, doc):
      self.production[self.ndoc] = doc
      self.ndoc += 1

    def __str__(self):
      return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)

    def __repr__(self):
      return self.name