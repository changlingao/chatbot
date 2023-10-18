from flask import Flask, jsonify, request, abort
import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import json_util, ObjectId
from bson.errors import InvalidId
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta

app = Flask(__name__)

#db
# mongodb link to be changed to read only access
uri = "mongodb+srv://changlin:chatbot@cluster0.vpvr7e8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.chatbot_database

#swagger.yaml file not yet integrated when running flask 

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route('/chats', methods=['GET'])
def db_get_chats():
    cursor = db.chats.find()
    ls = []
    for document in cursor:
        ls.append(document)
    return json.loads(json_util.dumps(ls))

@app.route('/chats/<oid>', methods=['GET'])
def get_chat_oid(oid):
    try:
        id = ObjectId(oid)
    except InvalidId:
        abort(404, description="Invalid ID")

    cursor = db.chats.find({"_id": ObjectId(str(oid))})

    # edit return value with content-type
    return json.loads(json_util.dumps(cursor)), 200

# http://127.0.0.1:5000/chats/daterange/?from_date=01-01-2001&to_date=13-12-2023
@app.route('/chats/daterange/', methods=["GET"])
def get_chat_daterange():
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    print(from_date, to_date)

    # db storing string atm using strfttime
    # string into datetime obj strptime
    try:
        from_date = datetime.strptime(from_date, "%d-%m-%Y")
        to_date = datetime.strptime(to_date, "%d-%m-%Y")
    except ValueError:
        abort(404, description="Date/s in incorrect format DD-MM-YYYY")

    query = {"date": {"$gte": from_date, "$lt": to_date}}  
    cursor = db.chats.find(query)
    return json.loads(json_util.dumps(cursor)), 200

# http://127.0.0.1:5000/chats/date/?date=13-10-2023
@app.route('/chats/date/', methods=["GET"])
def get_chat_date():
    date = request.args.get("date")

    try:
        date = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        abort(404, description="Dates in incorrect format DD-MM-YYYY")
    
    query = {"date": {"$gte": date, "$lt": date + timedelta(days=1)}}  
    cursor = db.chats.find(query)
    ls = []
    for document in cursor:
        ls.append(document)
    return json.loads(json_util.dumps(ls)), 200

# @app.route('/chats/summary/<string>', methods=["GET"])
# def get_chat_summary():
if __name__ == '__main__':
    app.run()
