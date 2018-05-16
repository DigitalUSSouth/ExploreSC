from flask import Flask, Response,request,render_template,g,redirect
from pprint import pprint
import json
from urllib import request as Req, parse
app = Flask(__name__)
import re,cgi
import sqlite3
DATABASE = 'data/database.db'

exec(open("./config.py").read())

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
    r =  Req.Request("http://localhost:8983/solr/exploresc/select?q=*%3A*{!geofilt}&sfield=geolocation_machine&pt="+
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
    #response = Response("Search Results")
    query = request.args.get('q')
    print(query)
    escape_string = '+-&|!(){}[]^"~*?:\/'
    for char in escape_string:
        query = query.replace(char,' ')
        #query = text.replace(':','').replace('(','').replace(')','').replace('[','').replace(']','').replace('~','')
    query = strip_html(query)
    print(query)
    query_url = "http://localhost:8983/solr/exploresc/select?q=title:("+ parse.quote(query) + ")%0Aalternative_title:("+ parse.quote(query) + ")%0Adescription:("+ parse.quote(query) + ")&start=0&rows=20&wt=json&hl=true&hl.simple.pre=<mark>&hl.simple.post=<%2Fmark>&hl.fl=*&facet=true&facet.field=archive_facet&facet.field=contributing_institution_facet&facet.field=subject_heading_facet&facet.field=type_content&facet.field=file_format&facet.field=language&stats=true&stats.field=years&indent=true" 
    r =  Req.Request(query_url)
    resp = Req.urlopen(r)
    pprint(vars(resp))
    response = Response(resp.read())
    #response.headers['Content-Type'] = 'application/json'
    #response = Response(query_url)
    response.headers['Content-Type'] = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getRel', methods=['GET'])
#@crossdomain(origin='*')
def get_rel():
    with open("markers_api.json","r") as json_file:
        markers = json.load(json_file)
    #json_text = json.dumps(posts['image'],ensure_ascii=False,indent=4, sort_keys=True)
    markerId = request.args.get('link')
    retJson = request.args.get('json')
    if retJson=="true":
        returnJson = True
    else:
        returnJson = False
    if markerId in markers:
        with get_db() as db:
            rel_items = []
            for rel in query_db('select * from related_objects where object_id=?',[markerId]):
                rel_items.append(rel['related_item'])
            if rel_items:
                stripped_docs = []
                for item in rel_items:
                    title,excerpt = get_url_details(item)
                    new_doc = {
                        'url':item.replace('https','http'),
                        'title':title,
                        'excerpt':excerpt
                    }
                    stripped_docs.append(new_doc)
                if returnJson:
                    response =  Response(json.dumps({'title':markers[markerId]['options']['title'],"results":stripped_docs}))
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers['Content-Type'] = 'application/json'
                    return response

                response = Response(render_template('showMore.html',title=markers[markerId]['options']['title'],docs=stripped_docs))
                response.headers.add('Access-Control-Allow-Origin', '*')
                pprint(response)
                return response

        text = markers[markerId]['text']
        #excape characters for solr query
        escape_string = '+-&|!(){}[]^"~*?:\/'
        query = text[:150]
        for char in escape_string:
            query = query.replace(char,' ')
        #query = text.replace(':','').replace('(','').replace(')','').replace('[','').replace(']','').replace('~','')
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
                if returnJson:
                    response =  Response(json.dumps({'title':markers[markerId]['options']['title'],"results":stripped_docs}))
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers['Content-Type'] = 'application/json'
                    return response
                response = Response(render_template('showMore.html',title=markers[markerId]['options']['title'],docs=stripped_docs))
            else:
                if returnJson:
                    response =  Response(json.dumps({"results":"No results"}))
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers['Content-Type'] = 'application/json'
                    return response
                response = Response(render_template('noResults.html'))
        else:
            if returnJson:
                    response =  Response(json.dumps({"results":"No results"}))
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers['Content-Type'] = 'application/json'
                    return response
            response = Response(render_template('noResults.html'))

    else:
        if returnJson:
                    response =  Response(json.dumps({"results":"No results"}))
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers['Content-Type'] = 'application/json'
                    return response
        response = Response(render_template('noResults.html'))

    response.headers.add('Access-Control-Allow-Origin', '*')

    pprint(response)
    return response
    #response.headers['Content-Type'] = 'application/json'
    #return response
    #

def get_url_details(url):
    import lxml.html
    t = lxml.html.parse(url.replace('https','http'))
    paragraphs = t.xpath('//p')
    p1 = ""
    counter = 0
    for ps in paragraphs:
        p1 += ps.text
        if counter== 2:
            break
        counter +=1
    return t.find(".//title").text, strip_html(p1[:150])

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
            'title':strip_html(marker['options']['title']),
            'desc':strip_html(marker['text'][:150])
            }
        rel_items = []
        with get_db() as db:
            for rel in query_db('select * from related_objects where object_id=?',[id]):
                rel_items.append(rel['related_item'])
        item['rel'] = rel_items
        #print(rel_items)
        items.append(item)
    response = Response(render_template("items.html",items=items))
    return response

