# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# if __name__ == "__main__":
#     app.run()

from flask import Flask, url_for, json, render_template, request, Response
app = Flask(__name__)

# from datetime import timedelta
# from flask import make_response, request, current_app
# from functools import update_wrapper


# def crossdomain(origin=None, methods=None, headers=None,
#                 max_age=21600, attach_to_all=True,
#                 automatic_options=True):
#     if methods is not None:
#         methods = ', '.join(sorted(x.upper() for x in methods))
#     if headers is not None and not isinstance(headers, str):
#         headers = ', '.join(x.upper() for x in headers)
#     if not isinstance(origin, str):
#         origin = ', '.join(origin)
#     if isinstance(max_age, timedelta):
#         max_age = max_age.total_seconds()

#     def get_methods():
#         if methods is not None:
#             return methods

#         options_resp = current_app.make_default_options_response()
#         return options_resp.headers['allow']

#     def decorator(f):
#         def wrapped_function(*args, **kwargs):
#             if automatic_options and request.method == 'OPTIONS':
#                 resp = current_app.make_default_options_response()
#             else:
#                 resp = make_response(f(*args, **kwargs))
#             if not attach_to_all and request.method != 'OPTIONS':
#                 return resp

#             h = resp.headers
#             h['Access-Control-Allow-Origin'] = origin
#             h['Access-Control-Allow-Methods'] = get_methods()
#             h['Access-Control-Max-Age'] = str(max_age)
#             h['Access-Control-Allow-Credentials'] = 'true'
#             h['Access-Control-Allow-Headers'] = \
#                 "Origin, X-Requested-With, Content-Type, Accept, Authorization"
#             if headers is not None:
#                 h['Access-Control-Allow-Headers'] = headers
#             return resp

#         f.provide_automatic_options = False
#         return update_wrapper(wrapped_function, f)
#     return decorator

# --disable-web-security --user-data-dir
@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/save', methods=['POST', 'OPTIONS'])
# @crossdomain(origin='*')
def api_save():
    if request.headers['Content-Type'] == 'application/json':
        print("Got POST data " + json.dumps(request.json))
        data = { 'response'  : 'true', 'name' : 'vinay' }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main__':
    app.run(port=int("5001"))