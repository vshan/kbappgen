import nltk

POS_MAP = {
  "NNP" : "PropN",
  "JJ" : "Adj"
}

GRAMMAR_FILE = "data/grammar.fcfg"
KB_FILE = "data/kb.txt"

def generate_rule_propn(word):
  return r"PropN[-LOC,NUM=sg,SEM=<\P.P(" + word + r")>] -> '" + word + r"'"

def generate_rule_adj(word):
  return r"Adj[SEM=<\x." + word + r"(x)>] -> '" + word + r"'"

def is_plural(word):
  word[-1] == 's'

def generate_rule_noun(word):
  if is_plural(word):
    return r"N[NUM=pl,SEM=<\x." + word + r"(x)>] -> '" + word + r"'"
  else:
    return r"N[NUM=sg,SEM=<\x." + word + r"(x)>] -> '" + word + r"'"

def generate_rule(word, pos):
  if POS_MAP[pos] == "PropN":
    return generate_rule_propn(word)
  elif POS_MAP[pos] == "Adj":
    return generate_rule_adj(word)

def get_pos_tags(sentence):
  tokens = nltk.word_tokenize(sentence)
  pos_tags = nltk.pos_tag(tokens)
  return [{'word': x, 'tag': y} for (x,y) in pos_tags]

def get_key_from_val(dict, val):
  for (k, v) in dict.items():
    if v == val:
      return k

def build_model_from_fols(fol_list):
  read_expr = nltk.sem.Expression.fromstring
  mc = nltk.MaceCommand(None, assumptions=list(map(read_expr, fol_list)))
  mc.build_model()
  return mc

def fol_satisfying_model(fol_string, mc):
  read_expr = nltk.sem.Expression.fromstring
  val = mc.valuation
  dom = val.domain
  model = nltk.Model(dom, val)
  g = nltk.Assignment(dom, [])
  sats = model.satisfiers(read_expr(fol_string), 'x', g)
  return [get_key_from_val(dict(val), elem) for elem in sats]

def abstract_over(str):
  return r"\x. (" + str + r")"

def apply_con_to_abs(abstr, const):
  read_expr = nltk.sem.Expression.fromstring
  expr_str = abstr + "(" + const + ")"
  expr = read_expr(expr_str)
  return expr.simplify()

def model_consistent(fol_list, expr):
  read_expr = nltk.sem.Expression.fromstring
  fol_exprs = list(map(read_expr, fol_list))
  prover = nltk.Prover9()
  return prover.prove(expr, fol_exprs)

def is_consistent_with(fol_list, fol_str):
  abs_fol = abstract_over(fol_str)
  satisfiers = []
  for const in CONST_ELEMS:
    expr = apply_con_to_abs(abs_fol, const)
    if (model_consistent(fol_list, expr)):
      satisfiers.push(const)
  return satisfiers

def append_to_file(line, file):
  with open(file, "a") as append_file:
    append_file.write(line + "\n")
    append_file.flush()

def exists_in_file(word, file):
  l_word = word.lower()
  return (l_word in open(file).read() or word in open(file).read())

def prepare_grammar(text):
  word_tags = get_pos_tags(text)
  for word_tag in word_tags:
    if not exists_in_file(word_tag['word'], GRAMMAR_FILE):
      new_rule = generate_rule(word_tag['word'], word_tag['tag'])
      append_to_file(new_rule, GRAMMAR_FILE)

def parse_text(text):
  parser = nltk.load_parser(GRAMMAR_FILE, trace=0)
  tokens = nltk.word_tokenize(text)
  for tree in parser.parse(tokens):
    return str(tree.label()['SEM'])

def nl_to_fol(nl):
  prepare_grammar(nl)
  return parse_text(nl)

def add_to_kb(text):
  fol_text = nl_to_fol(text)
  append_to_file(fol_text, KB_FILE)

# fol = nl_to_fol(input("Enter natural lang>> "))
# print("FOL>> " + fol)