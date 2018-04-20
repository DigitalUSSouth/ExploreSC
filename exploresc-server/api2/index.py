import numpy as np
import math
from nlputils import tokenize_text
from itertools import repeat
import numpy as np
import json
from tqdm import tqdm
from pprint import pprint
terms_list = {}
num_docs = 0

def build_index(corpus):
  doc_vectors = []
  pbar = tqdm(total=len(corpus)*2)
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
    pbar.update(1)
  num_docs = len(corpus)
  num_terms = len(terms_list)
  tfidf_array = np.zeros([num_docs,num_terms],dtype=np.float32)
  counter = 0
  for doc in doc_vectors:
    for term,tf in doc[0].items():
      idf = get_idf(term)
      #doc_tfidf = np.zeros([num_terms],dtype=np.float32)
      #doc_tfidf[counter,terms_list[term][1]] = tf*idf
      tfidf_array[counter,terms_list[term][1]] = tf*idf
    counter += 1
    pbar.update(1)
  pbar.close()
  pprint(len(tfidf_array[0]))
  return tfidf_array

def add_doc_to_index(doc):
  tokens,doc_len = tokenize_text(doc)
  for term in tokens.keys():
    if term in terms_list:
      continue
    else:
      terms_list.append(term)
  doc_vector = dict(zip(tokens,list(map(get_tf,tokens,repeat(doc_len)))))

def get_idf(term):
  if not term in terms_list:
    return 0
  return math.log(float(1 + num_docs) / 
    (1 + terms_list[term][0]))

def get_norm_tf(term_freq,doc_len):
  return term_freq/doc_len

def main():
  with open("sceposts.json","r") as postsfile:
    posts = json.loads(postsfile.read())
  corpus = {}
  counter = 0
  for category,cat_items in posts.items():
    #if not category=='document':
    #  continue
    for item in cat_items:
      corpus[counter] = item['text']
      counter += 1
      #print(item)
      #break
  index = build_index(corpus)
  print (type(index))
  np.savez_compressed("index.npz",index)

if __name__ == "__main__":
  main()