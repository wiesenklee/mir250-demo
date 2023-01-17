from flask import Flask, request
from rosbridge.mir import MirInspect

app = Flask(__name__)

mir = None

@app.route("/")
def hello():
    greeting = '<h2>Welcome to MiR250 custom web interface!</h2>'
    list = '<p>These endpoints are avaiable:</p>'
    list += '<ul>'
    list += '<li><a href="/connect">/connect</a></li>'
    list += '<li><a href="/list">/list</a></li>'
    list += '<li><a href="/echo">/echo</a></li>'
    list += '</ul>'
    return greeting + list

@app.route("/connect")
def connect():
    global mir
    if (mir == None): 
        host = request.args.get("host", default= "mir.com", type=str)
        mir = MirInspect(host)
        try: mir.connect()
        except: return "Cloud not connect to 'mir.com'. Specify host with the '?host=' parameter!"
    return 'Connected! <a href="/">Back</a>'

@app.route("/list")
def list():
    global mir
    if (mir == None): return 'Not yet connected to mir, go to <a href="/connect">/connect</a>.'
    return mir.topic_list()

@app.route("/echo")
def echo():
    global mir
    if (mir == None): return 'Not yet connected to mir, go to <a href="/connect">/connect</a>.'
    topic = request.args.get("topic", default= "", type=str)
    return mir.topic_list()
