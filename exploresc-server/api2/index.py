import numpy as np
import math
import nlputils
from itertools import repeat

terms_list = []
num_docs = 0

def build_index(corpus):
  index = {}
  doc_vectors = []
  for item in corpus:
    doc_vectory.append(add_doc_to_index(doc))

def add_doc_to_index(doc):
  tokens,doc_len = tokenize_text(doc)
  for term in tokens.keys():
    if term in terms_list:
      continue
    else:
      terms_list.append(term)
  #tokens_tf = {list(map(get_tf,tokens,repeat(doc_len)))}
  #create a dict => {term:term_frequency}
  doc_vector = dict(zip(tokens,list(map(get_tf,tokens,repeat(doc_len)))))

def get_idf(term):
  if not term in terms_list:
    return 0
  return math.log(float(1 + total_num_docs) / 
    (1 + num_docs[term]))

def get_tf(term,doc_len):
  return doc_terms[term]/reduce