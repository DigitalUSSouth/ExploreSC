import numpy as np
import math
from nlputils import tokenize_text
from itertools import repeat
import numpy as np
from scipy import spatial
import json
from tqdm import tqdm
from pprint import pprint
from operator import itemgetter
import time
num_docs = 0

def build_index(corpus):
  terms_list = {}
  start_time = time.time()
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
      idf = get_idf(term,terms_list)
      #doc_tfidf = np.zeros([num_terms],dtype=np.float32)
      #doc_tfidf[counter,terms_list[term][1]] = tf*idf
      tfidf_array[counter,terms_list[term][1]] = tf*idf
    counter += 1
    pbar.update(1)
  pbar.close()
  pprint(len(tfidf_array[0]))
  print("Time:",time.time()-start_time,"s")
  return tfidf_array,terms_list

"""def add_doc_to_index(doc):
  tokens,doc_len = tokenize_text(doc)
  for term in tokens.keys():
    if term in terms_list:
      continue
    else:
      terms_list.append(term)
  doc_vector = dict(zip(tokens,list(map(get_tf,tokens,repeat(doc_len)))))"""

def get_idf(term,terms_list):
  if not term in terms_list:
    return 0
  return math.log(float(1 + num_docs) / 
    (1 + terms_list[term][0]))

def get_norm_tf(term_freq,doc_len):
  return term_freq/doc_len

def cosine_similarity(a,b):
  return 1 - spatial.distance.cosine(a, b)

def get_query_tfidf(query_text,terms_list):
  doc_tfidf = {}
  tokens,doc_len = tokenize_text(query_text)
  for token,freq in tokens.items():
    if token in terms_list:
      term_index = terms_list[token][1] #previously defined token
      tf = get_norm_tf(freq,doc_len)
      idf = get_idf(token,terms_list)
      doc_tfidf[token] = tf*idf
  doc_vector = np.zeros([len(terms_list)],dtype=np.float32)
  for term,tfidf in doc_tfidf.items():
    term_index = terms_list[term]
    doc_vector[term_index] = tfidf
  return doc_vector

def get_rankings(index,terms_list,query):
  rankings = []
  query_vector = get_query_tfidf(query,terms_list)
  for i in range(index.shape[0]):
    vector = index[i]
    cos_sim = cosine_similarity(query_vector,vector)
    doc_sim = [i,cos_sim]
    rankings.append(doc_sim)
  rankings.sort(key=itemgetter(1),reverse=True)
  return rankings

def search(query,index,terms_list,doc_keys):
  rankings = get_rankings(index,terms_list,query)
  results = []
  for key,val in rankings:
    results.append(doc_keys[key])
  return results

def load_index():
  saved_index = np.load("index.npz")
  index = saved_index['arr_0']
  terms_list = saved_index['arr_1'].item()
  doc_keys = saved_index['arr_2'].item()
  return index,terms_list,doc_keys

def main():
  with open("sceposts.json","r") as postsfile:
    posts = json.loads(postsfile.read())
  corpus = {}
  counter = 0
  doc_keys = {}
  for category,cat_items in posts.items():
    #if not category=='document':
    #  continue
    for item in cat_items:
      corpus[counter] = item['text']
      doc_keys[counter] = {'excerpt':item['content'][:150],'url':item['url'],'title':item['title']}
      counter += 1
      #print(item)
      #break
  index,terms_list = build_index(corpus)
  print (type(index))
  np.savez_compressed("index.npz",index,terms_list,doc_keys)

if __name__ == "__main__":
  main()