from transpiler import *
import nltk

fol = nl_to_fol(input("Enter natural lang>> "))
satisfiers = kb_fol_query(fol)
if not satisfiers:
	satisfiers = ['Nothing found']
print("APP1>> " + ', '.join(satisfiers))