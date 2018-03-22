#script to gather relevant marker data from from full markers

import json
from pprint import pprint
import time
from nlputils import tokenize_text
start_time = time.time()
with open("raw-markers.json", "r") as datafile:
    full_markers = json.load(datafile)
    datafile.close()



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
    text = marker["name"]+" "+marker["cmt"] +" " + marker["desc"]
    marker["tokens"],marker["doc_len"] = tokenize_text(text)
    markers.append(marker)

print(len(markers))
print("Exec time",time.time()-start_time,"s")
with open("markers.json","w") as outfile:
    json_markers = json.dumps(markers,outfile,ensure_ascii=False,indent=4, sort_keys=True)
    outfile.write(json_markers)
    outfile.close
