#script to gather relevant marker data from from full markers

import json
from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import time
nltk.download('punkt')
nltk.download('stopwords')
start_time = time.time()
with open("raw-markers.json", "r") as datafile:
    full_markers = json.load(datafile)
    datafile.close()

def tokenize_marker(marker):
    text = marker["name"]+" "+marker["cmt"] +" " + marker["desc"]
    tokens = {}
    stop_words = list(stopwords.words('english'))
    stop_words.extend([
        '{',
        '}',
        '[',
        ']',
        '(',
        ')',
        ',',
        '.',
        '\'',
        '\'\'',
        '/',
        '<',
        '>',
        ';',
        'br',
        '#',
        '&',
        '/b',
        '/i'
        ])
    doc_len = 0
    for item in [w for w in word_tokenize(text) if not w in stop_words]:
        if item in tokens:
            tokens[item] += 1
        else:
            tokens[item] = 1
        doc_len += 1
    return tokens,doc_len

markers = []
for item in full_markers:
    marker = {
        "name":item["properties"]["name"],
        "cmt":item["properties"]["cmt"],
        "desc":item["properties"]["desc"],
        "geolocation": [item["geometry"]["coordinates"][1],item["geometry"]["coordinates"][0]],
        "category": None,
        "ref": None,
        "url": item["properties"]["link1_href"]
    }
    marker["tokens"],marker["doc_len"] = tokenize_marker(marker)
    markers.append(marker)

print(len(markers))
print("Exec time",time.time()-start_time,"s")
with open("markers.json","w") as outfile:
    json_markers = json.dumps(markers,outfile,ensure_ascii=False,indent=4, sort_keys=True)
    outfile.write(json_markers)
    outfile.close
