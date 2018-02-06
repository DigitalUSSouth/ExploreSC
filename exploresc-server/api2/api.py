from flask import Flask, Response,request
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
    r =  Req.Request("http://localhost:8983/solr/duss-indexing/select?q=*%3A*{!geofilt}&sfield=geolocation_machine&pt="+parse.quote(latlng)+"&d=50&sort=geodist()+asc&wt=json&indent=true")
    resp = Req.urlopen(r)
    pprint(vars(resp))
    #json_text = json.dumps(resp.read(),ensure_ascii=False,indent=4, sort_keys=True)
    response = Response(resp.read())
    response.headers['Content-Type'] = 'application/json'
    return response