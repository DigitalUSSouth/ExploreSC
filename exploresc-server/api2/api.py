from flask import Flask, Response,request,render_template
from pprint import pprint
import json
from urllib import request as Req, parse
app = Flask(__name__)

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
        "&d=50&sort=geodist()+asc&rows=10&wt=json&indent=true")
    resp = Req.urlopen(r)
    pprint(vars(resp))
    #json_text = json.dumps(resp.read(),ensure_ascii=False,indent=4, sort_keys=True)
    response = Response(resp.read())
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/getRel', methods=['GET'])
#@crossdomain(origin='*')
def get_rel():
    #with open("sceposts.json","r") as json_file:
    #    posts = json.load(json_file)
    #json_text = json.dumps(posts['image'],ensure_ascii=False,indent=4, sort_keys=True)
    r =  Req.Request('https://www.digitalussouth.org/api?q=pickens&start=0&fq[]="South+Carolina+Encyclopedia"&fq_field[]=archive_facet')
    resp = Req.urlopen(r)
    #pprint(vars(resp))
    data = json.loads(resp.read().decode())
    #data
    
    #print(type(data))
    data = data['response']
    
    response = Response(render_template('showMore.html',title=data['error']))
    #response = Response(resp.read())

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    #response.headers['Content-Type'] = 'application/json'
    #return response
    #