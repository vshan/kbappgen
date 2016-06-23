from flask import Flask, url_for, json, render_template, request, Response
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
        print("Dir name: " + os.path.dirname(os.path.realpath(__file__)));
        with open('data/app1.json', 'w') as outfile:
            json.dump(request.json, outfile)
        data = { 'response'  : 'true', 'name' : 'vinay' }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main__':
    app.run(port=int("5001"))