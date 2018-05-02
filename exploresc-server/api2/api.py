from flask import Flask, Response,request,render_template,g,redirect
from pprint import pprint
import json
from urllib import request as Req, parse
app = Flask(__name__)
import re,cgi
import sqlite3
DATABASE = 'data/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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

@app.route('/search', methods=['GET', 'POST'])
def search():
    response = Response("Search Results")
    #response.headers['Content-Type'] = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
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
        query = text.replace(':','').replace('(','').replace(')','').replace('[','').replace(']','')
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
                response = Response(render_template('noResults.html'))
        else:
            response = Response(render_template('noResults.html'))

    else:
        response = Response(render_template('noResults.html'))

    response.headers.add('Access-Control-Allow-Origin', '*')

    pprint(response)
    return response
    #response.headers['Content-Type'] = 'application/json'
    #return response
    #

@app.route('/items', methods=['GET'])
def view_items():
    #items = [{'title':"t1",'rel':[1,2,3]},{'title':"t2",'rel':[2,4,6]}]
    with open("markers_api.json") as file:
        markers = json.load(file)
    items = []
    for id,marker in markers.items():
        item = {
            'id':id,
            'rel':[],
            'title':marker['options']['title'],
            'desc':strip_html(marker['text'][:150])
            }
        rel_items = []
        with get_db() as db:
            for rel in query_db('select * from related_objects where object_id=?',[id]):
                rel_items.append(rel['related_item'])
        item['rel'] = rel_items
        print(rel_items)
        items.append(item)
    response = Response(render_template("items.html",items=items))
    return response

@app.route('/item', methods=['GET'])
def item_details():
    del_rel = request.args.get('del')
    id = request.args.get('id')
    add = request.args.get('add')
    if del_rel is not None:
        with get_db() as db:
            res = query_db("delete from related_objects where object_id=? and related_item=?",[id,del_rel])
        return redirect('/item?id='+id)
    if add is not None:
        with get_db() as db:
            res = query_db("insert into related_objects (object_id,related_item) VALUES (?,?)",[id,add])
        return redirect('/item?id='+id)
    with open("markers_api.json") as file:
        markers = json.load(file)
    item = []
    for key,value in markers[id].items():
        data = {}
        data['key'] = key
        data['value'] = strip_html(str(value))
        item.append(data)
    item.append({'key':'title','value':markers[id]['options']['title']})
    #pprint(markers[id])
    rel_items = []
    with get_db() as db:
        for rel in query_db('select * from related_objects where object_id=?',[id]):
            rel_items.append(rel['related_item'])
    response = Response(render_template("item.html",item=item,title=markers[id]['options']['title'],related_items=rel_items,object_id=id))
    return response

def strip_html(html):
	#from https://stackoverflow.com/a/19730306

	tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

	# Remove well-formed tags, fixing mistakes by legitimate users
	no_tags = tag_re.sub('', html)

	# Clean up anything else by escaping
	ready_for_web = cgi.escape(no_tags)
	return ready_for_web