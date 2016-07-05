import nltk

POS_MAP = {
  "NNP" : "PropN",
  "JJ" : "Adj",
  "NN" : "Noun",
  "NNS" : "Noun",
  "VB" : "Verb",
  "VBD" : "Verb",
  "VBG" : "Verb",
  "VBN" : "Verb",
  "VBP" : "Verb",
  "VBZ" : "Verb",
  "IN" : "P",
  "RP" : "P",
  "CD" : "PropN"
}

GRAMMAR_FILE = "data/grammar.fcfg"
KB_FILE = "data/kb.txt"
CONST_FILE = "data/consts.txt"

def file_to_list(file):
  list_str = []
  with open(file) as f:
    list_str = f.read().splitlines()
  return list_str

CONST_ELEMS = file_to_list(CONST_FILE)

def is_plural(word):
  return word[-1] == 's'

def generate_rule_propn(word):
  CONST_ELEMS.append(word)
  append_to_file(word, CONST_FILE)
  return r"PropN[-LOC,NUM=sg,SEM=<\P.P(" + word + r")>] -> '" + word + r"'"

def generate_rule_adj(word):
  return r"Adj[SEM=<\x." + word + r"(x)>] -> '" + word + r"'"

def generate_rule_noun(word):
  if is_plural(word):
    return r"N[NUM=pl,SEM=<\x." + word[0:-1] + r"(x)>] -> '" + word + r"'"
  else:
    return r"N[NUM=sg,SEM=<\x." + word + r"(x)>] -> '" + word + r"'"

def generate_preposition(word):
  return r"P[SEM=<\X P x.X(\y.(P(x) & " + word + r"(x,y)))>] -> '" + word + r"'"

def generate_trans_verb(word):
  # In verb, if last letter is s, then singular
  # Note: this is the opposite in nouns
  if word[-1] == 's':
    return r"TV[NUM=sg,SEM=<\X y.X(\x." + word[0:-1] + r"(y,x))>,tns=pres] -> '" + word + r"'"
  else:
    return r"TV[NUM=pl,SEM=<\X y.X(\x." + word + r"(y,x))>,tns=pres] -> '" + word + r"'"

def generate_intra_verb(word):
  # In verb, if last letter is s, then singular
  # Note: this is the opposite in nouns
  if word[-1] == 's':
    return r"IV[NUM=sg,SEM=<\x." + word[0:-1] + r"(x)>,tns=pres] -> '" + word + r"'"
  else:
    return r"IV[NUM=sg,SEM=<\x." + word + r"(x)>,tns=pres] -> '" + word + r"'"

def is_noun(word_tag):
  return word_tag['tag'][0] == 'N'

def is_determiner(word_tag):
  return word_tag['tag'] == 'DT'

def is_transitive_verb(word, pos, words):
  index = words.index({'word': word, 'tag': pos})
  try:
    next_word = words[index+1]
    if is_noun(next_word) or is_determiner(next_word) or next_word['tag'] == 'TO':
      return True
  except IndexError:
    return False
  return False

def generate_rule(word, pos, words):
  if POS_MAP[pos] == "PropN":
    return generate_rule_propn(word)
  elif POS_MAP[pos] == "Adj":
    return generate_rule_adj(word)
  elif POS_MAP[pos] == "Noun":
    return generate_rule_noun(word)
  elif POS_MAP[pos] == "P":
    return generate_preposition(word)
  elif POS_MAP[pos] == "Verb":
    if is_transitive_verb(word, pos, words):
      return generate_trans_verb(word)
    else:
      return generate_intra_verb(word)

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

def is_unbound_expr(fol_str):
  read_expr = nltk.sem.Expression.fromstring
  expr = read_expr(fol_str)
  return expr.free()

def abstract_over(str):
  return r"\x. (" + str + r")"

def apply_con_to_abs(abstr, const):
  read_expr = nltk.sem.Expression.fromstring
  expr_str = abstr + "(" + const + ")"
  expr = read_expr(expr_str)
  return expr.simplify()

def make_model(fol_list):
  read_expr = nltk.sem.Expression.fromstring
  fol_exprs = list(map(read_expr, fol_list))
  return fol_exprs

def model_consistent(model, expr):
  prover = nltk.Prover9()
  return prover.prove(expr, model)

def begins_with_quantifier(fol_str):
  first_word = fol_str.split()[0]
  return (first_word == "exists" or first_word == "all")

def is_consistent_with(fol_list, fol_str):
  model = make_model(fol_list)

  if is_unbound_expr(fol_str):
    abs_fol = abstract_over(fol_str)
  else:
    abs_fol = fol_str
  
  if begins_with_quantifier(fol_str):
    expr = nltk.sem.Expression.fromstring(fol_str)
    return [str(model_consistent(model, expr))]
  
  satisfiers = []
  for const in CONST_ELEMS:
    expr = apply_con_to_abs(abs_fol, const)
    if (model_consistent(model, expr)):
      satisfiers.append(const)
  
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
    if word_tag['word'][0].isupper() and word_tag['tag'] != 'NNP':
      word_tag['tag'] = 'NNP'
    if not exists_in_file(word_tag['word'], GRAMMAR_FILE):
      new_rule = generate_rule(word_tag['word'], word_tag['tag'], word_tags)
      append_to_file(new_rule, GRAMMAR_FILE)

def parse_text(text):
  parser = nltk.load_parser(GRAMMAR_FILE, trace=0)
  tokens = nltk.word_tokenize(text)
  for tree in parser.parse(tokens):
    return str(tree.label()['SEM'])

def remove_extra_chars(str):
  return str.replace("?", "")

def nl_to_fol(nl):
  nl = remove_extra_chars(nl)
  prepare_grammar(nl)
  try:
    parsed = parse_text(nl)
    return parsed
  except ValueError:
    return False

def kb_add(text):
  fol_text = nl_to_fol(text)
  if fol_text:
    append_to_file(fol_text, KB_FILE)
  else:
    return False

def kb_query(text):
  fol_str = nl_to_fol(text)
  kb_fol_query(fol_str)

def kb_fol_query(fol_str):
  fol_list = file_to_list(KB_FILE)
  return is_consistent_with(fol_list, fol_str)


# fol = nl_to_fol(input("Enter natural lang>> "))
# print("FOL>> " + fol)