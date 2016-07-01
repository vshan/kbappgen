from transpiler import *
import nltk

fol = input("Enter FOL>> ")
satisfiers = kb_fol_query(fol)
print("APP1>> " + ', '.join(satisfiers))