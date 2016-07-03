from transpiler import *
import nltk

fol = input("Enter FOL>> ")
satisfiers = kb_fol_query(fol)
if not satisfiers:
	satisfiers = ['Nothing found']
print("APP1>> " + ', '.join(satisfiers))