#script to gather relevant marker data from from full markers

import json
from pprint import pprint
import time
#from nlputils import tokenize_text
import sqlite3
start_time = time.time()
with open("raw-markers.json", "r") as datafile:
    full_markers = json.load(datafile)
    datafile.close()



markers = {}
for item in full_markers:
    marker = {
        "name":item["properties"]["name"],
        "cmt":item["properties"]["cmt"],
        "desc":item["properties"]["desc"],
        "geolocation": [item["geometry"]["coordinates"][1],item["geometry"]["coordinates"][0]],
        "category": None,
        "re": None,
        "url": item["properties"]["link1_href"]
    }
    #text = marker["name"]+" "+marker["cmt"] +" " + marker["desc"]
    #marker["tokens"],marker["doc_len"] = tokenize_text(text)
    markers[marker['url']] = marker

with open("data/sample-data.json", "r") as datafile:
    sample_markers = json.load(datafile)
    datafile.close()
for item in sample_markers:
    if 'Category' in item['properties']:
        category = item['properties']['Category']
        markers[item["properties"]["link1_href"]]['category'] = category
    if 'rel' in item['properties']:
        rel = item['properties']['rel']
        markers[item["properties"]["link1_href"]]['rel'] = rel

with sqlite3.connect('data/database.db') as connection:
    cursor = connection.cursor()
    for key,item in markers.items():
        if item['category'] is None:
            continue
        if item['rel'] is None:
            continue
        for rel in item['rel']:
            if rel=="":
                continue
            cursor.execute("INSERT INTO related_objects (object_id,related_item) VALUES (?,?)",(key,rel))
        for cat in item['category']:
            if cat is None:
                continue
            cursor.execute("INSERT INTO categories (object_id,category) VALUES (?,?)",(key,cat))

print(len(markers))
print("Exec time",time.time()-start_time,"s")
with open("processed-markers.json","w") as outfile:
    json_markers = json.dumps(markers,outfile,ensure_ascii=False,indent=4, sort_keys=True)
    outfile.write(json_markers)
    outfile.close
