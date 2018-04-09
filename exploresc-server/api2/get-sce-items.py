#script to gather encyclopedia data

import json
from pprint import pprint
from nlputils import tokenize_text
import time
start_time = time.time()

exec(open("./db-config.py").read())

query = ("SELECT id,post_title,post_name,post_date,"
+"post_excerpt,post_content,post_type FROM scecms_posts WHERE post_status='publish'")

cursor.execute(query)

counter = 1
posts = {}
for doc in cursor:
    allowed_types = ['entry','document','image','recording','video']
    if doc[6] not in allowed_types:
        continue
    type_url = {'entry':'entries',
        'document':'documents',
        'image':'images',
        'recording':'recordings',
        'video':'videos'
        }
    post_type = doc[6]
    post_type_url = type_url[doc[6]]
    docdict = {
        'id': doc[0],
        'title': doc[1],
        'url': "http://www.scencyclopedia.org/sce/"+post_type_url+"/"+str(doc[2]),
        'date': str(doc[3]),
        'excerpt': doc[4],
        'content': doc[5],
        'type': doc[6]
    }
    text = docdict['title'] + " " + docdict['content']
    docdict["tokens"],docdict["doc_len"] = tokenize_text(text)
    if post_type in posts:
        posts[post_type].append(docdict)
    else:
        posts[post_type] = [docdict]


print(len(posts))
print("Exec time",time.time()-start_time,"s")

for post_type in posts:
    print(post_type,len(posts[post_type]))

with open("sceposts.json","w") as outfile:
    docFile = json.dumps(posts,outfile,ensure_ascii=False,indent=4, sort_keys=True)
    outfile.write(docFile)
    outfile.close