from flask import Flask, url_for, json, render_template, request, Response
import transpiler
import os
app = Flask(__name__)

# --disable-web-security --user-data-dir
@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/load', methods=['GET'])
def api_load():
    data = {}
    with open('data/app1.json') as data_file:    
        data = json.load(data_file)
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/save', methods=['POST'])
def api_save():
    if request.headers['Content-Type'] == 'application/json':
        print("Got POST data " + json.dumps(request.json))
        print("Dir name: " + os.path.dirname(os.path.realpath(__file__)))
        with open('data/app1.json', 'w') as outfile:
            json.dump(request.json, outfile)
        data = { 'response'  : 'true', 'name' : 'vinay' }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    else:
        return "415 Unsupported Media Type ;)"

@app.route('/tell', methods=['POST'])
def api_tell():
    if request.headers['Content-Type'] == 'application/json':
        print("Got POST data " + json.dumps(request.json))
        stat = request.json['statement']
        data = {}
        if transpiler.kb_add(stat):
            data = {'response' : 'success'}
        else:
            data = {'response' : 'fail'}
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    else:
        return "415 Unsupported Media Type ;)"

@app.route('/query', methods=['GET'])
def api_query():
    if request.headers['Content-Type'] == 'application/json':
        print("Got POST data " + json.dumps(request.json))
        query = request.json['query']
        data = {}
        sol = transpiler.kb_query(query)
        if sol:
            data = {'response' : 'success', 'solution' : sol}
        else:
            data = {'response' : 'success', 'solution' : ['Nothing found!']}
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    else:
        return "415 Unsupported Media Type ;)"

@app.route('/fol_query', methods=['GET'])
def api_fol_query():
    if request.headers['Content-Type'] == 'application/json':
        print("Got POST data " + json.dumps(request.json))
        query = request.json['query']
        data = {}
        sol = transpiler.kb_fol_query(query)
        if sol:
            data = {'response' : 'success', 'solution' : sol}
        else:
            data = {'response' : 'success', 'solution' : ['Nothing found!']}
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
    app.run(port=int("5001"))