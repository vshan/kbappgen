from transpiler import *
import nltk

fol = nl_to_fol(input("Enter natural lang>> "))
print("FOL>> " + fol)
append_to_file(fol, KB_FILE)