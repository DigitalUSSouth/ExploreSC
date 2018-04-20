import numpy as np
import math
import nlputils
from itertools import repeat
import numpy as np

terms_list = {}
num_docs = 0

def build_index(corpus):
  index = {}
  doc_vectors = []
  for key,item in corpus.items():
    doc_term_freqs = {}
    tokens,doc_len = tokenize_text(item)
    for token,freq in tokens.items():
      if token in terms_list:
        terms_list[token][0] += 1
        term_index = terms_list[token][1] #previously defined token
      else:
        term_index = len(terms_list) #index for new term
        terms_list[token] = [1,term_index]
      doc_term_freqs[token] = get_norm_tf(freq,doc_len)
    doc_vectors.append((doc_term_freqs,key))
  num_docs = len(corpus)
  num_terms = len(terms_list)
  tfidf_array = {key:np.zeros([num_terms],dtype=np.float32]) for key in corpus.keys()}
  for doc in doc_vectors:
    for term,tf in doc[0].items():
      idf = get_idf(term)
      tfidf_array[doc[1]][term_index[term]] = tf*idf

  #for doc_vectors in doc_vectors:

    #doc_vector.append(add_doc_to_index(doc))

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
  return math.log(float(1 + num_docs) / 
    (1 + terms_list[term]))

def get_norm_tf(term_freq,doc_len):
  return term_freq/doc_len