@app.route('/item', methods=['GET','POST'])
def item_details():
    if request.method == 'POST':
        id = request.values.get('id')
    else:
        id = request.args.get('id')
    del_rel = request.values.get('del')
    add = request.values.get('add')
    add_cat = request.values.get('add_cat')
    del_cat = request.values.get('del_cat')
    message = request.args.get('msg')
    password = request.values.get('password')
    if password is None:
        password = ""
    if message is None:
        message = ""
    if del_rel is not None:
        if password != pass_word:
            return redirect(url_root+'/item?id='+id+"&msg=Invalid+password")
        with get_db() as db:
            res = query_db("delete from related_objects where object_id=? and related_item=?",[id,del_rel])
        return redirect(url_root+'/item?id='+id+"&msg=Deleted+item")
    if add is not None:
        if password != pass_word:
            return redirect(url_root+'/item?id='+id+"&msg=Invalid+password")
        with get_db() as db:
            res = query_db("insert into related_objects (object_id,related_item) VALUES (?,?)",[id,add])
        return redirect(url_root+'/item?id='+id+"&msg=Added+item")
    if del_cat is not None:
        if password != pass_word:
            return redirect(url_root+'/item?id='+id+"&msg=Invalid+password")
        with open("data/categories.json") as file:
            cat_dict = json.load(file)
            cat_key = None
            for k,v in cat_dict.items():
                if v==del_cat:
                    cat_key = k
        if cat_key is None:
            return redirect(url_root+'/item?id='+id+"&msg=Error:+Invalid+category")  
        with get_db() as db:
            res = query_db("delete from categories where object_id=? and category=?",[id,cat_key])
        return redirect(url_root+'/item?id='+id+"&msg=Deleted+category")
    if add_cat is not None:
        if password != pass_word:
            return redirect(url_root+'/item?id='+id+"&msg=Invalid+password")
        with open("data/categories.json") as file:
            cat_dict = json.load(file)
            if add_cat not in cat_dict:
                return redirect(url_root+'/item?id='+id+"&msg=Error:+Invalid+category")
        with get_db() as db:
            res = query_db("insert into categories (object_id,category) VALUES (?,?)",[id,add_cat])
        return redirect(url_root+'/item?id='+id+"&msg=Added+category")
    with open("markers_api.json") as file:
        markers = json.load(file)
    item = []
    for key,value in markers[id].items():
        data = {}
        if key=='popup':
            continue
        data['key'] = key
        data['value'] = strip_html(str(value))
        item.append(data)
    item.append({'key':'title','value':markers[id]['options']['title']})
    #pprint(markers[id])
    rel_items = []
    with get_db() as db:
        for rel in query_db('select * from related_objects where object_id=?',[id]):
            rel_items.append(rel['related_item']) 
    categories = []
    with get_db() as db:
        with open("data/categories.json") as file:
            cat_dict = json.load(file)
        for rel in query_db('select * from categories where object_id=?',[id]):
            if rel['category'] not in cat_dict:
                continue
            categories.append(cat_dict[rel['category']])
    cat_dict= {int(k):v for k,v in cat_dict.items()}
    response = Response(render_template("item.html",
        item=item,
        title=markers[id]['options']['title'],
        related_items=rel_items,
        object_id=id,
        categories=categories,
        cat_dict=sorted(cat_dict.items()),
        message_text = message,
        url_root = url_root
        ))
    return response

def strip_html(html):
	#from https://stackoverflow.com/a/19730306

	tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

	# Remove well-formed tags, fixing mistakes by legitimate users
	no_tags = tag_re.sub('', html)

	# Clean up anything else by escaping
	ready_for_web = cgi.escape(no_tags)
	return ready_for_web

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=5000)