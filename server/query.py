import nltk

def process(text):
	sents = [text]
	grammar_file = 'grammars/book_grammars/simple-sem.fcfg'
	for results in nltk.interpret_sents(sents, grammar_file):
		for (synrep, semrep) in results:
			print(synrep)

while True:
	query_raw = input("APP1>> ")
	process(query_raw)