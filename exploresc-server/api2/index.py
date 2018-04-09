import numpy as np


terms_list = []
num_docs = 0



def get_idf(term):
    if not term in terms_list:
      return 0

    return math.log(float(1 + total_num_docs) / 
      (1 + num_docs[term]))