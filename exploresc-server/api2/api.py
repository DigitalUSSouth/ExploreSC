from flask import Flask, Response,request,render_template
from pprint import pprint
import json
from urllib import request as Req, parse
app = Flask(__name__)
import re,cgi

@app.route('/getAllSCEEntries')
def get_all_sce_entries():
    with open("sceposts.json","r") as json_file:
        posts = json.load(json_file)
    json_text = json.dumps(posts['entry'],ensure_ascii=False,indent=4, sort_keys=True)
    response = Response(json_text)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/getAllSCEImages')
def get_all_sce_images():
    with open("sceposts.json","r") as json_file:
        posts = json.load(json_file)
    json_text = json.dumps(posts['image'],ensure_ascii=False,indent=4, sort_keys=True)
    response = Response(json_text)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/getItemsNear', methods=['GET', 'POST'])
def get_items_near():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    latlng = str(lat)+","+str(lng)
    r =  Req.Request("http://localhost:8983/solr/duss-indexing/select?q=*%3A*{!geofilt}&sfield=geolocation_machine&pt="+
        parse.quote(latlng)+
        '&d=50&sort=geodist()+asc&rows=10&fq=archive:"Historical+Marker+Database"&wt=json&indent=true')
    resp = Req.urlopen(r)
    pprint(vars(resp))
    #json_text = json.dumps(resp.read(),ensure_ascii=False,indent=4, sort_keys=True)
    response = Response(resp.read())
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/getRel', methods=['GET'])
#@crossdomain(origin='*')
def get_rel():
    with open("markers_api.json","r") as json_file:
        markers = json.load(json_file)
    #json_text = json.dumps(posts['image'],ensure_ascii=False,indent=4, sort_keys=True)
    markerId = request.args.get('link')
    if markerId in markers:
        text = markers[markerId]['text']
        #print(text)
        query = text[:150].replace(':','').replace('(','').replace(')','').replace('[','').replace(']','')
        print(query)
        query = parse.quote(strip_html(query))
        url = 'https://www.digitalussouth.org/api?q='+ query +'&start=0&fq[]="South+Carolina+Encyclopedia"&fq_field[]=archive_facet'
        print(url)
        print(query)
        r =  Req.Request(url)
        resp = Req.urlopen(r)
        data = json.loads(resp.read().decode())

        if data['error'] == "None":
            if data['response']['numFound'] > 0:
                docs = []
                if data['response']['numFound']>10:
                    docs = data['response']['docs'][:10]
                else:
                    docs = data['response']['docs']
                stripped_docs = []
                for doc in docs:
                    new_doc = {
                        'url':doc['url'],
                        'title':doc['title'],
                        'excerpt':strip_html(doc['full_text'][:150])
                    }
                    stripped_docs.append(new_doc)
                response = Response(render_template('showMore.html',title=markers[markerId]['options']['title'],docs=stripped_docs))
        else:
            response = Response(render_template('No results found'))

    else:
        response = Response(render_template('No results found'))

    response.headers.add('Access-Control-Allow-Origin', '*')

    pprint(response)
    return response
    #response.headers['Content-Type'] = 'application/json'
    #return response
    #

def strip_html(html):
	#from https://stackoverflow.com/a/19730306

	tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

	# Remove well-formed tags, fixing mistakes by legitimate users
	no_tags = tag_re.sub('', html)

	# Clean up anything else by escaping
	ready_for_web = cgi.escape(no_tags)
	return ready_for_web